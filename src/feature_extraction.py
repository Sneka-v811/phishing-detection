"""
feature_extraction.py
---------------------
This module extracts structural, lexical, and domain-based features from a given URL.
These numerical features will be used by our Machine Learning model to classify
a website as Phishing (1) or Legitimate (0).
"""

import re
import ipaddress
from urllib.parse import urlparse


def extract_features(url: str) -> dict:
    """
    Extracts 8 key features from a URL string.

    Parameters:
        url (str): The web address to analyze (e.g., "http://login.secure-bank.com/verify").

    Returns:
        dict: A dictionary of extracted features with feature names as keys
              and binary/numeric values.
    """
    # Standardize URL format if scheme is missing
    if not url.startswith(("http://", "https://")):
        url_to_parse = "http://" + url
    else:
        url_to_parse = url

    # Parse URL components using standard urllib
    parsed_url = urlparse(url_to_parse)
    hostname = parsed_url.hostname or ""

    # 1. Feature: URL length
    # Phishing URLs are often unnaturally long to hide suspicious parameters
    url_length = len(url)

    # 2. Feature: Number of dots in the URL
    # Phishing links often use multiple dots (e.g., paypal.com.attacker.com)
    num_dots = url.count(".")

    # 3. Feature: Presence of '@' symbol
    # The '@' symbol leads browsers to ignore everything preceding it
    having_at_symbol = 1 if "@" in url else 0

    # 4. Feature: Presence of '-' (dash) in domain name
    # Attackers frequently use dashes to impersonate brands (e.g., paypal-security.com)
    prefix_suffix_in_domain = 1 if "-" in hostname else 0

    # 5. Feature: Whether the URL uses HTTPS
    # Legitimate sites mostly use encrypted HTTPS connections
    uses_https = 1 if parsed_url.scheme.lower() == "https" else 0

    # 6. Feature: Whether domain is an IP address instead of a domain name
    # Using an IP directly (e.g., http://192.168.1.1/login) is typical of phishing
    is_ip = 0
    if hostname:
        try:
            ipaddress.ip_address(hostname)
            is_ip = 1
        except ValueError:
            # Check for hex/octal or regex-based IPv4 fallback
            ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
            if re.match(ipv4_pattern, hostname):
                is_ip = 1

    # 7. Feature: Number of subdomains
    # Deeply nested subdomains (e.g., login.verify.account.bank.com) indicate phishing
    num_subdomains = 0
    if hostname and not is_ip:
        parts = hostname.split(".")
        # A normal domain like "google.com" has 2 parts (subdomains = 0)
        # "sub.google.com" has 3 parts (subdomains = 1)
        if len(parts) > 2:
            num_subdomains = len(parts) - 2

    # 8. Feature: Presence of suspicious keywords
    # Words commonly seen in phishing links seeking credentials or verification
    suspicious_keywords = ["login", "verify", "secure", "account", "update", "banking", "signin", "confirm"]
    url_lower = url.lower()
    has_suspicious_keyword = 1 if any(keyword in url_lower for keyword in suspicious_keywords) else 0

    # Bundle all features into a structured dictionary
    features = {
        "url_length": url_length,
        "num_dots": num_dots,
        "having_at_symbol": having_at_symbol,
        "prefix_suffix_in_domain": prefix_suffix_in_domain,
        "uses_https": uses_https,
        "is_ip": is_ip,
        "num_subdomains": num_subdomains,
        "has_suspicious_keyword": has_suspicious_keyword,
    }

    return features


# Simple execution block to test feature extraction locally
if __name__ == "__main__":
    sample_urls = [
        "https://www.google.com",
        "http://192.168.1.100/login/verify-account",
        "http://secure-login.paypal.com.attacker-site.org/update",
    ]

    print("--- Phishing Detection Feature Extractor Test ---\n")
    for sample in sample_urls:
        print(f"URL: {sample}")
        extracted = extract_features(sample)
        for feature_name, value in extracted.items():
            print(f"  - {feature_name}: {value}")
        print("-" * 50)
