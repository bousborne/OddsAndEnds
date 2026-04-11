#!/usr/bin/env python3
"""
login_check.py — Automated login verifier for local web services.

Usage:
    python login_check.py --url http://localhost:8080/login \
                          --username admin \
                          --password secret

    # With explicit selectors (overrides auto-detection):
    python login_check.py --url http://localhost:8080/login \
                          --username admin --password secret \
                          --user-field "input[name='email']" \
                          --pass-field "input[name='password']" \
                          --submit    "button[type='submit']" \
                          --success   "url:/dashboard"

Exit codes:
    0 — login succeeded
    1 — login failed or error
"""
import pdb
import argparse
import logging
import sys
import time
from dataclasses import dataclass
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger("login_check")


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class LoginResult:
    status: str       # "OK" | "FAILED"
    detail: str       # human-readable explanation
    final_url: str = ""

    def __str__(self) -> str:
        base = f"[{self.status}] {self.detail}"
        if self.final_url:
            base += f" — {self.final_url}"
        return base


# ---------------------------------------------------------------------------
# Shadow DOM JavaScript helpers
# ---------------------------------------------------------------------------

_DEEP_QUERY_ALL_JS = """
    function deepQueryAll(root, sel, results) {
        root.querySelectorAll(sel).forEach(el => results.push(el));
        for (const node of root.querySelectorAll('*')) {
            if (node.shadowRoot) deepQueryAll(node.shadowRoot, sel, results);
        }
        return results;
    }
    return deepQueryAll(document, arguments[0], []);
"""


# ---------------------------------------------------------------------------
# Field auto-detection heuristics
# ---------------------------------------------------------------------------

_USERNAME_CANDIDATES = [
    "input[type='email']",
    "input[name='email']",
    "input[id='email']",
    "input[name='username']",
    "input[id='username']",
    "input[autocomplete*='username']",
    "input[autocomplete*='email']",
    "input[autocomplete='username']",
    "input[autocomplete='email']",
    "input[name='user']",
    "input[id='user']",
    "input[name='login']",
    "input[id='login']",
    "input[type='text']",
]

_PASSWORD_CANDIDATES = [
    "input[type='password']",
    "input[name='password']",
    "input[id='password']",
    "input[autocomplete='current-password']",
    "input[name='pass']",
    "input[id='pass']",
]

_SUBMIT_CANDIDATES = [
    "button[type='submit']",
    "input[type='submit']",
    "button[name='submit']",
    "button[name='login']",
    "[role='button'][aria-label*='Log']",
    "[role='button'][aria-label*='Sign']",
    "[role='button'][aria-label*='Continue']",
]

_SUBMIT_TEXT_KEYWORDS = ("log in", "login", "sign in", "signin", "submit", "continue")


def _find_first_visible(driver: webdriver.Chrome, selectors: list[str]) -> Optional[WebElement]:
    """
    Return the first visible element matching any selector.
    Tries standard DOM first, then recurses into shadow roots.
    """
    for sel in selectors:
        # 1. Standard DOM (fast path)
        try:
            for el in driver.find_elements(By.CSS_SELECTOR, sel):
                if el.is_displayed() and el.is_enabled():
                    log.debug("  Matched (DOM): %s", sel)
                    return el
        except Exception:
            pass

        # 2. Shadow DOM deep pierce (slow path)
        try:
            for el in (driver.execute_script(_DEEP_QUERY_ALL_JS, sel) or []):
                try:
                    if el.is_displayed() and el.is_enabled():
                        log.debug("  Matched (shadow DOM): %s", sel)
                        return el
                except Exception:
                    continue
        except Exception:
            continue

    return None


def _find_submit_button(driver: webdriver.Chrome, explicit_sel: Optional[str]) -> Optional[WebElement]:
    """Locate the submit button, falling back to text-content matching."""
    if explicit_sel:
        return _find_first_visible(driver, [explicit_sel])

    el = _find_first_visible(driver, _SUBMIT_CANDIDATES)
    if el:
        return el

    # Fallback: match by visible button text
    for tag in ("button", "input[type='button']", "a"):
        try:
            for c in (driver.execute_script(_DEEP_QUERY_ALL_JS, tag) or []):
                try:
                    if not c.is_displayed():
                        continue
                    text = (c.text or c.get_attribute("value") or "").lower()
                    if any(kw in text for kw in _SUBMIT_TEXT_KEYWORDS):
                        log.debug("  Matched submit by text: '%s'", text.strip())
                        return c
                except Exception:
                    continue
        except Exception:
            continue

    return None


def _click_element(driver: webdriver.Chrome, el: WebElement) -> None:
    """
    Click an element using multiple fallback strategies.
    Handles web components that swallow native Selenium clicks.
    """
    # 1. Native Selenium click
    try:
        el.click()
        return
    except Exception:
        pass

    # 2. JavaScript .click()
    try:
        driver.execute_script("arguments[0].click()", el)
        return
    except Exception:
        pass

    # 3. Dispatch a real MouseEvent
    try:
        driver.execute_script("""
            arguments[0].dispatchEvent(
                new MouseEvent('click', {bubbles: true, cancelable: true})
            )
        """, el)
        return
    except Exception:
        pass

    # 4. ActionChains as last resort
    ActionChains(driver).move_to_element(el).click().perform()


