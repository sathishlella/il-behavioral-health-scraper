# app.py - Enhanced Dashboard for IL Behavioral Health Clinics
import pandas as pd
import streamlit as st

CSV_PATH = "il_behavioral_health_clinics.csv"

st.set_page_config(
    page_title="Velden – IL Behavioral Health Clinic Pipeline",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load clinic data from CSV."""
    try:
        df = pd.read_csv(path, dtype=str)
        # Convert numeric columns
        if "provider_count" in df.columns:
            df["provider_count"] = pd.to_numeric(df["provider_count"], errors="coerce").fillna(0).astype(int)
        if "billing_score" in df.columns:
            df["billing_score"] = pd.to_numeric(df["billing_score"], errors="coerce").fillna(0)
        return df
    except FileNotFoundError:
        return None


def main():
    st.title("🏥 Velden Health – Illinois Behavioral Health Clinic Pipeline")
    st.markdown("**Small Outpatient Clinics for Medical Billing Outreach**")

    # Load data
    df = load_data(CSV_PATH)
    
    if df is None:
        st.error(f"❌ CSV not found: `{CSV_PATH}`")
        st.info("👉 Run `scrape_npi_enhanced.py` first to generate clinic data.")
        st.code("python scrape_npi_enhanced.py", language="bash")
        st.stop()

    # Sidebar Filters
    st.sidebar.header("🔍 Filters")

    # City filter
    all_cities = sorted(df["city"].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "City", 
        options=all_cities, 
        default=[],
        help="Filter by city"
    )

    # Clinic size filter
    size_options = ["All"] + sorted(df["clinic_size"].unique().tolist())
    selected_size = st.sidebar.selectbox(
        "Clinic Size",
        options=size_options,
        index=0,
        help="Solo, Small Group, Medium, or Large"
    )

    # Billing prediction filter
    billing_options = ["All", "High", "Medium", "Low"]
    selected_billing = st.sidebar.selectbox(
        "Billing Prediction",
        options=billing_options,
        index=0,
        help="Likelihood they need medical billing services"
    )

    # Data availability filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Availability")
    has_website = st.sidebar.checkbox("Has Website", value=False)
    has_email = st.sidebar.checkbox("Has Email", value=False)

    # Search by name
    st.sidebar.markdown("---")
    search_term = st.sidebar.text_input(
        "🔎 Search Clinic Name",
        "",
        help="Search for clinics by name"
    )

    # Apply filters
    filtered = df.copy()

    if selected_cities:
        filtered = filtered[filtered["city"].isin(selected_cities)]

    if selected_size != "All":
        filtered = filtered[filtered["clinic_size"] == selected_size]

    if selected_billing != "All":
        filtered = filtered[filtered["billing_prediction"] == selected_billing]

    if has_website:
        filtered = filtered[filtered["website"].str.len() > 0]

    if has_email:
        filtered = filtered[filtered["email"].str.len() > 0]

    if search_term:
        filtered = filtered[
            filtered["clinic_name"].str.contains(search_term, case=False, na=False)
        ]

    # Summary Metrics
    st.subheader("📊 Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Clinics", len(df))
    with col2:
        st.metric("Filtered Results", len(filtered))
    with col3:
        high_priority = (df["billing_prediction"] == "High").sum()
        st.metric("High Billing Priority", high_priority)
    with col4:
        with_website = (df["website"].str.len() > 0).sum()
        st.metric("With Website", with_website)
    with col5:
        with_email = (df["email"].str.len() > 0).sum()
        st.metric("With Email", with_email)

    # Distribution Charts
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏢 Clinic Size Distribution")
        size_counts = filtered["clinic_size"].value_counts()
        st.bar_chart(size_counts)
    
    with col2:
        st.subheader("💼 Billing Prediction")
        billing_counts = filtered["billing_prediction"].value_counts()
        st.bar_chart(billing_counts)
    
    with col3:
        st.subheader("🏙️ Top Cities")
        city_counts = filtered["city"].value_counts().head(10)
        st.bar_chart(city_counts)

    # Main Data Table
    st.markdown("---")
    st.subheader("🗂️ Clinic Details")
    
    # Select columns to display
    display_columns = [
        "clinic_name",
        "city",
        "practice_type",
        "phone",
        "website",
        "email",
        "clinic_size",
        "billing_prediction",
        "billing_score",
    ]
    
    # Filter to only existing columns
    display_columns = [col for col in display_columns if col in filtered.columns]
    
    # Configure column display
    column_config = {
        "clinic_name": st.column_config.TextColumn("Clinic Name", width="medium"),
        "city": st.column_config.TextColumn("City", width="small"),
        "practice_type": st.column_config.TextColumn("Practice Type", width="large"),
        "phone": st.column_config.TextColumn("Phone", width="small"),
        "website": st.column_config.LinkColumn("Website", width="medium"),
        "email": st.column_config.TextColumn("Email", width="medium"),
        "clinic_size": st.column_config.TextColumn("Size", width="small"),
        "billing_prediction": st.column_config.TextColumn("Billing Need", width="small"),
        "billing_score": st.column_config.NumberColumn(
            "Score",
            width="small",
            format="%.2f"
        ),
    }
    
    st.dataframe(
        filtered[display_columns],
        column_config=column_config,
        use_container_width=True,
        height=500,
        hide_index=True
    )

    # Export functionality
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.caption(f"📁 Data source: NPI Registry API + Web Enrichment | {len(filtered)} clinics shown")
    
    with col2:
        # Download button for filtered data
        csv_data = filtered.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="filtered_clinics.csv",
            mime="text/csv",
        )

    # Detailed view for selected clinic
    st.markdown("---")
    st.subheader("🔍 Clinic Detail View")
    
    if not filtered.empty:
        clinic_names = filtered["clinic_name"].tolist()
        selected_clinic = st.selectbox(
            "Select a clinic to view details:",
            options=clinic_names,
            index=0
        )
        
        if selected_clinic:
            clinic_data = filtered[filtered["clinic_name"] == selected_clinic].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Basic Information**")
                st.write(f"**Name:** {clinic_data.get('clinic_name', 'N/A')}")
                st.write(f"**NPI:** {clinic_data.get('npi', 'N/A')}")
                st.write(f"**Practice Type:** {clinic_data.get('practice_type', 'N/A')}")
                st.write(f"**Address:** {clinic_data.get('address_1', 'N/A')}")
                if clinic_data.get('address_2'):
                    st.write(f"**Address 2:** {clinic_data.get('address_2')}")
                st.write(f"**City, State:** {clinic_data.get('city', 'N/A')}, {clinic_data.get('state', 'N/A')} {clinic_data.get('postal_code', '')}")
                st.write(f"**Phone:** {clinic_data.get('phone', 'N/A')}")
            
            with col2:
                st.markdown("**🌐 Contact & Insights**")
                
                website = clinic_data.get('website', '')
                if website:
                    st.write(f"**Website:** [{website}]({website})")
                else:
                    st.write("**Website:** Not found")
                
                email = clinic_data.get('email', '')
                if email:
                    st.write(f"**Email:** {email}")
                else:
                    st.write("**Email:** Not found")
                
                st.write(f"**Clinic Size:** {clinic_data.get('clinic_size', 'N/A')}")
                st.write(f"**Provider Count:** ~{clinic_data.get('provider_count', 'N/A')}")
                st.write(f"**Billing Prediction:** {clinic_data.get('billing_prediction', 'N/A')}")
                st.write(f"**Billing Score:** {clinic_data.get('billing_score', 'N/A')}")
                
                billing_reason = clinic_data.get('billing_reason', '')
                if billing_reason:
                    st.info(f"💡 **Why:** {billing_reason}")


if __name__ == "__main__":
    main()
