"""
Contact Validator for Velden Health RCM
Validates website URLs and email addresses to ensure outreach quality
"""

import requests
import dns.resolver
import socket
from urllib.parse import urlparse
import time

# Timeout settings
HTTP_TIMEOUT = 5
DNS_TIMEOUT = 3


def validate_website(url):
    """
    Check if website exists and is reachable.
    
    Args:
        url (str): Website URL (e.g., "www.example.com" or "http://example.com")
    
    Returns:
        dict: {"status": "verified|warning|invalid", "message": str}
    """
    if not url or len(url) < 5:
        return {"status": "invalid", "message": "No website"}
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        test_url = f"https://{url}"
    else:
        test_url = url
    
    try:
        # Try HTTPS first
        response = requests.head(test_url, timeout=HTTP_TIMEOUT, allow_redirects=True)
        if response.status_code < 400:
            return {"status": "verified", "message": "Website active"}
        
        # Try HTTP if HTTPS fails
        if test_url.startswith('https://'):
            test_url = test_url.replace('https://', 'http://')
            response = requests.head(test_url, timeout=HTTP_TIMEOUT, allow_redirects=True)
            if response.status_code < 400:
                return {"status": "warning", "message": "HTTP only (no HTTPS)"}
        
        return {"status": "invalid", "message": f"Status {response.status_code}"}
    
    except requests.exceptions.SSLError:
        return {"status": "warning", "message": "SSL certificate issue"}
    except requests.exceptions.Timeout:
        return {"status": "warning", "message": "Timeout - may be slow"}
    except requests.exceptions.ConnectionError:
        return {"status": "invalid", "message": "Cannot connect"}
    except Exception as e:
        return {"status": "warning", "message": "Needs manual check"}


def validate_email_domain(email):
    """
    Validate email address domain has valid MX records.
    
    Args:
        email (str): Email address (e.g., "contact@example.com")
    
    Returns:
        dict: {"status": "verified|warning|invalid", "message": str}
    """
    if not email or '@' not in email:
        return {"status": "invalid", "message": "No email"}
    
    try:
        domain = email.split('@')[1]
        
        # Check MX records
        mx_records = dns.resolver.resolve(domain, 'MX', lifetime=DNS_TIMEOUT)
        if mx_records:
            return {"status": "verified", "message": "Valid email domain"}
    
    except dns.resolver.NXDOMAIN:
        return {"status": "invalid", "message": "Domain doesn't exist"}
    except dns.resolver.NoAnswer:
        return {"status": "warning", "message": "No MX records"}
    except dns.resolver.Timeout:
        return {"status": "warning", "message": "DNS timeout"}
    except Exception as e:
        return {"status": "warning", "message": "Needs manual check"}
    
    return {"status": "warning", "message": "Unknown"}


def validate_contact(website, email):
    """
    Validate both website and email for a clinic.
    
    Args:
        website (str): Website URL
        email (str): Email address
    
    Returns:
        dict: {
            "website_status": str,
            "website_message": str,
            "email_status": str,
            "email_message": str,
            "overall_status": str
        }
    """
    web_result = validate_website(website)
    email_result = validate_email_domain(email)
    
    # Determine overall status
    statuses = [web_result["status"], email_result["status"]]
    if all(s == "verified" for s in statuses):
        overall = "verified"
    elif any(s == "invalid" for s in statuses):
        overall = "partial"
    else:
        overall = "warning"
    
    return {
        "website_status": web_result["status"],
        "website_message": web_result["message"],
        "email_status": email_result["status"],
        "email_message": email_result["message"],
        "overall_status": overall
    }


# Status icons for display
STATUS_ICONS = {
    "verified": "✅",
    "warning": "⚠️",
    "invalid": "❌",
    "partial": "⚠️"
}


def get_status_icon(status):
    """Get emoji icon for status."""
    return STATUS_ICONS.get(status, "❓")


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CONTACT VALIDATOR - TEST")
    print("=" * 80)
    
    test_cases = [
        ("www.google.com", "test@google.com"),
        ("www.thisdoesnotexist12345.com", "invalid@baddomain999.com"),
        ("", ""),
    ]
    
    for website, email in test_cases:
        print(f"\nTesting: {website} | {email}")
        result = validate_contact(website, email)
        print(f"  Website: {get_status_icon(result['website_status'])} {result['website_message']}")
        print(f"  Email: {get_status_icon(result['email_status'])} {result['email_message']}")
        print(f"  Overall: {get_status_icon(result['overall_status'])}")
        time.sleep(0.5)  # Rate limiting
    
    print("\n" + "=" * 80 + "\n")
