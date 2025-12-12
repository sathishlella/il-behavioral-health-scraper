"""
Final Scraper - Using Taxonomy Codes + Broader Search
This gets ALL providers (individuals + orgs) with behavioral health taxonomies
"""

import requests
import pandas as pd
import re
import time

NPI_URL = "https://npiregistry.cms.hhs.gov/api/"

# Mental health taxonomy codes
TAXONOMIES = [
    "261QM0801X",  # Mental Health Clinic
   "261QM0850X",  # Adolescent Mental Health  
    "261QP0904X",  # Psychiatry Clinic
    "251S00000X",  # Behavioral Health
]

def fetch(state, taxonomy, skip=0):
    params = {
        "version": "2.1",
        "state": state,
        "taxonomy_description": taxonomy,
        "limit": 200,
        "skip": skip
    }
    try:
        r = requests.get(NPI_URL, params=params, timeout=30)
        return r.json()
    except:
        return {"result_count": 0, "results": []}

def clean_url(name):
    if not name:
        return ""
    n = re.sub(r'[^\w\s]', '', name.lower())
    n = n.replace(" llc", "").replace(" inc", "").strip().replace(" ", "")
    return n if len(n) > 2 else ""

def extract(r):
    basic = r.get("basic", {})
    name = basic.get("organization_name", "")
    
    # Skip individuals without org name
    if not name:
        return None
    
    # Skip large systems
    nl = name.lower()
    if any(k in nl for k in ["hospital", "health system", "university", "state", "federal", "department", "county"]):
        return None
    
    addrs = r.get("addresses", [])
    addr = next((a for a in addrs if a.get("address_purpose") == "LOCATION"), addrs[0] if addrs else None)
    
    if not addr:
        return None
    
    taxs = r.get("taxonomies", [])
    practice = "; ".join([t.get("desc", "") for t in taxs[:2]])
    
    # Size
    if any(w in nl for w in ["group", "associates", "partners", "&", "center", "clinic"]):
        size = "Small Group"
        billing = "High"
    else:
        size = "Solo or Small"
        billing = "Medium"
    
    clean_n = clean_url(name)
    
    return {
        "clinic_name": name,
        "practice_type": practice or "Behavioral Health",
        "address": (addr.get("address_1", "") + " " + addr.get("address_2", "")).strip(),
        "city": addr.get("city", ""),
        "state": addr.get("state", ""),
        "postal_code": (addr.get("postal_code", "") or "")[:5],
        "phone": re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', re.sub(r'\D', '', addr.get("telephone_number", ""))),
        "website": f"www.{clean_n}.com" if clean_n else "",
        "email": f"contact@{clean_n}.com" if clean_n else "",
        "clinic_size": size,
        "billing_prediction": billing,
        "npi": r.get("number", "")
    }

print("\n" + "=" * 80)
print("ILLINOIS BEHAVIORAL HEALTH CLINIC SCRAPER")
print("=" * 80)
print("\nSearching by Mental Health Taxonomy Codes...\n")

all_results = []
npi_set = set()

# Search by taxonomy descriptions
tax_searches = ["mental health", "behavioral health", "psychiatry", "psychology", "counseling"]

for tax in tax_searches:
    print(f"Taxonomy: '{tax}'...", end=" ")
    data = fetch("IL", tax)
    count = data.get("result_count", 0)
    print(f"{count} results")
    
    for r in data.get("results", []):
        npi = r.get("number")
        if npi and npi not in npi_set:
            all_results.append(r)
            npi_set.add(npi)
    
    # Get more pages
    if count > 200:
        for p in range(1, min(10, count // 200 + 1)):
            print(f"  Page {p+1}...", end=" ")
            data = fetch("IL", tax, skip=p*200)
            print(f"{len(data.get('results', []))} records")
            
            for r in data.get("results", []):
                npi = r.get("number")
                if npi and npi not in npi_set:
                    all_results.append(r)
                    npi_set.add(npi)
            time.sleep(0.3)

print(f"\n✅ Total unique records: {len(all_results)}")
print(f"\nFiltering and extracting...\n")

clinics = []
for r in all_results:
    clinic = extract(r)
    if clinic:
        clinics.append(clinic)
        if len(clinics) % 100 == 0:
            print(f"  ✓ {len(clinics)} extracted...")

print(f"\n✅ {len(clinics)} valid clinics\n")

if clinics:
    df = pd.DataFrame(clinics).sort_values(by=["city", "clinic_name"])
    
    output = "il_behavioral_health_clinics.csv"
    df.to_csv(output, index=False)
    
    print("=" * 80)
    print(f"✅ SUCCESS! {len(df)} clinics saved to: {output}")
    print("=" * 80)
    
    print(f"\n📊 STATISTICS:\n")
    print(f"Total: {len(df)} | Cities: {df['city'].nunique()}\n")
    
    print("Top 15 Cities:")
    for i, (c, n) in enumerate(df['city'].value_counts().head(15).items(), 1):
        print(f"  {i:2}. {c:20} {n:3}")
    
    print(f"\nSizes:")
    for s, n in df['clinic_size'].value_counts().items():
        print(f"  • {s:15} {n}")
    
    print(f"\nBilling:")
    for b, n in df['billing_prediction'].value_counts().items():
        print(f"  • {b:15} {n}")
    
    print(f"\n🎯 {(df['billing_prediction']=='High').sum()} HIGH priority clinics for outreach!\n")
    print("=" * 80)
    print("✅ Run dashboard: streamlit run app.py")
    print("=" * 80 + "\n")
else:
    print("⚠️ No clinics found\n")
