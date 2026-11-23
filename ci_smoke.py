"""Minimal CI smoke check for the conference management app.

This is deliberately NOT a test suite. The project has no tests, and CI must not
pretend otherwise: this script only proves that the Flask application imports,
that every route defined in app.py is still reachable, and that its Jinja2
template renders without a database.

Exit code 0 = smoke check passed, 1 = at least one problem was found.
"""

import sys

from app import app

# Every GET route defined in app.py and the status code a plain GET must return.
EXPECTED_GET = {
    "/": 200,
    "/login": 200,
    "/signup": 200,
    "/contact": 200,
    "/services": 200,
    "/logout": 302,  # redirects to home()
    "/manage_bookings": 200,
    "/admin": 200,
    "/book": 200,
    "/dashboard": 200,
    "/about": 200,
}


def main():
    failures = []

    with app.test_client() as client:
        for route, expected in EXPECTED_GET.items():
            response = client.get(route)
            passed = response.status_code == expected
            status = "PASS" if passed else "FAIL"
            print("%s GET %s -> %s (expected %s)" % (status, route, response.status_code, expected))
            if not passed:
                failures.append(route)

    defined = {rule.rule for rule in app.url_map.iter_rules() if rule.endpoint != "static"}
    not_covered = sorted(defined - set(EXPECTED_GET))
    stale = sorted(set(EXPECTED_GET) - defined)

    if not_covered:
        print("FAIL routes defined in app.py but missing from this smoke check: %s" % not_covered)
        failures.append("<route-coverage>")
    if stale:
        print("FAIL routes checked here but no longer defined in app.py: %s" % stale)
        failures.append("<stale-route>")

    if failures:
        print("SMOKE CHECK FAILED: %d problem(s) -> %s" % (len(failures), failures))
        return 1

    print("SMOKE CHECK PASSED: %d routes rendered" % len(EXPECTED_GET))
    return 0


if __name__ == "__main__":
    sys.exit(main())
