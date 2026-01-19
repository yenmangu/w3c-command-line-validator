# w3c-validator

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

Clone the repository and install it into a virtual environment:

```bash
pip install -e .
```
