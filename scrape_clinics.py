"""
Enhanced Multi-State Behavioral Health Clinic Scraper
Features:
- Multi-state support (IL, FL, MI, and more)
- 15+ targeted search terms
- Practice type classification
- Current vs Future prospect categorization
- Expanded data collection
"""

import requests
import pandas as pd
import re
import time
from revenue_estimator import calculate_revenue, format_revenue_display

NPI_URL = "https://npiregistry.cms.hhs.gov/api/"

# States to scrape - CURRENTLY FOCUSED ON ILLINOIS ONLY
STATES = ["IL"]  # Change this to add more states: ["IL", "FL", "MI"]

# Comprehensive search terms for maximum coverage
SEARCH_TERMS = [
    # Core mental health
    "mental health clinic",
    "mental health center",
    "behavioral health",
    "behavioral health clinic",
    
    # Therapy focused
    "therapy center",
    "therapy clinic",
    "therapist",
    "psychotherapy",
    
    # Counseling focused
    "counseling center",
    "counseling services",
    "counselor",
    "family counseling",
    "marriage therapy",
    
    # Psychology/Psychiatry
    "psychology",
    "psychologist",
    "psychiatry",
    "psychiatric",
    
    # Specialized
    "trauma therapy",
    "child therapy",
    "adolescent mental health",
    "substance abuse counseling",
    "addiction counseling",
]

def fetch(state, search_term, skip=0):
    """Fetch NPI data for a state and search term."""
    params = {
        "version": "2.1",
        "state": state,
        "taxonomy_description": search_term,
        "limit": 200,
        "skip": skip
    }
    try:
        r = requests.get(NPI_URL, params=params, timeout=30)
        return r.json()
    except Exception as e:
        print(f" Error: {e}")
        return {"result_count": 0, "results": []}

def classify_practice_type(name, taxonomies):
    """Classify practice into specific type and priority."""
    name_lower = name.lower()
    tax_str = " ".join([t.get("desc", "") or "" for t in taxonomies]).lower()
    
    # FUTURE PROSPECTS (not current focus)
    if "neurology" in tax_str or "neurolog" in name_lower:
        if "psychiatr" not in tax_str:  # Avoid psychiatry/neurology overlap
            return "Neurology Practice", "Future"
    
    if "orthopedic" in tax_str or "orthopaedic" in tax_str or "ortho" in name_lower:
        return "Orthopedic Clinic", "Future"
    
    if "pain management" in tax_str or "pain mgmt" in name_lower:
        return "Pain Management", "Future"
    
    if "physical therapy" in tax_str or "physical therap" in name_lower:
        return "Physical Therapy", "Future"
    
    # CURRENT TARGETS (your focus)
    if "psychiatr" in tax_str:
        return "Psychiatry Practice", "Current"
    
    if "psycholog" in tax_str:
        return "Psychology Practice", "Current"
    
    if "counselor" in tax_str or "counseling" in name_lower or "counsel" in name_lower:
        return "Counseling Center", "Current"
    
    if ("therap" in name_lower or "therapy" in tax_str) and "physical" not in name_lower:
        return "Therapy Center", "Current"
    
    if "substance" in tax_str or "addiction" in tax_str:
        return "Substance Abuse Treatment", "Current"
    
    # Default to mental health clinic
    return "Mental Health Clinic", "Current"

def determine_size(org_name):
    """Determine clinic size from name."""
    name = org_name.lower()
    
    if any(w in name for w in ["group", "associates", "partners", " & ", " and "]):
        return "Small Group"
    if "center" in name or "clinic" in name:
        return "Small Group"
    if any(w in name for w in [" llc", " inc", " pllc", " pc"]):
        return "Solo or Small"
    
    return "Unknown"

