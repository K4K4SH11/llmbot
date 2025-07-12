import os
from datetime import datetime
import re

def anonymize_data(text):
    # Remove PII (e.g., names, addresses)
    patterns = [
        r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",  # Names
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",  # IPs
        r"\b\d{4}-\d{2}-\d{2}\b"  # Dates
    ]
    for pattern in patterns:
        text = re.sub(pattern, "[REDACTED]", text)
    return text

def log_interaction(query, response, log_dir="src/gdpr_logs"):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{log_dir}/interactions.log", "a") as f:
        f.write(f"[{timestamp}] Query: {query} | Response: {response}\n")