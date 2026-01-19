from __future__ import annotations
import argparse
import requests

W3C_NU_ENDPOINT = "https://validator.w3.org/nu/"


# 1. Prove the API works
def validate_one(url: str) -> int:
    """Validate a single deployed URL's markup
    Calls the W3C_NU_ENDPOINT with a GET request to validate the markup at the `url`

    Args:
        url (str): The deployed URL in question

    Returns:
        int: Number of errors
    """
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
    """Builds the command line argument parser.

    Returns:
        argparse.ArgumentParser: returns an instance of the ArgumentParser class
    """
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
        help="Request timeout in seconds (default: 30).",
    )
    return parser


# TODO: Add count_messages()
# TODO: Add print_error_messages()


# Standard entrypoint convention
def main() -> int:
    """Conventional entrypoint for program

    Returns:
        int: standard exit code convention - 0 = success; non-zero = Error
    """
    parser = build_arg_parser()
    args = parser.parse_args()

    exit_code = 0

    for url in args.urls:
        error_count = validate_one(url)
        if error_count > 1:
            exit_code = 1
    return exit_code


# Check code is not being run as part of an import
if __name__ == "__main__":
    raise SystemExit(main())
