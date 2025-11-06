import re

# Sample text
text = """
Visit our website at https://www.flipkart.com or http://example.org for more info.
Our server IPs are 192.168.1.1 and 10.0.0.5.
Meeting dates: 12/09/2025, 2025-11-04, 01-01-24.
Employee PAN numbers: ABCDE1234F, AAAAA9999Z, XY12Z5678Q (invalid).
"""

# Regular expressions for each pattern
url_pattern = r'(https?://[^\s]+)'
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
date_pattern = r'\b(?:\d{2}[/-]\d{2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})\b'
pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'

# Finding matches
urls = re.findall(url_pattern, text)
ips = re.findall(ip_pattern, text)
dates = re.findall(date_pattern, text)
pans = re.findall(pan_pattern, text)

# Displaying results
print("✅ URLs Found:", urls)
print("✅ IP Addresses Found:", ips)
print("✅ Dates Found:", dates)
print("✅ PAN Numbers Found:", pans)
