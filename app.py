# app.py - Enhanced Dashboard with Data Refresh Capabilities
import pandas as pd
import streamlit as st
import subprocess
import sys
from datetime import datetime
import os
from outreach_tracker import (
    get_status, update_status, get_pipeline_summary, 
    VALID_STATUSES, add_note
)
from contact_validator import validate_contact, get_status_icon

CSV_CLINICS = "il_behavioral_health_clinics.csv"
CSV_DOCTORS = "il_behavioral_health_doctors.csv"

# Login credentials
USERNAME = "Admin"
PASSWORD = "Admin123"

st.set_page_config(
    page_title="Velden – IL Behavioral Health Pipeline",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load clinic/doctor data from CSV."""
    try:
        if not os.path.exists(path):
            return None
        df = pd.read_csv(path, dtype=str)
        # Convert numeric columns
        if "provider_count" in df.columns:
            df["provider_count"] = pd.to_numeric(df["provider_count"], errors="coerce").fillna(0).astype(int)
        if "billing_score" in df.columns:
            df["billing_score"] = pd.to_numeric(df["billing_score"], errors="coerce").fillna(0)
        return df
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return None


def run_scraper(script_name: str, description: str):
    """Run a scraper script and show progress."""
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    try:
        progress_placeholder.info(f"🔄 Running {description}...")
        
        # Run the scraper
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            progress_placeholder.empty()
            status_placeholder.success(f"✅ {description} completed successfully!")
            
            # Show output summary
            with st.expander("View scraper output"):
                st.text(result.stdout)
            
            # Clear cache to reload data
            st.cache_data.clear()
            return True
        else:
            progress_placeholder.empty()
            status_placeholder.error(f"❌ {description} failed!")
            with st.expander("View error details"):
                st.text(result.stderr or result.stdout)
            return False
            
    except subprocess.TimeoutExpired:
        progress_placeholder.empty()
        status_placeholder.error(f"⏱️ {description} timed out (took longer than 5 minutes)")
        return False
    except Exception as e:
        progress_placeholder.empty()
        status_placeholder.error(f"❌ Error running {description}: {str(e)}")
        return False


def login_page():
    """Display login page."""
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("# 🏥 Velden Health")
        st.markdown("### Illinois Behavioral Health Pipeline")
        st.markdown("---")
        
        # Login form
        with st.form("login_form"):
            st.markdown("#### 🔐 Login")
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username == USERNAME and password == PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.login_attempts = 0
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    st.error(f"❌ Invalid credentials. Attempt {st.session_state.login_attempts}/3")
                    
                    if st.session_state.login_attempts >= 3:
                        st.warning("⚠️ Too many failed attempts. Please refresh the page.")
        
        # Help text
        st.markdown("---")
        st.caption("🔒 Secure access to clinic pipeline data")
        st.caption("Contact administrator if you've forgotten credentials")


def main():
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown("---")
    
    st.title("🏥 Velden Health – Illinois Behavioral Health Pipeline")
    
    # Sidebar - Data Management
    with st.sidebar:
        st.header("📊 Data Management")
        
        st.markdown("### Refresh Data")
        st.caption("Click to fetch latest data from NPI Registry")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏢 Refresh Clinics", use_container_width=True):
                with st.spinner("Fetching clinics..."):
                    success = run_scraper("scrape_clinics.py", "Clinic scraper")
                    if success:
                        st.rerun()
        
        with col2:
            if st.button("👨‍⚕️ Refresh Doctors", use_container_width=True):
                with st.spinner("Fetching doctors..."):
                    success = run_scraper("scrape_doctors.py", "Doctor scraper")
                    if success:
                        st.rerun()
        
        if st.button("🔄 Refresh Both", type="primary", use_container_width=True):
            with st.spinner("Fetching all data..."):
                clinics_success = run_scraper("scrape_clinics.py", "Clinic scraper")
                doctors_success = run_scraper("scrape_doctors.py", "Doctor scraper")
                
                if clinics_success or doctors_success:
                    st.rerun()
        
        st.markdown("---")
        
        # Data file info
        st.markdown("### 📁 Current Data")
        
        if os.path.exists(CSV_CLINICS):
            clinics_modified = datetime.fromtimestamp(os.path.getmtime(CSV_CLINICS))
            st.caption(f"**Clinics:** Last updated {clinics_modified.strftime('%Y-%m-%d %H:%M')}")
        else:
            st.caption("**Clinics:** No data yet")
        
        if os.path.exists(CSV_DOCTORS):
            doctors_modified = datetime.fromtimestamp(os.path.getmtime(CSV_DOCTORS))
            st.caption(f"**Doctors:** Last updated {doctors_modified.strftime('%Y-%m-%d %H:%M')}")
        else:
            st.caption(f"**Doctors:** No data yet")
        
        st.markdown("---")
        
        # Pipeline Summary
        st.markdown("### 📈 Sales Pipeline")
        try:
            pipeline = get_pipeline_summary()
            st.metric("Active Pipeline", pipeline["active_pipeline"])
            
            with st.expander("Pipeline Details"):
                st.write(f"**Total Tracked:** {pipeline['total']}")
                st.write(f"**Contacted:** {pipeline['Contacted']}")
                st.write(f"**Meetings:** {pipeline['Meeting Scheduled']}")
                st.write(f"**Proposals:** {pipeline['Proposal Sent']}")
                st.write(f"**Won:** {pipeline['Won']}")
        except Exception as e:
            st.caption("No tracking data yet")
        
        st.markdown("---")
    
    # Main content tabs
    tab1, tab2 = st.tabs(["🏢 Clinics/Organizations", "👨‍⚕️ Individual Doctors"])
    
    # ==================== CLINICS TAB ====================
    with tab1:
        df_clinics = load_data(CSV_CLINICS)
        
        if df_clinics is None or df_clinics.empty:
            st.warning("⚠️ No clinic data found. Click 'Refresh Clinics' to fetch data.")
            st.info("👉 Use the sidebar to refresh data from NPI Registry")
        else:
            # Filters
            st.subheader("🔍 Filters")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                # State filter
                all_states = sorted(df_clinics["state"].dropna().unique().tolist())
                selected_states = st.multiselect("State", options=all_states, default=all_states)
            
            with col2:
                # Practice Type filter
                all_types = sorted(df_clinics["practice_type"].dropna().unique().tolist())
                selected_types = st.multiselect("Practice Type", options=all_types, default=[])
            
            with col3:
                # Target Priority filter
                priority_options = ["All", "Current Targets", "Future Prospects"]
                selected_priority = st.selectbox("Target Priority", options=priority_options, index=0)
            
            with col4:
                # Clinic Size filter
                size_options = ["All"] + sorted(df_clinics["clinic_size"].unique().tolist())
                selected_size = st.selectbox("Clinic Size", options=size_options, index=0)
           
            with col5:
                # Billing Prediction filter
                billing_options = ["All", "High", "Medium", "Low"]
                selected_billing = st.selectbox("Billing Need", options=billing_options, index=0)
            
            # Second row of filters
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # City filter
                all_cities = sorted(df_clinics["city"].dropna().unique().tolist())
                selected_cities = st.multiselect("City", options=all_cities, default=[])
            
            with col2:
                has_website = st.checkbox("Has Website")
            
            with col3:
                has_email = st.checkbox("Has Email")
            
            with col4:
                search_term = st.text_input("🔎 Search name", "")
            
            # Apply filters
            filtered = df_clinics.copy()
            
            if selected_states:
                filtered = filtered[filtered["state"].isin(selected_states)]
            if selected_types:
                filtered = filtered[filtered["practice_type"].isin(selected_types)]
            if selected_priority == "Current Targets":
                filtered = filtered[filtered["target_priority"] == "Current"]
            elif selected_priority == "Future Prospects":
                filtered = filtered[filtered["target_priority"] == "Future"]
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
                filtered = filtered[filtered["clinic_name"].str.contains(search_term, case=False, na=False)]
            
            # Summary
            st.subheader("📊 Summary")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Clinics", f"{len(df_clinics):,}")
            with col2:
                st.metric("Filtered Results", f"{len(filtered):,}")
            with col3:
                current = (df_clinics["target_priority"] == "Current").sum()
                st.metric("Current Targets", f"{current:,}")
            with col4:
                high_priority = (df_clinics["billing_prediction"] == "High").sum()
                st.metric("High Priority", f"{high_priority:,}")
            with col5:
                states_count = df_clinics["state"].nunique()
                st.metric("States", states_count)
            
            # Practice Type Breakdown (for Current targets)
            if "target_priority" in df_clinics.columns:
                current_targets = df_clinics[df_clinics["target_priority"] == "Current"]
                if not current_targets.empty:
                    st.markdown("### 🎯 Current Target Breakdown")
                    type_breakdown = current_targets["practice_type"].value_counts().head(8)
                    
                    cols = st.columns(4)
                    for idx, (ptype, count) in enumerate(type_breakdown.items()):
                        with cols[idx % 4]:
                            st.metric(ptype, f"{count:,}")
            
            # Data table with status tracking
            st.subheader("🗂️ Clinic List")
            
            # Add status tracking columns
            display_df = filtered.copy()
            
            # Add outreach status if available
            if 'npi' in display_df.columns:
                display_df['outreach_status'] = display_df['npi'].apply(
                    lambda npi: get_status(npi)['status'] if get_status(npi) else "Not Contacted"
                )
                # Add notes column
                display_df['notes'] = display_df['npi'].apply(
                    lambda npi: get_status(npi)['notes'] if get_status(npi) and get_status(npi).get('notes') else ""
                )
            
            # Add validation status for website and email
            if 'website' in display_df.columns and 'email' in display_df.columns:
                @st.cache_data(ttl=3600)  # Cache for 1 hour
                def get_validation_status(website, email):
                    """Get validation status with caching."""
                    try:
                        result = validate_contact(website, email)
                        web_icon = get_status_icon(result['website_status'])
                        email_icon = get_status_icon(result['email_status'])
                        return web_icon, email_icon
                    except:
                        return "❓", "❓"
                
                # Add validation columns
                validation_results = display_df.apply(
                    lambda row: get_validation_status(row.get('website', ''), row.get('email', '')),
                    axis=1
                )
                display_df['web_check'] = validation_results.apply(lambda x: x[0])
                display_df['email_check'] = validation_results.apply(lambda x: x[1])
            
            # Select columns to display
            display_cols = ["clinic_name", "practice_type", "city", "state", "phone"]
            
            # Add website and email
            if 'website' in display_df.columns:
                display_cols.append("website")
            if 'email' in display_df.columns:
                display_cols.append("email")
            
            # Add validation columns
            if 'web_check' in display_df.columns:
                display_cols.append("web_check")
            if 'email_check' in display_df.columns:
                display_cols.append("email_check")
            
            # Add revenue columns if they exist
            if "est_monthly_revenue" in display_df.columns:
                display_cols.append("est_monthly_revenue")
            if "est_annual_value" in display_df.columns:
                display_cols.append("est_annual_value")
            
            # Add other important columns
            display_cols.extend(["clinic_size", "billing_prediction"])
            
            if 'outreach_status' in display_df.columns:
                display_cols.append("outreach_status")
            if 'notes' in display_df.columns:
                display_cols.append("notes")
            
            # Keep only available columns
            display_cols = [c for c in display_cols if c in display_df.columns]
            
            # Format revenue columns for display
            if "est_monthly_revenue" in display_df.columns:
                display_df["est_monthly_revenue"] = display_df["est_monthly_revenue"].apply(
                    lambda x: f"${float(x):,.0f}/mo" if pd.notna(x) else "$0"
                )
            if "est_annual_value" in display_df.columns:
                display_df["est_annual_value"] = display_df["est_annual_value"].apply(
                    lambda x: f"${float(x):,.0f}/yr" if pd.notna(x) else "$0"
                )
            
            st.dataframe(
                display_df[display_cols],
                use_container_width=True,
                height=500,
                hide_index=True,
                column_config={
                    "clinic_name": st.column_config.TextColumn("Clinic Name", width="large"),
                    "practice_type": st.column_config.TextColumn("Practice Type", width="medium"),
                    "city": st.column_config.TextColumn("City", width="medium"),
                    "state": st.column_config.TextColumn("State", width="small"),
                    "phone": st.column_config.TextColumn("Phone", width="medium"),
                    "website": st.column_config.TextColumn("Website", width="medium"),
                    "email": st.column_config.TextColumn("Email", width="medium"),
                    "web_check": st.column_config.TextColumn("🌐 Web", width="small"),
                    "email_check": st.column_config.TextColumn("📧 Email", width="small"),
                    "est_monthly_revenue": st.column_config.TextColumn("Monthly RCM", width="small"),
                    "est_annual_value": st.column_config.TextColumn("Annual Value", width="small"),
                    "outreach_status": st.column_config.TextColumn("Status", width="medium"),
                    "notes": st.column_config.TextColumn("Notes", width="large"),
                }
            )
            
            # Status Update Section
            st.markdown("### 📝 Update Outreach Status")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                selected_npi = st.selectbox(
                    "Select Clinic (by NPI)",
                    options=filtered['npi'].tolist() if 'npi' in filtered.columns else [],
                    format_func=lambda npi: f"{filtered[filtered['npi']==npi]['clinic_name'].iloc[0][:30]}..." if npi else ""
                )
            
            with col2:
                new_status = st.selectbox("New Status", options=VALID_STATUSES)
            
            with col3:
                contact_date = st.date_input("Contact Date", value=datetime.now())
            
            with col4:
                if st.button("Update Status", type="primary"):
                    if selected_npi:
                        success = update_status(
                            selected_npi,
                            new_status,
                            f"Updated via dashboard on {datetime.now().strftime('%Y-%m-%d')}",
                            contact_date.strftime("%Y-%m-%d")
                        )
                        if success:
                            st.success(f"✅ Updated to: {new_status}")
                            st.rerun()
                        else:
                            st.error("Failed to update")
            
            # Notes section
            notes_input = st.text_area("Add Notes (optional)", placeholder="e.g., Spoke with Jane, sending proposal...")
            if st.button("Add Note") and selected_npi and notes_input:
                if add_note(selected_npi, notes_input):
                    st.success("✅ Note added")
                    st.rerun()
            
            # Download
            csv = filtered.to_csv(index=False)
            st.download_button(
                label=f"⬇️ Download Filtered Data ({len(filtered):,} clinics)",
                data=csv,
                file_name=f"clinics_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # ==================== DOCTORS TAB ====================
    with tab2:
        df_doctors = load_data(CSV_DOCTORS)
        
        if df_doctors is None or df_doctors.empty:
            st.warning("⚠️ No doctor data found. Click 'Refresh Doctors' to fetch data.")
            st.info("👉 Use the sidebar to refresh data from NPI Registry")
        else:
            # Filters
            st.subheader("🔍 Filters")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                all_cities_doc = sorted(df_doctors["city"].dropna().unique().tolist())
                selected_cities_doc = st.multiselect("City", options=all_cities_doc, default=[], key="doc_city")
            
            with col2:
                all_specialties = sorted(df_doctors["specialty"].dropna().unique().tolist())
                selected_specialty = st.multiselect("Specialty", options=all_specialties, default=[], key="specialty")
            
            with col3:
                billing_options_doc = ["All", "High", "Medium", "Low"]
                selected_billing_doc = st.selectbox("Billing Need", options=billing_options_doc, index=0, key="doc_billing")
            
            # Search
            search_term_doc = st.text_input("🔎 Search doctor name", "", key="doc_search")
            
            # Apply filters
            filtered_doc = df_doctors.copy()
            
            if selected_cities_doc:
                filtered_doc = filtered_doc[filtered_doc["city"].isin(selected_cities_doc)]
            if selected_specialty:
                filtered_doc = filtered_doc[filtered_doc["specialty"].isin(selected_specialty)]
            if selected_billing_doc != "All":
                filtered_doc = filtered_doc[filtered_doc["billing_prediction"] == selected_billing_doc]
            if search_term_doc:
                filtered_doc = filtered_doc[filtered_doc["doctor_name"].str.contains(search_term_doc, case=False, na=False)]
            
            # Summary
            st.subheader("📊 Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Doctors", len(df_doctors))
            with col2:
                st.metric("Filtered Results", len(filtered_doc))
            with col3:
                high_priority_doc = (df_doctors["billing_prediction"] == "High").sum()
                st.metric("High Priority", high_priority_doc)
            with col4:
                specialties_count = df_doctors["specialty"].nunique()
                st.metric("Specialties", specialties_count)
            
            # Data table
            st.subheader("🗂️ Doctor List")
            
            # Add status and notes columns
            if 'npi' in filtered_doc.columns:
                filtered_doc['outreach_status'] = filtered_doc['npi'].apply(
                    lambda npi: get_status(npi)['status'] if get_status(npi) else "Not Contacted"
                )
                filtered_doc['notes'] = filtered_doc['npi'].apply(
                    lambda npi: get_status(npi)['notes'] if get_status(npi) and get_status(npi).get('notes') else ""
                )
            
            display_cols_doc = ["doctor_name", "credentials", "specialty", "city", 
                               "phone", "practice_type", "billing_prediction"]
            
            # Add status and notes if available
            if 'outreach_status' in filtered_doc.columns:
                display_cols_doc.append("outreach_status")
            if 'notes' in filtered_doc.columns:
                display_cols_doc.append("notes")
                
            display_cols_doc = [c for c in display_cols_doc if c in filtered_doc.columns]
            
            st.dataframe(
                filtered_doc[display_cols_doc],
                use_container_width=True,
                height=500,
                hide_index=True,
                column_config={
                    "doctor_name": st.column_config.TextColumn("Doctor Name", width="large"),
                    "credentials": st.column_config.TextColumn("Credentials", width="small"),
                    "specialty": st.column_config.TextColumn("Specialty", width="medium"),
                    "outreach_status": st.column_config.TextColumn("Status", width="medium"),
                    "notes": st.column_config.TextColumn("Notes", width="large"),
                }
            )
            
            # Status Update Section for Doctors
            st.markdown("### 📝 Update Outreach Status")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                selected_doc_npi = st.selectbox(
                    "Select Doctor (by NPI)",
                    options=filtered_doc['npi'].tolist() if 'npi' in filtered_doc.columns else [],
                    format_func=lambda npi: f"{filtered_doc[filtered_doc['npi']==npi]['doctor_name'].iloc[0][:30]}..." if npi else "",
                    key="doc_npi_select"
                )
            
            with col2:
                new_status_doc = st.selectbox("New Status", options=VALID_STATUSES, key="doc_status")
            
            with col3:
                contact_date_doc = st.date_input("Contact Date", value=datetime.now(), key="doc_date")
            
            with col4:
                if st.button("Update Status", type="primary", key="doc_update"):
                    if selected_doc_npi:
                        success = update_status(
                            selected_doc_npi,
                            new_status_doc,
                            f"Updated via dashboard on {datetime.now().strftime('%Y-%m-%d')}",
                            contact_date_doc.strftime("%Y-%m-%d")
                        )
                        if success:
                            st.success(f"✅ Updated to: {new_status_doc}")
                            st.rerun()
                        else:
                            st.error("Failed to update")
            
            # Notes section for doctors
            notes_input_doc = st.text_area("Add Notes (optional)", placeholder="e.g., Called Dr. Smith, interested in proposal...", key="doc_notes")
            if st.button("Add Note", key="doc_add_note") and selected_doc_npi and notes_input_doc:
                if add_note(selected_doc_npi, notes_input_doc):
                    st.success("✅ Note added")
                    st.rerun()
            
            # Download
            csv_doc = filtered_doc.to_csv(index=False)
            st.download_button(
                label="⬇️ Download Filtered Data",
                data=csv_doc,
                file_name=f"doctors_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_doctors"
            )


if __name__ == "__main__":
    main()
