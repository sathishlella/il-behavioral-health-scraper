"""
Revenue Estimator for Velden Health RCM
Calculates estimated monthly RCM revenue based on:
- Practice type and size
- Industry-standard collections data
- Your customizable RCM pricing
"""

# ====================================================================
# CUSTOMIZE THESE VALUES BASED ON YOUR PRICING MODEL
# ====================================================================

# Your RCM Pricing (choose one method)
RCM_PRICING = {
    "method": "percentage",  # "percentage" or "per_claim"
    "percentage_rate": 6.5,  # % of collections you charge (if using percentage method)
    "per_claim_rate": 8.50,  # $ per claim you charge (if using per_claim method)
}

# ====================================================================
# INDUSTRY DATA - Based on CMS and Insurance Payment Averages
# ====================================================================

# Average monthly collections by practice type and size
# Sources: MGMA, CMS physician fee schedules, industry benchmarks
MONTHLY_COLLECTIONS = {
    # Psychiatry Practices (CPT codes 90832-90899, avg $150-250/session)
    "Psychiatry Practice": {
        "Solo or Small": 35000,      # 1 provider, ~25-30 patients/week
        "Small Group": 87500,         # 2-3 providers
        "Medium": 175000,             # 5-7 providers
        "Unknown": 35000,
    },
    
    # Psychology Practices (CPT codes 90832-90837, avg $120-180/session)
    "Psychology Practice": {
        "Solo or Small": 25000,       # 1 provider, ~30-35 patients/week
        "Small Group": 62500,         # 2-3 providers
        "Medium": 125000,             # 5-7 providers
        "Unknown": 25000,
    },
    
    # Counseling Centers (CPT codes 90832-90834, 90846-90847, avg $90-130/session)
    "Counseling Center": {
        "Solo or Small": 18000,       # 1-2 counselors
        "Small Group": 54000,         # 3-5 counselors
        "Medium": 108000,             # 6-10 counselors
        "Unknown": 18000,
    },
    
    # Therapy Centers (Similar to counseling)
    "Therapy Center": {
        "Solo or Small": 20000,
        "Small Group": 60000,
        "Medium": 120000,
        "Unknown": 20000,
    },
    
    # Mental Health Clinics (Mixed services)
    "Mental Health Clinic": {
        "Solo or Small": 22000,
        "Small Group": 66000,
        "Medium": 132000,
        "Unknown": 22000,
    },
    
    # Substance Abuse Treatment (CPT codes 90832, H0001-H0050, insurance-heavy)
    "Substance Abuse Treatment": {
        "Solo or Small": 30000,       # High claim volume, insurance billing
        "Small Group": 90000,
        "Medium": 180000,
        "Unknown": 30000,
    },
}

# Average claims per month by practice type (for per-claim pricing)
MONTHLY_CLAIMS = {
    "Psychiatry Practice": 120,       # Fewer patients, longer sessions, med management
    "Psychology Practice": 100,       # Therapy sessions
    "Counseling Center": 140,         # High volume, shorter sessions
    "Therapy Center": 130,
    "Mental Health Clinic": 125,
    "Substance Abuse Treatment": 180, # Very high volume
}

# Default values for unknown types
DEFAULT_COLLECTIONS = 20000
DEFAULT_CLAIMS = 100


