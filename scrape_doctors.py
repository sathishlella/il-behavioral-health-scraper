"""
Illinois Behavioral Health Individual Doctors Scraper
Fetches individual practitioners (psychiatrists, psychologists, counselors, etc.)
"""

import requests
import pandas as pd
import re
import time

NPI_URL = "https://npiregistry.cms.hhs.gov/api/"

def fetch(state, taxonomy, skip=0):
    """Fetch NPI data."""
    params = {
        "version": "2.1",
        "state": state,
        "taxonomy_description": taxonomy,
        "enumeration_type": "NPI-1",  # INDIVIDUALS only
        "limit": 200,
        "skip": skip
    }
    try:
        r = requests.get(NPI_URL, params=params, timeout=30)
        return r.json()
    except:
        return {"result_count": 0, "results": []}

def extract_credentials(name, taxonomies):
    """Extract professional credentials."""
    # Common credentials
    creds = []
    name_upper = name.upper()
    
    if "MD" in name_upper or "M.D." in name_upper:
        creds.append("MD")
    if "DO" in name_upper or "D.O." in name_upper:
        creds.append("DO")
    if "PHD" in name_upper or "PH.D." in name_upper or "PH D" in name_upper:
        creds.append("PhD")
    if "PSYD" in name_upper or "PSY.D." in name_upper:
        creds.append("PsyD")
    if "LCSW" in name_upper:
        creds.append("LCSW")
    if "LCPC" in name_upper:
        creds.append("LCPC")
    if "LPC" in name_upper and "LCPC" not in name_upper:
        creds.append("LPC")
    if "LMFT" in name_upper:
        creds.append("LMFT")
    
    # From taxonomy
    for tax in taxonomies:
        desc = (tax.get("desc", "") or "").lower()
        if "psychiatr" in desc and not any(c in ["MD", "DO"] for c in creds):
            creds.append("MD")
        if "psychologist" in desc and not any(c in ["PhD", "PsyD"] for c in creds):
            creds.append("PhD")
    
    return ", ".join(creds) if creds else "Licensed Professional"

def determine_practice_type(taxonomies, org_name):
    """Determine if solo or group practice."""
    # Check if affiliated with organization
    if org_name and len(org_name) > 5:
        if any(word in org_name.lower() for word in ["group", "associates", "partners", "center", "clinic", "&"]):
            return "Group Practice"
    
    return "Solo Practice"

def extract_doctor(r):
    """Extract doctor data from NPI record."""
    basic = r.get("basic", {})
    
    # Get name
    first = basic.get("first_name", "")
    last = basic.get("last_name", "")
    middle = basic.get("middle_name", "")
    
    if middle:
        full_name = f"{first} {middle} {last}"
    else:
        full_name = f"{first} {last}"
    
    full_name = full_name.strip()
    
    if not full_name or len(full_name) < 3:
        return None
    
    # Get address
    addrs = r.get("addresses", [])
    addr = next((a for a in addrs if a.get("address_purpose") == "LOCATION"), addrs[0] if addrs else None)
    
    if not addr:
        return None
    
    # Get taxonomies
    taxs = r.get("taxonomies", [])
    if not taxs:
        return None
    
    # Check if behavioral health
    tax_str = " ".join([t.get("desc", "") or "" for t in taxs]).lower()
    if not any(word in tax_str for word in ["mental", "behavior", "psychiatr", "psycholog", "counselor", "counseling", "social work", "substance", "addiction"]):
        return None
    
    # Get specialty
    primary_tax = taxs[0] if taxs else {}
    specialty = primary_tax.get("desc", "Behavioral Health") or "Behavioral Health"
    
    # Extract credentials
    credentials = extract_credentials(full_name, taxs)
    
    # Organization affiliation
    org_name = basic.get("organization_name", "")
    practice_type = determine_practice_type(taxs, org_name)
    
    # Billing prediction
    if practice_type == "Solo Practice":
        if "psychiatr" in tax_str or "physician" in tax_str:
            billing = "High"
        else:
            billing = "Medium"
    else:
        billing = "Medium"
    
    # Format phone
    phone = addr.get("telephone_number", "")
    if phone:
        d = re.sub(r'\D', '', phone)
        if len(d) == 10:
            phone = f"({d[:3]}) {d[3:6]}-{d[6:]}"
    
    return {
        "doctor_name": full_name,
        "credentials": credentials,
        "specialty": specialty,
        "practice_type": practice_type,
        "organization": org_name or "Independent",
        "address": (addr.get("address_1", "") + " " + addr.get("address_2", "")).strip(),
        "city": addr.get("city", ""),
        "state": addr.get("state", ""),
        "postal_code": (addr.get("postal_code", "") or "")[:5],
        "phone": phone,
        "billing_prediction": billing,
        "npi": r.get("number", "")
    }