def predict_billing(org_name, practice_type, size):
    """Predict billing service need."""
    score = 0
    
    # Size factor
    if size == "Small Group":
        score += 3
    elif "Solo" in size:
        score += 2
    
    # Practice type factor
    pt_lower = practice_type.lower()
    if "psychiatr" in pt_lower:
        score += 2
    if "substance" in pt_lower or "addiction" in pt_lower:
        score += 2
    if "counselor" in pt_lower or "therapy" in pt_lower:
        score += 1
    
    # Name indicators
    name_lower = org_name.lower()
    if any(w in name_lower for w in [" llc", " inc", " pllc"]):
        score += 1
    
    # Final prediction
    if score >= 4:
        return "High"
    elif score >= 2:
        return "Medium"
    return "Low"

def clean_url(name):
    """Create clean URL from clinic name."""
    if not name:
        return ""
    n = re.sub(r'[^\w\s]', '', name.lower())
    n = n.replace(" llc", "").replace(" inc", "").replace(" pllc", "").replace(" pc", "")
    n = n.strip().replace(" ", "")
    return n if len(n) > 2 else ""

def extract_clinic(result, state):
    """Extract clinic data from NPI result."""
    basic = result.get("basic", {})
    org_name = basic.get("organization_name", "")
    
    if not org_name:
        return None
    
    # Filter out large systems
    name_lower = org_name.lower()
    exclude_keywords = [
        "hospital", "health system", "university", "medical center",
        "department of", "state of", "federal", "government",
        "county health", "public health department"
    ]
    if any(k in name_lower for k in exclude_keywords):
        return None
    
    # Get address
    addrs = result.get("addresses", [])
    addr = next((a for a in addrs if a.get("address_purpose") == "LOCATION"), addrs[0] if addrs else None)
    
    if not addr:
        return None
    
    # Verify state matches
    if addr.get("state", "") != state:
        return None
    
    # Get taxonomies
    taxs = result.get("taxonomies", [])
    tax_descs = [t.get("desc", "") for t in taxs if t.get("desc")]
    
    # Classify practice
    practice_type, target_priority = classify_practice_type(org_name, taxs)
    
    # Determine size and billing
    size = determine_size(org_name)
    billing = predict_billing(org_name, practice_type, size)
    
    # Don't infer website/email - they're usually wrong!
    # Leave blank - use enrich_contacts.py to get REAL contacts from websites
    website = ""
    email = ""
    
    # Format phone
    phone = addr.get("telephone_number", "")
    if phone:
        d = re.sub(r'\D', '', phone)
        if len(d) == 10:
            phone = f"({d[:3]}) {d[3:6]}-{d[6:]}"
    
    # Calculate revenue estimates
    revenue_data = calculate_revenue(practice_type, size)
    
    return {
        "clinic_name": org_name,
        "practice_type": practice_type,
        "target_priority": target_priority,
        "taxonomy_description": "; ".join(tax_descs[:2]) if tax_descs else "",
        "address": (addr.get("address_1", "") + " " + addr.get("address_2", "")).strip(),
        "city": addr.get("city", ""),
        "state": addr.get("state", ""),
        "postal_code": (addr.get("postal_code", "") or "")[:5],
        "phone": phone,
        "website": website,
        "email": email,
        "clinic_size": size,
        "billing_prediction": billing,
        "est_monthly_collections": revenue_data["monthly_collections"],
        "est_monthly_revenue": revenue_data["rcm_revenue_estimate"],
        "est_revenue_range": f"${revenue_data['rcm_revenue_min']:.0f}-${revenue_data['rcm_revenue_max']:.0f}",
        "est_annual_value": round(revenue_data["rcm_revenue_estimate"] * 12, 2),
        "npi": result.get("number", "")
    }

print("\n" + "=" * 90)
print("  ENHANCED MULTI-STATE BEHAVIORAL HEALTH CLINIC SCRAPER")
print("=" * 90)
print(f"\nSearching states: {', '.join(STATES)}")
print(f"Search terms: {len(SEARCH_TERMS)}")
print(f"Expected results: 5,000-10,000+ clinics\n")
print("=" * 90)

all_results = []
npi_set = set()
state_counts = {state: 0 for state in STATES}