def calculate_revenue(practice_type, clinic_size):
    """
    Calculate estimated monthly RCM revenue for a clinic.
    
    Args:
        practice_type (str): Type of practice (e.g., "Psychiatry Practice")
        clinic_size (str): Size category (e.g., "Small Group")
    
    Returns:
        dict: {
            "monthly_collections": int,
            "monthly_claims": int,
            "rcm_revenue_estimate": float,
            "rcm_revenue_min": float,
            "rcm_revenue_max": float,
            "method": str
        }
    """
    
    # Get collections estimate
    if practice_type in MONTHLY_COLLECTIONS:
        collections = MONTHLY_COLLECTIONS[practice_type].get(clinic_size, DEFAULT_COLLECTIONS)
    else:
        collections = DEFAULT_COLLECTIONS
    
    # Get claims estimate
    claims = MONTHLY_CLAIMS.get(practice_type, DEFAULT_CLAIMS)
    
    # Adjust claims by size
    size_multipliers = {
        "Solo or Small": 1.0,
        "Small Group": 3.0,  # ~3 providers
        "Medium": 6.0,       # ~6 providers
        "Unknown": 1.0,
    }
    claims = int(claims * size_multipliers.get(clinic_size, 1.0))
    
    # Calculate RCM revenue based on pricing method
    if RCM_PRICING["method"] == "percentage":
        rcm_revenue = collections * (RCM_PRICING["percentage_rate"] / 100)
        # Add ±20% range for uncertainty
        rcm_min = rcm_revenue * 0.8
        rcm_max = rcm_revenue * 1.2
        method = f"{RCM_PRICING['percentage_rate']}% of collections"
    
    else:  # per_claim
        rcm_revenue = claims * RCM_PRICING["per_claim_rate"]
        # Add ±20% range for claim volume uncertainty
        rcm_min = rcm_revenue * 0.8
        rcm_max = rcm_revenue * 1.2
        method = f"${RCM_PRICING['per_claim_rate']}/claim"
    
    return {
        "monthly_collections": int(collections),
        "monthly_claims": claims,
        "rcm_revenue_estimate": round(rcm_revenue, 2),
        "rcm_revenue_min": round(rcm_min, 2),
        "rcm_revenue_max": round(rcm_max, 2),
        "method": method,
    }


def format_revenue_display(revenue_data):
    """
    Format revenue data for display.
    
    Args:
        revenue_data (dict): Output from calculate_revenue()
    
    Returns:
        str: Formatted string like "$2,925/mo ($2,350-$3,500)"
    """
    est = revenue_data["rcm_revenue_estimate"]
    min_val = revenue_data["rcm_revenue_min"]
    max_val = revenue_data["rcm_revenue_max"]
    
    return f"${est:,.0f}/mo (${min_val:,.0f}-${max_val:,.0f})"


def get_annual_value(revenue_data):
    """
    Calculate annual RCM revenue value.
    
    Args:
        revenue_data (dict): Output from calculate_revenue()
    
    Returns:
        float: Annual revenue estimate
    """
    return revenue_data["rcm_revenue_estimate"] * 12


# ====================================================================
# EXAMPLE USAGE
# ====================================================================

if __name__ == "__main__":
    # Example calculations
    examples = [
        ("Psychiatry Practice", "Small Group"),
        ("Counseling Center", "Solo or Small"),
        ("Therapy Center", "Small Group"),
        ("Psychology Practice", "Medium"),
    ]
    
    print("\n" + "=" * 80)
    print("VELDEN HEALTH RCM - REVENUE ESTIMATOR")
    print("=" * 80)
    print(f"\nPricing Method: {RCM_PRICING['method']}")
    if RCM_PRICING['method'] == 'percentage':
        print(f"Rate: {RCM_PRICING['percentage_rate']}% of collections")
    else:
        print(f"Rate: ${RCM_PRICING['per_claim_rate']} per claim")
    print("\n" + "-" * 80)
    
    total_annual = 0
    
    for practice_type, size in examples:
        revenue = calculate_revenue(practice_type, size)
        annual = get_annual_value(revenue)
        total_annual += annual
        
        print(f"\n{practice_type} - {size}")
        print(f"  Est. Collections: ${revenue['monthly_collections']:,}/mo")
        print(f"  Est. Claims: {revenue['monthly_claims']}/mo")
        print(f"  RCM Revenue: {format_revenue_display(revenue)}")
        print(f"  Annual Value: ${annual:,.0f}")
    
    print("\n" + "=" * 80)
    print(f"Total Annual Value (4 examples): ${total_annual:,.0f}")
    print("=" * 80 + "\n")
