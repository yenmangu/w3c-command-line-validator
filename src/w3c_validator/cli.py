from __future__ import annotations
import argparse
import requests

W3C_NU_ENDPOINT = "https://validator.w3.org/nu/"


# 1. Prove the API works
def validate_one(url: str) -> int:
    response = requests.get(
        W3C_NU_ENDPOINT, params={"doc": url, "out": "json"}, timeout=30
    )

    # Raise HTTPError, if one occurs
    response.raise_for_status()

    # Parse the JSON into payload
    payload = response.json()

    # Get any and all messages from the payload
    messages = payload.get("messages", [])

    # Canonical way to count in python. Below is a generator function, the function yields a '1' for every message whose type is "error"
    # sum(result of generator function)
    error_count = sum(1 for m in messages if m.get("type") == "error")

    print(url)
    print(f"Errors: {error_count}")
    return error_count


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="w3c-validator",
        description="Validate deployed URLs using the W3C Nu HTML Checker (JSON output).",
    )

    parser.add_argument(
        "urls",
        nargs="+",
        help="One or more deployed URLs to validate.",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout im seconds (default: 30).",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    exit_code = 0

    for url in args.urls:
        error_count = validate_one(url)
        if error_count > 1:
            exit_code = 1
    return exit_code

    test_url = "https://example.com"

    # Exit code convention: 0 = success, non-zero = failure
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
