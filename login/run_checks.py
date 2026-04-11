#!/usr/bin/env python3
"""
run_checks.py — Multi-site login checker with explicit pairs and matrix test modes.

Usage:
    python run_checks.py --config sites.yaml
    python run_checks.py --config sites.yaml --parallel

Config supports two modes per site:

  # Mode 1: Explicit pairs (original behaviour)
  - name: Jellyfin
    url: http://localhost:8096/login
    success: url:/home
    logins:
      - username: ben
        password: mypassword

  # Mode 2: Matrix — every combination of usernames x passwords
  # Use expect_fail to mark combinations that should NOT succeed
  - name: My Auth System
    url: http://localhost:8080/login
    success: url:/dashboard
    test_matrix:
      usernames:
        - ben@example.com
        - admin@example.com
        - fake@example.com
      passwords:
        - correctpassword
        - wrongpassword
      expect_fail:
        - [fake@example.com, correctpassword]
        - [ben@example.com, wrongpassword]

Both modes can be mixed in the same config file.
"""

import argparse
import concurrent.futures
import time
from dataclasses import dataclass, field

import yaml

from login_check import LoginResult, attempt_login

# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    site:        str
    username:    str
    password:    str
    result:      LoginResult
    elapsed:     float
    expected_ok: bool = True      # True = login should succeed

    @property
    def correct(self) -> bool:
        """Did the actual outcome match the expected outcome?"""
        return (self.result.status == "OK") == self.expected_ok


# ---------------------------------------------------------------------------
# Job building
# ---------------------------------------------------------------------------

def build_jobs(config: dict) -> list[tuple[dict, dict, bool]]:
    """
    Returns a flat list of (site_config, login_dict, expected_ok) tuples.

    Handles both 'logins' (explicit pairs) and 'test_matrix' (all combos).
    """
    jobs: list[tuple[dict, dict, bool]] = []

    for site in config["sites"]:
        if "test_matrix" in site:
            matrix = site["test_matrix"]
            expect_fail = {
                tuple(pair) for pair in matrix.get("expect_fail", [])
            }
            for username in matrix["usernames"]:
                for password in matrix["passwords"]:
                    expected_ok = (username, password) not in expect_fail
                    jobs.append((site, {"username": username, "password": password}, expected_ok))
        else:
            for login in site.get("logins", []):
                jobs.append((site, login, True))

    return jobs


# ---------------------------------------------------------------------------
# Single check runner
# ---------------------------------------------------------------------------

def run_single(site: dict, login: dict, expected_ok: bool) -> CheckResult:
    start = time.monotonic()
    result = attempt_login(
        url               = site["url"],
        username          = login["username"],
        password          = login["password"],
        user_sel          = site.get("user_field"),
        pass_sel          = site.get("pass_field"),
        submit_sel        = site.get("submit"),
        success_indicator = site.get("success", ""),
        timeout           = site.get("timeout", 15),
        headless          = site.get("headless", True),
    )
    return CheckResult(
        site        = site["name"],
        username    = login["username"],
        password    = login["password"],
        result      = result,
        elapsed     = time.monotonic() - start,
        expected_ok = expected_ok,
    )


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(results: list[CheckResult]) -> None:
    width = 72

    # Separate matrix-mode results (have an expected outcome) from plain results
    has_matrix = any(not r.expected_ok for r in results)

    print(f"\n{BOLD}{'═' * width}{RESET}")
    print(f"{BOLD}  LOGIN CHECK REPORT{RESET}")
    print(f"{BOLD}{'═' * width}{RESET}\n")

    sites = list(dict.fromkeys(r.site for r in results))

    for site in sites:
        site_results = [r for r in results if r.site == site]
        is_matrix    = any(not r.expected_ok for r in site_results) or \
                       len({r.password for r in site_results}) > 1

        print(f"{CYAN}{BOLD}  {site}{RESET}")

        if is_matrix:
            # Matrix mode — show expected vs actual
            _print_matrix_rows(site_results)
        else:
            # Original mode — simple pass/fail
            _print_simple_rows(site_results)

        print()

    # Summary
    if has_matrix:
        correct   = [r for r in results if r.correct]
        incorrect = [r for r in results if not r.correct]
        print(f"{BOLD}{'─' * width}{RESET}")
        print(
            f"  {BOLD}Total:{RESET} {len(results)}  "
            f"{GREEN}{BOLD}{len(correct)} correct{RESET}  "
            f"{RED}{BOLD}{len(incorrect)} unexpected{RESET}"
        )
    else:
        ok     = [r for r in results if r.result.status == "OK"]
        failed = [r for r in results if r.result.status != "OK"]
        print(f"{BOLD}{'─' * width}{RESET}")
        print(
            f"  {BOLD}Total:{RESET} {len(results)}  "
            f"{GREEN}{BOLD}{len(ok)} passed{RESET}  "
            f"{RED}{BOLD}{len(failed)} failed{RESET}"
        )

    print(f"{BOLD}{'═' * width}{RESET}\n")


def _print_simple_rows(results: list[CheckResult]) -> None:
    for r in results:
        ok      = r.result.status == "OK"
        icon    = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
        status  = f"{GREEN}OK{RESET}"     if ok else f"{RED}FAILED{RESET}"
        elapsed = f"{DIM}{r.elapsed:.1f}s{RESET}"
        print(f"    {icon}  {r.username:<28} {status:<10} {elapsed}")
        if not ok:
            print(f"       {DIM}↳ {r.result.detail}{RESET}")


def _print_matrix_rows(results: list[CheckResult]) -> None:
    for r in results:
        actual_ok = r.result.status == "OK"

        if r.correct:
            icon  = f"{GREEN}✓{RESET}"
            label = f"{GREEN}CORRECT{RESET}  "
        else:
            icon  = f"{RED}✗{RESET}"
            unexpected = "SHOULD FAIL" if actual_ok else "SHOULD PASS"
            label = f"{RED}UNEXPECTED ({unexpected}){RESET}"

        exp     = f"{DIM}(expected {'OK' if r.expected_ok else 'FAIL'}){RESET}"
        elapsed = f"{DIM}{r.elapsed:.1f}s{RESET}"
        print(f"    {icon}  {r.username:<25} {r.password:<18} {label} {exp} {elapsed}")
        if not r.correct:
            print(f"       {DIM}↳ {r.result.detail}{RESET}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Multi-site login checker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--config",   default="sites.yaml", help="Path to YAML config (default: sites.yaml)")
    p.add_argument("--parallel", action="store_true",  help="Run all checks concurrently")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    jobs = build_jobs(config)
    site_count = len(config["sites"])

    print(f"\n{BOLD}Running {len(jobs)} check(s) across {site_count} site(s)...{RESET}\n")

    results: list[CheckResult] = []

    if args.parallel:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            futures = {
                ex.submit(run_single, site, login, expected_ok): (site, login)
                for site, login, expected_ok in jobs
            }
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
    else:
        for site, login, expected_ok in jobs:
            print(f"  {DIM}Checking {site['name']} → {login['username']}...{RESET}")
            results.append(run_single(site, login, expected_ok))

    # Restore site order for the report
    site_order = {s["name"]: i for i, s in enumerate(config["sites"])}
    results.sort(key=lambda r: (site_order.get(r.site, 99), r.username))

    print_report(results)


if __name__ == "__main__":
    main()