print("\n" + "=" * 80)
print("ILLINOIS BEHAVIORAL HEALTH INDIVIDUAL DOCTORS SCRAPER")
print("=" * 80)
print("\nSearching for individual practitioners in Illinois...\n")

all_results = []
npi_set = set()

# Search by specialty - ILLINOIS ONLY
STATE = "IL"
specialties = [
    "psychiatry",
    "psychology", 
    "clinical social work",
    "mental health counseling",
    "substance abuse counseling",
    "behavioral health",
]

for specialty in specialties:
    print(f"Specialty: '{specialty}'...", end=" ")
    data = fetch(STATE, specialty)
    count = data.get("result_count", 0)
    print(f"{count} results")
    
    for r in data.get("results", []):
        npi = r.get("number")
        if npi and npi not in npi_set:
            all_results.append(r)
            npi_set.add(npi)
    
    # Get more pages (up to 5 per specialty)
    if count > 200:
        for p in range(1, min(5, count // 200 + 1)):
            print(f"  Page {p+1}...", end=" ")
            data = fetch(STATE, specialty, skip=p*200)
            print(f"{len(data.get('results', []))} records")
            
            for r in data.get("results", []):
                npi = r.get("number")
                if npi and npi not in npi_set:
                    all_results.append(r)
                    npi_set.add(npi)
            time.sleep(0.3)

print(f"\n✅ Total unique records: {len(all_results)}")
print(f"\nFiltering and extracting...\n")

doctors = []
for r in all_results:
    doctor = extract_doctor(r)
    if doctor:
        doctors.append(doctor)
        if len(doctors) % 100 == 0:
            print(f"  ✓ {len(doctors)} extracted...")

print(f"\n✅ {len(doctors)} valid doctors\n")

if doctors:
    df = pd.DataFrame(doctors).sort_values(by=["city", "doctor_name"])
    
    output = "il_behavioral_health_doctors.csv"
    df.to_csv(output, index=False)
    
    print("=" * 80)
    print(f"✅ SUCCESS! {len(df)} doctors saved to: {output}")
    print("=" * 80)
    
    print(f"\n📊 STATISTICS:\n")
    print(f"Total: {len(df)} | Cities: {df['city'].nunique()}\n")
    
    print("Top 10 Cities:")
    for i, (c, n) in enumerate(df['city'].value_counts().head(10).items(), 1):
        print(f"  {i:2}. {c:20} {n:3}")
    
    print(f"\nTop Specialties:")
    for s, n in df['specialty'].value_counts().head(10).items():
        print(f"  • {s[:40]:40} {n}")
    
    print(f"\nPractice Types:")
    for pt, n in df['practice_type'].value_counts().items():
        print(f"  • {pt:20} {n}")
    
    print(f"\nBilling Predictions:")
    for b, n in df['billing_prediction'].value_counts().items():
        print(f"  • {b:15} {n}")
    
    print(f"\n🎯 {(df['billing_prediction']=='High').sum()} HIGH priority doctors!\n")
    print("=" * 80)
    print("✅ View data: streamlit run app.py")
    print("=" * 80 + "\n")
else:
    print("⚠️ No doctors found\n")
