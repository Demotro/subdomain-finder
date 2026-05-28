# Subdomain Finder CLI

A Python command-line tool for basic subdomain discovery using a wordlist, DNS resolution, HTTP/HTTPS checks, multithreading, and JSON report export.

## Features

- Finds subdomains using a wordlist
- Resolves IP addresses using DNS
- Checks HTTP and HTTPS availability
- Shows HTTP status codes
- Uses multithreading for faster scanning
- Supports custom thread count
- Exports results to a JSON report
- Handles missing wordlist files and invalid thread values

## Project Structure

```text
subdomain-finder/
├── subfinder.py
├── wordlist.txt
├── requirements.txt
├── README.md
└── report.json
```

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

On Windows:

```bash
py -m pip install -r requirements.txt
```

## Usage

Basic scan:

```bash
python subfinder.py github.com
```

On Windows:

```bash
py subfinder.py github.com
```

Scan with custom thread count:

```bash
py subfinder.py github.com --threads 20
```

Scan with JSON export:

```bash
py subfinder.py github.com --json report.json
```

## Example Output

```text
Subdomain Finder CLI
-----------------------------
Target domain: github.com
Wordlist: wordlist.txt
Threads: 10

[FOUND] api.github.com
  IP: 140.82.121.5
  HTTP: https://api.github.com (200)

-----------------------------
Scan finished
Tested subdomains: 18
Found subdomains: 9
```

## Example JSON Report

The tool can export scan results into a JSON file:

```bash
py subfinder.py github.com --json report.json
```

The report contains information such as the target domain, used wordlist, thread count, tested subdomains, found subdomains, IP addresses, HTTP/HTTPS availability, and status codes.

## Technologies Used

- Python
- requests
- argparse
- socket
- concurrent.futures
- JSON
- DNS resolution
- HTTP/HTTPS checks

## Disclaimer

This tool is intended for educational purposes and basic security learning only.