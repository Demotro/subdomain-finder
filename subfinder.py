import argparse
import json
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


WORDLIST_FILE = "wordlist.txt"


def resolve_ip(subdomain):
    try:
        ip_address = socket.gethostbyname(subdomain)
        return ip_address
    except socket.gaierror:
        return None


def check_http(subdomain):
    urls = [
        f"https://{subdomain}",
        f"http://{subdomain}"
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            return {
                "url": url,
                "status_code": response.status_code
            }
        except requests.exceptions.RequestException:
            continue

    return {
        "url": None,
        "status_code": None
    }


def scan_subdomain(domain, word):
    subdomain = f"{word}.{domain}"

    ip_address = resolve_ip(subdomain)

    if ip_address is None:
        return None

    http_result = check_http(subdomain)

    return {
        "subdomain": subdomain,
        "ip_address": ip_address,
        "http_url": http_result["url"],
        "status_code": http_result["status_code"]
    }


def load_wordlist():
    try:
        with open(WORDLIST_FILE, "r", encoding="utf-8") as file:
            words = file.read().splitlines()

    except FileNotFoundError:
        print(f"[ERROR] Wordlist file not found: {WORDLIST_FILE}")
        return None

    cleaned_words = []

    for word in words:
        word = word.strip()

        if word:
            cleaned_words.append(word)

    return cleaned_words


def find_subdomains(domain, threads):
    words = load_wordlist()

    if words is None:
        return None

    found_subdomains = []

    print("Subdomain Finder CLI")
    print("-----------------------------")
    print("Target domain:", domain)
    print("Wordlist:", WORDLIST_FILE)
    print("Threads:", threads)
    print()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_results = []

        for word in words:
            future = executor.submit(scan_subdomain, domain, word)
            future_results.append(future)

        for future in as_completed(future_results):
            result = future.result()

            if result:
                found_subdomains.append(result)

                print(f"[FOUND] {result['subdomain']}")
                print(f"  IP: {result['ip_address']}")

                if result["http_url"]:
                    print(f"  HTTP: {result['http_url']} ({result['status_code']})")
                else:
                    print("  HTTP: not available")

                print()

    found_subdomains.sort(key=lambda item: item["subdomain"])

    return {
        "target_domain": domain,
        "wordlist": WORDLIST_FILE,
        "threads": threads,
        "tested_count": len(words),
        "found_count": len(found_subdomains),
        "subdomains": found_subdomains
    }


def print_summary(result):
    if result is None:
        return

    print("-----------------------------")
    print("Scan finished")
    print("Tested subdomains:", result["tested_count"])
    print("Found subdomains:", result["found_count"])


def save_json_report(result, filename):
    if result is None:
        return

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print()
    print(f"[INFO] JSON report saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Subdomain finder CLI"
    )

    parser.add_argument(
        "domain",
        help="Target domain, for example example.com"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=10,
        help="Number of threads, default is 10"
    )

    parser.add_argument(
        "--json",
        help="Save scan result to a JSON file, for example report.json"
    )

    args = parser.parse_args()

    if args.threads < 1:
        print("[ERROR] Number of threads must be at least 1.")
        return

    result = find_subdomains(args.domain, args.threads)
    print_summary(result)

    if args.json:
        save_json_report(result, args.json)


if __name__ == "__main__":
    main()