for state in STATES:
    print(f"\n📍 STATE: {state}")
    print("-" * 90)
    
    for term in SEARCH_TERMS:
        print(f"  '{term}'... ", end="", flush=True)
        
        data = fetch(state, term)
        count = data.get("result_count", 0)
        print(f"{count:,} found", end="")
        
        # Get first page
        for r in data.get("results", []):
            npi = r.get("number")
            if npi and npi not in npi_set:
                all_results.append((r, state))
                npi_set.add(npi)
                state_counts[state] += 1
        
        # Get additional pages (max 25 pages = 5,000 records)
        if count > 200:
            max_pages = min(25, (count // 200) + 1)
            fetched_pages = 1
            
            for p in range(1, max_pages):
                data = fetch(state, term, skip=p * 200)
                results = data.get("results", [])
                
                for r in results:
                    npi = r.get("number")
                    if npi and npi not in npi_set:
                        all_results.append((r, state))
                        npi_set.add(npi)
                        state_counts[state] += 1
                
                fetched_pages += 1
                time.sleep(0.2)
            
            print(f" → {fetched_pages} pages")
        else:
            print()

print("\n" + "=" * 90)
print(f"✅ Total unique NPIs collected: {len(all_results):,}")
print("\nBy State:")
for state, count in state_counts.items():
    print(f"  {state}: {count:,}")
print("=" * 90)

print("\n🔄 Processing and filtering...\n")

clinics = []
skipped = 0

for i, (result, state) in enumerate(all_results):
    clinic = extract_clinic(result, state)
    if clinic:
        clinics.append(clinic)
        if len(clinics) % 500 == 0:
            print(f"  ✓ {len(clinics):,} valid clinics extracted...")
    else:
        skipped += 1

print(f"\n✅ {len(clinics):,} valid clinics extracted")
print(f"⏭️  {skipped:,} filtered out (large systems, missing data, etc.)")

if clinics:
    df = pd.DataFrame(clinics)
    df = df.sort_values(by=["state", "city", "clinic_name"])
    
    output = "il_behavioral_health_clinics.csv"
    df.to_csv(output, index=False)
    
    print("\n" + "=" * 90)
    print(f"✅ SUCCESS! {len(df):,} clinics saved to: {output}")
    print("=" * 90)
    
    # Statistics
    print(f"\n📊 STATISTICS:\n")
    
    print("By State:")
    for state, count in df['state'].value_counts().items():
        print(f"  {state}: {count:,}")
    
    print(f"\nBy Practice Type:")
    for ptype, count in df['practice_type'].value_counts().head(10).items():
        print(f"  • {ptype:35} {count:,}")
    
    print(f"\nBy Target Priority:")
    for priority, count in df['target_priority'].value_counts().items():
        print(f"  • {priority:15} {count:,}")
    
    print(f"\nBy Clinic Size:")
    for size, count in df['clinic_size'].value_counts().items():
        print(f"  • {size:20} {count:,}")
    
    print(f"\nBy Billing Prediction:")
    for billing, count in df['billing_prediction'].value_counts().items():
        print(f"  • {billing:15} {count:,}")
    
    # Current targets only
    current_targets = df[df['target_priority'] == 'Current']
    high_priority = (current_targets['billing_prediction'] == 'High').sum()
    
    print(f"\n🎯 CURRENT TARGETS: {len(current_targets):,} clinics")
    print(f"   High Priority: {high_priority:,}")
    print(f"\n📅 FUTURE PROSPECTS: {(df['target_priority']=='Future').sum():,} clinics")
    
    print("\n" + "=" * 90)
    print("NEXT STEPS:")
    print("  1. Run dashboard: streamlit run app.py")
    print("  2. Filter by: Target Priority = 'Current'")
    print("  3. Filter by: Practice Type (Counseling, Therapy, etc.)")
    print("  4. Filter by: Billing Prediction = 'High'")
    print("  5. Export filtered list for outreach!")
    print("=" * 90 + "\n")
    
else:
    print("\n⚠️ No clinics found\n")
