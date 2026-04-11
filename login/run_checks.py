#!/usr/bin/env python3
"""
run_checks.py — Run login_check against multiple sites and credentials.

Usage:
    python run_checks.py --config sites.yaml
    python run_checks.py --config sites.yaml --parallel
"""

import argparse
import concurrent.futures
import time
from dataclasses import dataclass

import yaml

from login_check import LoginResult, attempt_login

# ---------------------------------------------------------------------------

RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"


@dataclass
class CheckResult:
    site:     str
    username: str
    result:   LoginResult
    elapsed:  float


def run_single(site: dict, login: dict) -> CheckResult:
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
        site     = site["name"],
        username = login["username"],
        result   = result,
        elapsed  = time.monotonic() - start,
    )


def print_report(results: list[CheckResult]) -> None:
    ok     = [r for r in results if r.result.status == "OK"]
    failed = [r for r in results if r.result.status != "OK"]

    width = 60
    print(f"\n{BOLD}{'═' * width}{RESET}")
    print(f"{BOLD}  LOGIN CHECK REPORT{RESET}")
    print(f"{BOLD}{'═' * width}{RESET}\n")

    # Group by site
    sites = dict.fromkeys(r.site for r in results)
    for site in sites:
        site_results = [r for r in results if r.site == site]
        print(f"{CYAN}{BOLD}  {site}{RESET}")
        for r in site_results:
            icon    = f"{GREEN}✓{RESET}" if r.result.status == "OK" else f"{RED}✗{RESET}"
            status  = f"{GREEN}OK{RESET}"     if r.result.status == "OK" else f"{RED}FAILED{RESET}"
            elapsed = f"{DIM}{r.elapsed:.1f}s{RESET}"
            print(f"    {icon}  {r.username:<20} {status:<10} {elapsed}")
            if r.result.status != "OK":
                print(f"       {DIM}↳ {r.result.detail}{RESET}")
        print()

    # Summary bar
    total = len(results)
    print(f"{BOLD}{'─' * width}{RESET}")
    print(
        f"  {BOLD}Total:{RESET} {total}  "
        f"{GREEN}{BOLD}{len(ok)} passed{RESET}  "
        f"{RED}{BOLD}{len(failed)} failed{RESET}"
    )
    print(f"{BOLD}{'═' * width}{RESET}\n")


def main() -> None:
    p = argparse.ArgumentParser(description="Multi-site login checker")
    p.add_argument("--config",   default="sites.yaml", help="Path to YAML config")
    p.add_argument("--parallel", action="store_true",  help="Run all checks concurrently")
    args = p.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    # Build flat list of (site, login) jobs
    jobs = [
        (site, login)
        for site in config["sites"]
        for login in site["logins"]
    ]

    print(f"\n{BOLD}Running {len(jobs)} login check(s) across {len(config['sites'])} site(s)...{RESET}\n")

    results: list[CheckResult] = []

    if args.parallel:
        with concurrent.futures.ThreadPoolExecutor() as ex:
            futures = {ex.submit(run_single, site, login): (site, login) for site, login in jobs}
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
    else:
        for site, login in jobs:
            print(f"  {DIM}Checking {site['name']} → {login['username']}...{RESET}")
            results.append(run_single(site, login))

    print_report(results)


if __name__ == "__main__":
    main()