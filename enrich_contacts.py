"""
Smart Website Finder using Google Search
Finds real clinic websites and emails by searching Google
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from urllib.parse import quote_plus, urlparse
import random

# User agents to rotate (appear more natural)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

# Sites to EXCLUDE (directories, not actual clinic sites)
EXCLUDE_DOMAINS = [
    'yelp.com', 'healthgrades.com', 'vitals.com', 'zocdoc.com',
    'psychologytoday.com', 'goodtherapy.org', 'facebook.com',
    'linkedin.com', 'twitter.com', 'instagram.com', 'yellowpages.com',
    'bbb.org', 'manta.com', 'whitepages.com', 'npidb.org',
    'npino.com', 'hipaaspace.com', 'medicare.gov'
]

# Delay between requests (seconds)
MIN_DELAY = 2
MAX_DELAY = 4


def google_search(query, num_results=5):
    """
    Search Google and return URLs.
    
    Args:
        query (str): Search query
        num_results (int): Number of results to return
    
    Returns:
        list: List of URLs found
    """
    
    # Build Google search URL
    search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results}"
    
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all search result links
            links = []
            for g in soup.find_all('div', class_='g'):
                anchors = g.find_all('a')
                for anchor in anchors:
                    if anchor.get('href'):
                        url = anchor['href']
                        if url.startswith('http'):
                            links.append(url)
            
            # Also try alternative parsing
            if not links:
                for a in soup.find_all('a', href=True):
                    url = a['href']
                    if '/url?q=' in url:
                        # Extract actual URL from Google redirect
                        actual_url = url.split('/url?q=')[1].split('&')[0]
                        if actual_url.startswith('http'):
                            links.append(actual_url)
            
            return links[:num_results]
        
        elif response.status_code == 429:
            print(" (rate limited)")
            return []
        else:
            return []
    
    except Exception as e:
        print(f" (error: {str(e)[:30]})")
        return []


def is_valid_clinic_website(url, clinic_name):
    """
    Check if URL is likely the actual clinic website.
    
    Args:
        url (str): URL to check
        clinic_name (str): Clinic name to match
    
    Returns:
        bool: True if likely the clinic's actual site
    """
    
    if not url:
        return False
    
    # Parse domain
    try:
        domain = urlparse(url).netloc.lower()
    except:
        return False
    
    # Exclude directory sites
    for exclude in EXCLUDE_DOMAINS:
        if exclude in domain:
            return False
    
    # Prefer .com, .org, .net domains
    if not any(domain.endswith(ext) for ext in ['.com', '.org', '.net', '.us', '.co']):
        return False
    
    return True


def find_clinic_website(clinic_name, city, state):
    """
    Find the actual website for a clinic using Google search.
    
    Args:
        clinic_name (str): Clinic name
        city (str): City
        state (str): State
    
    Returns:
        str: Website URL or empty string
    """
    
    # Build search query
    query = f"{clinic_name} {city} {state}"
    
    # Search Google
    results = google_search(query, num_results=5)
    
    if not results:
        # Try alternative query without LLC, Inc, etc.
        clean_name = re.sub(r'\b(LLC|Inc|PLLC|PC|Ltd)\b', '', clinic_name, flags=re.IGNORECASE).strip()
        query = f"{clean_name} {city} {state} therapy counseling"
        results = google_search(query, num_results=5)
    
    # Filter and return first valid result
    for url in results:
        if is_valid_clinic_website(url, clinic_name):
            return url
    
    return ""


def extract_emails_from_text(text):
    """Extract email addresses from text."""
    if not text:
        return []
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    # Filter out common non-contact emails
    exclude_patterns = ['example.com', 'test.com', 'yourdomain.com', '@sentry', '@google', '@facebook']
    filtered = [e for e in emails if not any(ex in e.lower() for ex in exclude_patterns)]
    
    return list(set(filtered))


def scrape_website_email(url):
    """
    Scrape email from website.
    
    Args:
        url (str): Website URL
    
    Returns:
        str: Email address or empty string
    """
    
    if not url:
        return ""
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get all text
            text = soup.get_text(separator=' ')
            
            # Find emails
            emails = extract_emails_from_text(text)
            
            # Also check mailto links
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('mailto:'):
                    email = link['href'].replace('mailto:', '').split('?')[0]
                    if '@' in email:
                        emails.append(email.lower())
            
            if emails:
                return emails[0]  # Return first email found
        
        return ""
    
    except:
        return ""


def enrich_with_google_search(csv_path, output_path=None, max_clinics=None, start_from=0):
    """
    Enrich clinic CSV with real websites and emails using Google search.
    
    Args:
        csv_path (str): Path to clinic CSV
        output_path (str): Output path (defaults to same file)
        max_clinics (int): Max clinics to process
        start_from (int): Start from this row (for resuming)
    """
    
    if output_path is None:
        output_path = csv_path
    
    print("\n" + "=" * 80)
    print("  SMART WEBSITE FINDER - Using Google Search")
    print("=" * 80)
    
    df = pd.read_csv(csv_path)
    
    # Add new columns if they don't exist
    if 'website' not in df.columns:
        df['website'] = ""
    if 'email' not in df.columns:
        df['email'] = ""
    if 'search_status' not in df.columns:
        df['search_status'] = ""
    
    total = len(df) if max_clinics is None else min(max_clinics, len(df) - start_from)
    
    print(f"\n📊 Processing {total} clinics...")
    print(f"⏱️  Estimated time: {total * 3 // 60} minutes (3 sec per clinic)")
    print(f"🔍 Starting from row {start_from}\n")
    
    found_websites = 0
    found_emails = 0
    
    for idx in range(start_from, min(start_from + total if max_clinics else len(df), len(df))):
        row = df.iloc[idx]
        
        clinic_name = row.get('clinic_name', 'Unknown')
        city = row.get('city', '')
        state = row.get('state', '')
        
        print(f"{idx+1}/{len(df)}: {clinic_name[:45]:45}", end=" ")
        
        # Find website
        website = find_clinic_website(clinic_name, city, state)
        
        if website:
            df.at[idx, 'website'] = website
            df.at[idx, 'search_status'] = 'Found website'
            found_websites += 1
            print(f"✅ {website[:40]}", end=" ")
            
            # Scrape email from website
            time.sleep(1)  # Small delay before scraping
            email = scrape_website_email(website)
            
            if email:
                df.at[idx, 'email'] = email
                df.at[idx, 'search_status'] = 'Found website & email'
                found_emails += 1
                print(f"📧 {email[:30]}")
            else:
                print("(no email)")
        else:
            df.at[idx, 'search_status'] = 'Website not found'
            print("❌ Not found")
        
        # Save progress every 10 clinics
        if (idx + 1) % 10 == 0:
            df.to_csv(output_path, index=False)
            print(f"\n💾 Progress saved ({idx+1} clinics processed)\n")
        
        # Random delay to avoid rate limiting
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)
    
    # Final save
    df.to_csv(output_path, index=False)
    
    print("\n" + "=" * 80)
    print("✅ ENRICHMENT COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Results:")
    print(f"  Websites found: {found_websites}/{total} ({found_websites/total*100:.1f}%)")
    print(f"  Emails found: {found_emails}/{total} ({found_emails/total*100:.1f}%)")
    print(f"\n📁 Saved to: {output_path}")
    print("=" * 80 + "\n")


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        max_to_process = int(sys.argv[2]) if len(sys.argv) > 2 else None
        start_from = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    else:
        csv_file = "il_behavioral_health_clinics.csv"
        max_to_process = 10  # Test with 10 first
        start_from = 0
    
    print(f"\n🔍 Finding real websites via Google search...")
    print(f"   Test run: {max_to_process or 'all'} clinics\n")
    
    enrich_with_google_search(csv_file, max_clinics=max_to_process, start_from=start_from)
