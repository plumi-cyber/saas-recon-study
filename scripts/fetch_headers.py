"""
Fetch HTTP security headers from a URL.

Passive observation only: makes one GET request, reads the response headers,
and prints them. No probing, no authentication, no follow-up requests.

Usage:
    python scripts/fetch_headers.py <url>

Example:
    python scripts/fetch_headers.py https://example.com
"""

import sys
import requests


def fetch_headers(url: str) -> None:
    """Make a single GET request and print the response headers."""
    response = requests.get(url, allow_redirects=True, timeout=10)
    print(f"Final URL: {response.url}")
    print(f"Status:    {response.status_code}")
    print()
    print("Headers:")
    for header_name, header_value in response.headers.items():
        print(f"  {header_name}: {header_value}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_headers.py <url>")
        sys.exit(1)
    target_url = sys.argv[1]
    fetch_headers(target_url)
