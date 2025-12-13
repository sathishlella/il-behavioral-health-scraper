"""
Website Contact Scraper for Velden Health RCM
Extracts real emails and phone numbers from clinic websites
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time
import pandas as pd

# Timeout and retry settings
REQUEST_TIMEOUT = 10
MAX_RETRIES = 2
DELAY_BETWEEN_REQUESTS = 1  # Be polite to servers


def extract_emails_from_text(text):
    """Extract email addresses from text using regex."""
    if not text:
        return []
    
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    # Filter out common non-contact emails
    exclude_patterns = ['example.com', 'test.com', 'yourdomain.com', '@sentry', '@google', '@facebook']
    filtered = [e for e in emails if not any(ex in e.lower() for ex in exclude_patterns)]
    
    return list(set(filtered))  # Remove duplicates


def extract_phones_from_text(text):
    """Extract phone numbers from text using regex."""
    if not text:
        return []
    
    # Phone regex patterns (US format)
    patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890 or 123-456-7890
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',          # 123.456.7890
        r'\d{10}',                                # 1234567890
    ]
    
    phones = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        phones.extend(found)
    
    # Clean and format
    cleaned = []
    for phone in phones:
        # Remove non-digits
        digits = re.sub(r'\D', '', phone)
        # Must be 10 digits
        if len(digits) == 10:
            formatted = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            cleaned.append(formatted)
    
    return list(set(cleaned))  # Remove duplicates


def scrape_website_contacts(url, max_pages=3):
    """
    Scrape a website for contact information.
    
    Args:
        url (str): Website URL
        max_pages (int): Maximum pages to check (homepage + contact pages)
    
    Returns:
        dict: {
            'emails': list of emails found,
            'phones': list of phones found,
            'success': bool,
            'error': str or None
        }
    """
    
    if not url or len(url) < 5:
        return {'emails': [], 'phones': [], 'success': False, 'error': 'No URL'}
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    all_emails = []
    all_phones = []
    
    try:
        # Pages to check (in priority order)
        pages_to_check = [
            url,  # Homepage
            urljoin(url, '/contact'),
            urljoin(url, '/contact-us'),
            urljoin(url, '/about'),
        ]
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        pages_checked = 0
        for page_url in pages_to_check[:max_pages]:
            if pages_checked >= max_pages:
                break
            
            try:
                response = session.get(page_url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract from visible text
                    text = soup.get_text(separator=' ')
                    
                    # Find emails
                    emails = extract_emails_from_text(text)
                    all_emails.extend(emails)
                    
                    # Find phones
                    phones = extract_phones_from_text(text)
                    all_phones.extend(phones)
                    
                    # Also check mailto links
                    for link in soup.find_all('a', href=True):
                        if link['href'].startswith('mailto:'):
                            email = link['href'].replace('mailto:', '').split('?')[0]
                            if '@' in email:
                                all_emails.append(email.lower())
                    
                    # Also check tel links
                    for link in soup.find_all('a', href=True):
                        if link['href'].startswith('tel:'):
                            phone_text = link['href'].replace('tel:', '').strip()
                            phones = extract_phones_from_text(phone_text)
                            all_phones.extend(phones)
                    
                    pages_checked += 1
                    time.sleep(0.5)  # Small delay between pages
                
            except Exception as e:
                # Continue to next page if this one fails
                continue
        
        # Remove duplicates and clean
        unique_emails = list(set([e.lower() for e in all_emails]))
        unique_phones = list(set(all_phones))
        
        return {
            'emails': unique_emails[:3],  # Return top 3
            'phones': unique_phones[:2],  # Return top 2
            'success': len(unique_emails) > 0 or len(unique_phones) > 0,
            'error': None
        }
    
    except requests.exceptions.Timeout:
        return {'emails': [], 'phones': [], 'success': False, 'error': 'Timeout'}
    except requests.exceptions.ConnectionError:
        return {'emails': [], 'phones': [], 'success': False, 'error': 'Connection failed'}
    except Exception as e:
        return {'emails': [], 'phones': [], 'success': False, 'error': str(e)[:50]}


def enrich_clinic_contacts(csv_path, output_path=None, max_clinics=None):
    """
    Enrich clinic CSV with actual website contacts.
    
    Args:
        csv_path (str): Path to clinic CSV
        output_path (str): Output path (defaults to same file)
        max_clinics (int): Max clinics to process (None = all)
    """
    
    if output_path is None:
        output_path = csv_path
    
    print("\n" + "=" * 80)
    print("WEBSITE CONTACT ENRICHMENT")
    print("=" * 80)
    
    df = pd.read_csv(csv_path)
    
    if 'website' not in df.columns:
        print("❌ No 'website' column found in CSV")
        return
    
    # Add new columns
    df['email_actual'] = ""
    df['phone_actual'] = ""
    df['scrape_status'] = ""
    
    total = len(df) if max_clinics is None else min(max_clinics, len(df))
    
    print(f"\n📊 Processing {total} clinics...")
    print(f"⏱️  Estimated time: {total * 3 // 60} minutes\n")
    
    for idx, row in df.iterrows():
        if max_clinics and idx >= max_clinics:
            break
        
        website = row.get('website', '')
        clinic_name = row.get('clinic_name', 'Unknown')
        
        print(f"{idx+1}/{total}: {clinic_name[:40]:40}", end=" ")
        
        if not website or len(website) < 5:
            print("⏭️  No website")
            df.at[idx, 'scrape_status'] = 'No website'
            continue
        
        # Scrape website
        result = scrape_website_contacts(website)
        
        if result['success']:
            # Update with found contacts
            if result['emails']:
                df.at[idx, 'email_actual'] = result['emails'][0]
                print(f"✅ Email: {result['emails'][0][:30]}", end=" ")
            
            if result['phones']:
                df.at[idx, 'phone_actual'] = result['phones'][0]
                print(f"📞 Phone: {result['phones'][0]}", end="")
            
            df.at[idx, 'scrape_status'] = 'Success'
            print()
        else:
            print(f"❌ {result['error']}")
            df.at[idx, 'scrape_status'] = result['error'] or 'Failed'
        
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Be polite
    
    # Save
    df.to_csv(output_path, index=False)
    
    print("\n" + "=" * 80)
    print(f"✅ Enrichment complete!")
    print(f"📁 Saved to: {output_path}")
    print("\n📊 Results:")
    print(f"  Emails found: {(df['email_actual'] != '').sum()}")
    print(f"  Phones found: {(df['phone_actual'] != '').sum()}")
    print(f"  Success rate: {(df['scrape_status'] == 'Success').sum() / total * 100:.1f}%")
    print("=" * 80 + "\n")


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        max_to_process = int(sys.argv[2]) if len(sys.argv) > 2 else None
    else:
        csv_file = "il_behavioral_health_clinics.csv"
        max_to_process = 10  # Test with 10 first
    
    print(f"\n🔍 Testing with {max_to_process or 'all'} clinics from {csv_file}\n")
    
    enrich_clinic_contacts(csv_file, max_clinics=max_to_process)
