# Subdomain Finder CLI

A Python command-line tool for subdomain discovery using a wordlist, DNS resolution, HTTP/HTTPS availability checks, multithreaded scanning and JSON report export.

The project tests common subdomain names against a target domain, resolves discovered subdomains to IP addresses, checks whether they are reachable over HTTPS or HTTP, and saves scan results into a structured JSON report.

## Highlights

- Clean single-file CLI implementation
- Wordlist-based subdomain discovery
- DNS resolution using Python sockets
- HTTPS-first availability checking
- HTTP fallback when HTTPS is unavailable
- HTTP status code detection
- Multithreaded scanning for faster execution
- Configurable thread count
- JSON report export
- Input validation and error handling

## Features

- Load subdomain names from `wordlist.txt`
- Generate possible subdomains from a target domain
- Resolve discovered subdomains to IP addresses
- Check HTTPS availability first
- Fall back to HTTP if HTTPS is not available
- Display discovered subdomains in the terminal
- Show resolved IP addresses
- Show reachable URLs and HTTP status codes
- Handle DNS resolution failures
- Handle unavailable HTTP/HTTPS services
- Use a 5-second timeout for HTTP requests
- Export scan results into a JSON report
- Sort discovered subdomains alphabetically in the final result

## Technologies

- Python
- requests
- argparse
- socket
- concurrent.futures
- JSON

## Project Structure

```text
subdomain-finder/
├── subfinder.py
├── wordlist.txt
├── requirements.txt
├── README.md
└── report.json
```

## Files

- `subfinder.py` - main CLI tool, DNS resolving, HTTP checks, multithreading and JSON export
- `wordlist.txt` - list of subdomain names used for discovery
- `requirements.txt` - project dependencies
- `README.md` - project documentation
- `report.json` - example JSON scan report

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

On Windows:

```bash
py -m pip install -r requirements.txt
```

## How It Works

The tool uses a wordlist to generate possible subdomains for a target domain.

Example:

```text
api + github.com = api.github.com
```

For each generated subdomain, the tool:

- tries to resolve the subdomain to an IP address using DNS
- skips the subdomain if DNS resolution fails
- checks whether the resolved subdomain is available over HTTPS
- falls back to HTTP if HTTPS is not available
- records the reachable URL and HTTP status code
- stores discovered subdomains in the final result

The scan is executed using multiple threads to make the discovery process faster.

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
  IP: 140.82.121.6
  HTTP: https://api.github.com (200)

[FOUND] docs.github.com
  IP: 185.199.108.154
  HTTP: https://docs.github.com (200)

-----------------------------
Scan finished
Tested subdomains: 18
Found subdomains: 9
```

## JSON Report

The tool can export scan results into a JSON file.

Example command:

```bash
py subfinder.py github.com --json report.json
```

The report includes:

- target domain
- used wordlist
- thread count
- tested subdomain count
- found subdomain count
- discovered subdomains
- resolved IP addresses
- reachable HTTP/HTTPS URLs
- HTTP status codes

Example JSON structure:

```json
{
    "target_domain": "github.com",
    "wordlist": "wordlist.txt",
    "threads": 10,
    "tested_count": 18,
    "found_count": 9,
    "subdomains": [
        {
            "subdomain": "api.github.com",
            "ip_address": "140.82.121.6",
            "http_url": "https://api.github.com",
            "status_code": 200
        }
    ]
}
```

## Error Handling

The tool handles common error situations such as:

- missing `wordlist.txt` file
- invalid thread count
- DNS resolution failures
- unavailable HTTP/HTTPS services
- request timeouts
- connection errors

If a subdomain resolves successfully but does not respond over HTTP or HTTPS, it is still included in the results with empty HTTP information.

## Disclaimer

This tool is intended for educational purposes and security learning only.