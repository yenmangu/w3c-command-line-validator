# w3c-nu-validator

A lightweight Python CLI tool for validating **deployed URLs** using the
**W3C Nu HTML Checker HTTP API** (JSON output).

This tool is designed to validate the HTML that users and assessors actually see
in production, rather than local templates or development builds.

---

## Why this exists

Manual HTML validation via copy-pasting URLs into the W3C validator is:

- slow
- repetitive
- error-prone
- difficult to repeat consistently across many pages

This tool allows you to:

- validate many deployed URLs in one run
- capture a complete, site-wide validation report
- fix issues systematically instead of page-by-page

---

## Features

- Validate one or more deployed URLs
- Read URLs from a file (one per line)
- De-duplicate URLs automatically
- Write a full validation report to disk
- Return a meaningful exit code (useful for scripts / CI)
- Uses the official W3C Nu Validator HTTP interface

---

## Installation

### From PyPI

```bash
pip install w3c-nu-validator
```

This installs the `w3c-nu-validator` command.

---

### Editable Install

Clone the repository and install it into a virtual environment.

```bash
pip install -e .
```

Or install from another project in editable mode:

```bash
pip install -e /path/to/w3c-nu-validator
```

---

## Usage

### Validate one or more URLs

```bash
w3c-nu-validator https://example.com https://example.com/about/
```

---

### Read URLs from a file

```bash
w3c-nu-validator -r urls.txt
```

File rules:

- one URL per line
- blank lines are ignored
- lines starting with # are ignored

Example `urls.txt`:

> [!NOTE]
> Lines beginning with hash `#` marks are treated as comments and thus ignored.

```text
# Home page
https://example.com/

# Resource list
https://example.com/resources/
```

---

### Write a full report to a file

```bash
w3c-nu-validator -r urls.txt -o report.txt
```

The report includes:

- a delimiter per URL
- error / info counts
- full error messages with HTML extracts

---

## Exit codes

| Code | Meaning                                             |
| ---: | --------------------------------------------------- |
|    0 | No validation errors found                          |
|    1 | One or more URLs contain validation errors          |
|    2 | Invalid input (missing URLs, unreadable file, etc.) |

This allows quick pass/fail checks:

```bash
w3c-nu-validator -r urls.txt
echo $?
```

---

## Requirements

- Python 3.10+
- `requests`

---

## Licence

MIT Licence.

This project is provided as-is, without warranty.
See the `LICENSE` file for details.
