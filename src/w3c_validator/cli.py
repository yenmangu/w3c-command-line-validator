from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Any

import requests

W3C_NU_ENDPOINT = "https://validator.w3.org/nu/"


@dataclass
class MessageCounts:
    """Lightweight dataclass, with dunders generated automatically
    through the use of `@dataclass`
    """

    errors: int
    infos: int
    non_document_errors: int


def fetch_validation_json(
    document_url: str,
    *,
    timeout_seconds: int,
) -> dict[str, Any]:
    """Make the single request for a single URL

    Args:
        document_url (str): The URL to validate
        timeout_seconds (int): Number of seconds allowed before timeout

    Returns:
        dict[str, Any]: Parsed JSON Response object
    """
    response = requests.get(
        W3C_NU_ENDPOINT,
        params={
            "doc": document_url,
            "out": "json",
        },
        timeout=timeout_seconds,
        headers={
            "User-Agent": "w3c-nu-validator-client/1.0",
        },
    )
    response.raise_for_status()
    return response.json()


def count_messages(payload: dict[str, Any]) -> MessageCounts:
    messages = payload.get("messages", [])

    error_count = 0
    info_count = 0
    non_doc_count = 0

    for m in messages:
        m_type = m.get("type", "info")
        if m_type == "error":
            error_count += 1
        elif m_type == "non-document-error":
            non_doc_count += 1
        else:
            info_count += 1

    return MessageCounts(
        errors=error_count,
        infos=info_count,
        non_document_errors=non_doc_count,
    )


def get_location(
    message: dict[str, Any],
) -> tuple[
    int | None,
    int | None,
    int | None,
    int | None,
]:
    """Access various error location points using keys in message dict.
    Each access has fallback.

    Tuple chosen as return as data is temporary, positional and immediately unpacked.

    Args:
        message (dict[str, Any]): Message from validation response

    Returns:
        tuple[ int | None, int | None, int | None, int | None, ]: Tuple containing all 4 location pooints.
    """
    first_line = message.get("firstLine") or message.get("line")
    last_line = message.get("lastLine") or message.get("line")

    first_col = message.get("firstColumn") or message.get("column")
    last_col = message.get("lastColumn") or message.get("column")

    return first_line, last_line, first_col, last_col


def collapse_blank_lines(text: str) -> str:
    """Collapse multiple consecutive blank lines into a single blank line
    Preserves indentation and non empty lines

    Args:
        text (str): Input HTML extract

    Returns:
        str: HTML extract with empty blank lines collapsed
    """

    lines = text.splitlines()

    normalised_lines: list[str] = []

    for line in lines:
        is_blank = not line.strip()

        if is_blank:
            continue

        normalised_lines.append(line.rstrip())

    return "\n".join(normalised_lines)


def print_error_messages(payload: dict[str, Any]) -> None:
    """Read and print any error messages from the parsed response JSON payload.
    Downstream expects an iterable, so default from get() is empty list.

    Args:
        payload (dict[str,Any]): Parsed JSON payload
    """
    # print(f"payload: ", payload)
    messages = payload.get("messages", [])

    # print(messages)

    # Iterate over messages, skipping non error messages
    for m in messages:
        # print(f"Type: {m.get("type")}")
        if m.get("type") != "error":
            continue

        (
            first_line,
            last_line,
            first_col,
            last_col,
        ) = get_location(m)

        text = (m.get("message") or "").strip()

        # Use blank lines helper
        raw_extract = m.get("extract") or ""
        extract = collapse_blank_lines(raw_extract).strip()
        # extract = (m.get("extract") or "").strip()

        line_column_coordinates: list[str] = []
        if first_line is not None and last_line is not None:
            if first_line == last_line:
                line_column_coordinates.append(f"line {last_line}")
            else:
                line_column_coordinates.append(f"lines {first_line}-{last_line}")
        elif last_line is not None:
            line_column_coordinates.append(f"line {last_line}")

        if first_col is not None and last_col is not None:
            if first_col == last_col:
                line_column_coordinates.append(f"column: {last_col}")
            else:
                line_column_coordinates.append(f"columns {first_col}-{last_col}")
        elif last_col is not None:
            line_column_coordinates.append(f"column: {last_col}")

        location = (
            f" ({', '.join(line_column_coordinates)})"
            if line_column_coordinates
            else ""
        )
        print(f"    - ERROR{location}: {text}")

        if extract:
            print(f"      Extract:\n{extract}\n")

    # TODO: Location helper, refactor to use location helper


# 1. Prove the API works
def validate_one(url: str, *, timeout_seconds: int) -> int:
    """Validate a single deployed URL's markup
    Calls the W3C_NU_ENDPOINT with a GET request to validate the markup at the `url`

    Args:
        url (str): The deployed URL in question

    Returns:
        int: Number of errors
    """

    payload = fetch_validation_json(url, timeout_seconds=timeout_seconds)
    counts = count_messages(payload)

    # print(f"counts {counts}")

    print(url)
    print(
        f"  Errors: {counts.errors} | "
        f"Info/Warnings: {counts.infos} | "
        f"Non-doc: {counts.non_document_errors}"
    )

    if counts.errors:
        print_error_messages(payload)

    return 1 if counts.errors else 0


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
        url_exit = validate_one(url, timeout_seconds=args.timeout)
        exit_code = max(exit_code, url_exit)

    return exit_code


# Check code is not being run as part of an import
if __name__ == "__main__":
    raise SystemExit(main())