# ---------------------------------------------------------------------------
# Success-state detection
# ---------------------------------------------------------------------------

def _check_success(driver: webdriver.Chrome, indicator: str, pre_login_url: str) -> bool:
    """
    Determine whether the login succeeded.

    indicator formats:
      url:/some/path  — post-login URL must contain the fragment
      url:*           — any URL change counts as success
      #css-selector   — element must be present after login
      (empty)         — URL-change heuristic
    """
    current_url = driver.current_url

    if not indicator or indicator == "url:*":
        return current_url != pre_login_url

    if indicator.startswith("url:"):
        return indicator[4:] in current_url

    try:
        elements = driver.find_elements(By.CSS_SELECTOR, indicator)
        return any(el.is_displayed() for el in elements)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_driver(headless: bool) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0)
    return driver


def attempt_login(
    url: str,
    username: str,
    password: str,
    user_sel: Optional[str] = None,
    pass_sel: Optional[str] = None,
    submit_sel: Optional[str] = None,
    success_indicator: str = "",
    timeout: int = 15,
    headless: bool = False,
) -> LoginResult:

    driver = build_driver(headless)
    wait = WebDriverWait(driver, timeout)

    try:
        log.info("Navigating to %s", url)
        driver.get(url)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Wait until a known input field is present in the DOM (including shadow DOM)
        log.info("Waiting for login form to hydrate …")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            el = _find_first_visible(driver, _USERNAME_CANDIDATES)
            if el:
                break
            time.sleep(0.3)

        pre_login_url = driver.current_url
        log.info("Page loaded: %s", pre_login_url)

        # --- Locate fields ---
        log.info("Locating username field …")
        user_field = _find_first_visible(driver, [user_sel] if user_sel else _USERNAME_CANDIDATES)
        if not user_field:
            return LoginResult("FAILED", "Could not locate a username/email input field")
        log.info("  ✓ Username field found")

        log.info("Locating password field …")
        pass_field = _find_first_visible(driver, [pass_sel] if pass_sel else _PASSWORD_CANDIDATES)
        if not pass_field:
            return LoginResult("FAILED", "Could not locate a password input field")
        log.info("  ✓ Password field found")

        log.info("Locating submit button …")
        submit_btn = _find_submit_button(driver, submit_sel)
        if not submit_btn:
            return LoginResult("FAILED", "Could not locate a submit/login button")
        log.info("  ✓ Submit button found")

        # --- Fill credentials ---
        user_field.clear()
        user_field.send_keys(username)
        time.sleep(0.1)

        pass_field.clear()
        pass_field.send_keys(password)
        time.sleep(0.1)

        # --- Submit ---
        # --- Submit ---
        log.info("Submitting login form …")
        _click_element(driver, submit_btn)

        # Poll for any sign the page has responded
        def login_complete(d):
            # 1. URL changed
            if d.current_url != pre_login_url:
                return True
            # 2. An error message appeared
            error_selectors = [
                "[role='alert']",
                ".error",
                "[class*='error']",
                "[class*='invalid']",
                "[aria-invalid='true']",
            ]
            for sel in error_selectors:
                try:
                    els = d.find_elements(By.CSS_SELECTOR, sel)
                    if any(e.is_displayed() for e in els):
                        return True
                except Exception:
                    pass
            return False

        try:
            wait.until(login_complete)
        except TimeoutException:
            log.warning("Timed out waiting for post-login response")

        post_url = driver.current_url
        log.info("Post-login URL: %s", post_url)

        if _check_success(driver, success_indicator, pre_login_url):
            return LoginResult("OK", "Login succeeded", final_url=post_url)
        else:
            return LoginResult("FAILED", "Login form submitted but success indicator not met", final_url=post_url)

    except WebDriverException as exc:
        return LoginResult("FAILED", f"WebDriver error: {exc.msg or exc}")
    except Exception as exc:
        return LoginResult("FAILED", f"Unexpected error: {exc}")
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Automated login verifier for local web services.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--url",        required=True,  help="Full URL of the login page")
    p.add_argument("--username",   required=True,  help="Username or email")
    p.add_argument("--password",   required=True,  help="Password")
    p.add_argument("--user-field", default=None,   help="CSS selector for username input (auto-detected if omitted)")
    p.add_argument("--pass-field", default=None,   help="CSS selector for password input (auto-detected if omitted)")
    p.add_argument("--submit",     default=None,   help="CSS selector for submit button (auto-detected if omitted)")
    p.add_argument("--success",    default="",     help="Success indicator: url:/path, url:*, CSS selector, or empty for URL-change heuristic")
    p.add_argument("--timeout",    type=int, default=15, help="Wait timeout in seconds (default: 15)")
    p.add_argument("--headless",   action="store_true",  help="Run Chrome headlessly (no visible window)")
    p.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)

    log.info("=" * 55)
    log.info("login_check — target: %s", args.url)
    log.info("=" * 55)

    result = attempt_login(
        url=args.url,
        username=args.username,
        password=args.password,
        user_sel=args.user_field,
        pass_sel=args.pass_field,
        submit_sel=args.submit,
        success_indicator=args.success,
        timeout=args.timeout,
        headless=args.headless,
    )

    log.info("=" * 55)
    print(result)
    log.info("=" * 55)

    sys.exit(0 if result.status == "OK" else 1)


if __name__ == "__main__":
    main()