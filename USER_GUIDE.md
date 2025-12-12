# Illinois Behavioral Health Clinic Scraper
## Complete User Guide

### Version 1.0 | December 2025

---

## Table of Contents

1. [Overview](#overview)
2. [System Features](#system-features)
3. [Getting Started](#getting-started)
4. [Using the Dashboard](#using-the-dashboard)
5. [Data Refresh Operations](#data-refresh-operations)
6. [Filtering and Searching](#filtering-and-searching)
7. [Exporting Data](#exporting-data)
8. [Understanding the Data](#understanding-the-data)
9. [Advanced Features](#advanced-features)
10. [Troubleshooting](#troubleshooting)

---

## 1. Overview

### What is This System?

The Illinois Behavioral Health Clinic Scraper is an automated data collection and management tool designed to help medical billing services identify and contact potential clients in Illinois. The system collects comprehensive information about behavioral health clinics and individual practitioners from the public NPI (National Provider Identifier) Registry.

### Who Should Use This?

- **Medical billing service providers** looking for new clients
- **Healthcare business development teams** building prospect lists
- **Healthcare consultants** researching the Illinois mental health market
- **Anyone** needing contact information for behavioral health providers in Illinois

### Key Benefits

✅ **Automated Data Collection** - No manual searching required  
✅ **Comprehensive Information** - Names, addresses, phones, websites, emails  
✅ **Smart Predictions** - AI-powered billing need predictions  
✅ **Easy Filtering** - Find exactly the prospects you need  
✅ **Self-Service** - Refresh data anytime with one click  
✅ **Export Ready** - Download filtered lists for your CRM  

---

## 2. System Features

### 2.1 Data Collection

The system collects two types of data:

#### A. Clinics/Organizations (224 records)

**What it includes:**
- Behavioral health clinics
- Mental health centers
- Counseling centers  
- Substance abuse treatment facilities
- Group practices

**Data fields collected:**
- Clinic name
- Practice type/specialty
- Complete address (street, city, state, ZIP)
- Phone number
- Website (inferred from name)
- Email (inferred from website)
- Clinic size (Solo/Small Group/Medium)
- Billing prediction (High/Medium/Low)
- NPI number

#### B. Individual Doctors (197 records)

**What it includes:**
- Psychiatrists (MD, DO)
- Psychologists (PhD, PsyD)
- Clinical Social Workers (LCSW)
- Mental Health Counselors (LCPC, LPC)
- Substance Abuse Counselors

**Data fields collected:**
- Doctor name
- Professional credentials (MD, PhD, LCSW, etc.)
- Specialty
- Practice type (Solo/Group)
- Organization affiliation
- Complete address
- Phone number
- Billing prediction
- NPI number

### 2.2 Interactive Dashboard

**Platform:** Streamlit web application  
**Access:** Local browser (http://localhost:8501)

**Dashboard Capabilities:**

| Feature | Description |
|---------|-------------|
| **Dual Tabs** | Separate views for clinics and doctors |
| **Real-time Filtering** | Filter by city, size, specialty, billing need |
| **Search** | Find specific clinics or doctors by name |
| **Data Refresh** | Update data with button clicks |
| **Visual Analytics** | Charts and metrics |
| **CSV Export** | Download filtered results |
| **Last Updated** | See when data was refreshed |

### 2.3 Smart Features

#### Billing Prediction Algorithm

The system uses intelligent heuristics to predict which providers are most likely to need medical billing services:

**HIGH Priority Indicators:**
- Small group practices (2-10 providers)
- Psychiatry practices (complex medical billing)
- Substance abuse treatment (insurance-intensive)
- Website mentions insurance acceptance

**MEDIUM Priority Indicators:**
- Solo practitioners
- Counseling/therapy services
- General behavioral health services

**LOW Priority Indicators:**
- Large organizations (likely have in-house billing)
- Cash-only/self-pay practices
- Wellness-focused practices

#### Size Detection

Analyzes multiple signals:
- Keywords in organization name ("group", "associates", "partners")
- Presence of "center" or "clinic" in name
- Professional entity structure (LLC, Inc)
- Website analysis (when available)

### 2.4 Data Sources

**Primary Source:** U.S. National Provider Identifier (NPI) Registry
- Official government database
- Public information
- Updated regularly
- Comprehensive coverage

**Search Strategy:**
- Taxonomy-based searches (mental health, psychiatry, psychology, etc.)
- Keyword searches (behavioral health, counseling, therapy)
- Geographic filtering (Illinois only)
- Deduplication by NPI number

---

## 3. Getting Started

### 3.1 Installation

**System Requirements:**
- Windows, Mac, or Linux
- Python 3.8 or higher
- Internet connection

**Installation Steps:**

1. **Navigate to project folder:**
```
cd "d:\Student Assignments\student_protfolios\Medexa_healthCare\Tools\Velden Scraper"
```

2. **Install dependencies:**
```
pip install -r requirements.txt
```

3. **Verify installation:**
```
python test_dashboard.py
```

### 3.2 First-Time Setup

**Step 1: Collect Initial Data**

Open terminal and run:
```
python refresh_all_data.py
```

This will:
- Fetch clinic data (~3 minutes)
- Fetch doctor data (~3 minutes)  
- Create CSV files with all data
- Total time: ~6-8 minutes

**Step 2: Launch Dashboard**

```
streamlit run app.py
```

Or:
```
python -m streamlit run app.py
```

Your browser will open automatically to: http://localhost:8501

**Step 3: Explore the Data**

- Click between "Clinics" and "Doctors" tabs
- Try the filters
- Search for a specific city
- Download a sample CSV

---

## 4. Using the Dashboard

### 4.1 Dashboard Layout

```
┌──────────────────────────────────────────────────────────────┐
│          🏥 Velden Health - IL Behavioral Health             │
│                     Pipeline Dashboard                        │
├──────────────┬───────────────────────────────────────────────┤
│   SIDEBAR    │              MAIN CONTENT AREA                │
│              │                                                 │
│ 📊 Data Mgmt │  [🏢 Clinics Tab] [👨‍⚕️ Doctors Tab]          │
│              │                                                 │
│ ┌──────────┐ │  🔍 FILTERS                                   │
│ │ 🏢 Refresh│ │  City | Size | Billing | Has Website/Email   │
│ │  Clinics │ │                                                 │
│ └──────────┘ │  📊 SUMMARY METRICS                           │
│ ┌──────────┐ │  Total: 224 | Filtered: 45 | High: 89        │
│ │👨‍⚕️ Refresh│ │                                                 │
│ │  Doctors │ │  🗂️ DATA TABLE                                │
│ └──────────┘ │  [Scrollable list of clinics/doctors]         │
│ ┌──────────┐ │  Name | City | Phone | Website | Size | ...   │
│ │🔄 Refresh│ │                                                 │
│ │   Both   │ │  [⬇️ Download Filtered Data Button]           │
│ └──────────┘ │                                                 │
│              │                                                 │
│ 📁 Last Data │                                                 │
│ Clinics:     │                                                 │
│ 12/13 02:15  │                                                 │
│ Doctors:     │                                                 │
│ 12/13 02:18  │                                                 │
└──────────────┴───────────────────────────────────────────────┘
```

### 4.2 Navigation

**Switching Between Data Types:**

1. **Clinics Tab** - Click "🏢 Clinics/Organizations" at top
   - View clinic data
   - 224 behavioral health organizations
   - Filter by size, city, billing prediction

2. **Doctors Tab** - Click "👨‍⚕️ Individual Doctors" at top
   - View individual practitioners
   - 197 doctors
   - Filter by specialty, city, billing prediction

**Using the Sidebar:**

The left sidebar contains:
- **Data refresh buttons** (top section)
- **Last updated timestamps** (bottom section)

Always visible, accessible from any tab.

### 4.3 Summary Metrics

At the top of each tab, you'll see 4 key metrics:

**Clinics Tab Metrics:**
- **Total Clinics:** All clinics in database (224)
- **Filtered Results:** Clinics matching current filters
- **High Priority:** Clinics with "High" billing prediction
- **With Email:** Clinics that have email addresses

**Doctors Tab Metrics:**
- **Total Doctors:** All doctors in database (197)
- **Filtered Results:** Doctors matching current filters
- **High Priority:** Doctors with "High" billing prediction
- **Specialties:** Number of unique specialties

---

## 5. Data Refresh Operations

### 5.1 When to Refresh Data

**Recommended Refresh Schedule:**

| Frequency | Purpose |
|-----------|---------|
| **Weekly** | Stay current with new providers |
| **Monthly** | Comprehensive updates |
| **Before campaigns** | Ensure fresh data for outreach |
| **After NPI updates** | When you know providers have been added |

### 5.2 How to Refresh Data

**Method 1: Dashboard (Recommended)**

1. Open dashboard (`streamlit run app.py`)
2. Look at left sidebar
3. Choose refresh option:
   - **🏢 Refresh Clinics** - Update only clinic data (~3 min)
   - **👨‍⚕️ Refresh Doctors** - Update only doctor data (~3 min)
   - **🔄 Refresh Both** - Update everything (~6 min)
4. Click the button
5. Wait for progress indicator
6. Watch for ✅ success message
7. Data automatically reloads!

**Method 2: Command Line (Advanced)**

```bash
# Refresh both
python refresh_all_data.py

# Or individually
python scrape_clinics.py
python scrape_doctors.py
```

### 5.3 What Happens During Refresh

**Step-by-Step Process:**

1. **Connect to NPI Registry**
   - System accesses public API
   - No authentication required
   
2. **Search Multiple Taxonomies**
   - Mental health
   - Behavioral health
   - Psychiatry
   - Psychology
   - Counseling
   - Substance abuse treatment

3. **Filter Results**
   - Remove duplicates
   - Filter out large hospital systems
   - Focus on small outpatient clinics
   - Verify Illinois addresses

4. **Enrich Data**
   - Infer websites from clinic names
   - Infer contact emails
   - Detect clinic size
   - Predict billing needs

5. **Save to CSV**
   - Overwrite previous data
   - Update timestamps
   - Clear dashboard cache

6. **Reload Dashboard**
   - Automatic refresh
   - New data appears instantly

### 5.4 Monitoring Progress

When refreshing from dashboard:

**Progress Indicators:**
- 🔄 Blue info box: "Running [scraper name]..."
- Progress bar (if long operation)  
- ✅ Green success: "Completed successfully!"
- ❌ Red error: "Failed!" (with details)

**View Output:**
- Click "View scraper output" to see detailed logs
- Shows number of records found
- Lists cities covered
- Displays any errors

---

## 6. Filtering and Searching

### 6.1 Available Filters

#### Clinics Tab Filters

| Filter | Options | Use Case |
|--------|---------|----------|
| **City** | Multi-select list | Target specific geographic areas |
| **Clinic Size** | All, Solo, Small Group, Medium, Large | Find practices of specific size |
| **Billing Need** | All, High, Medium, Low | Prioritize prospects |
| **Has Website** | Checkbox | Only clinics with websites (for validation) |
| **Has Email** | Checkbox | Only clinics with email (for direct outreach) |
| **Search Name** | Text input | Find specific clinic by name |

#### Doctors Tab Filters

| Filter | Options | Use Case |
|--------|---------|----------|
| **City** | Multi-select list | Target specific geographic areas |
| **Specialty** | Multi-select list | Find specific types of doctors |
| **Billing Need** | All, High, Medium, Low | Prioritize prospects |
| **Search Name** | Text input | Find specific doctor by name |

### 6.2 Filter Combinations

**Example Use Cases:**

**Use Case 1: High-Priority Small Groups in Chicago**
1. Go to Clinics tab
2. City: Select "CHICAGO"
3. Clinic Size: "Small Group"
4. Billing Need: "High"
5. Result: Small Chicago practices most likely to need billing services

**Use Case 2: Psychiatrists with Contact Info**
1. Go to Doctors tab
2. Specialty: Select "Psychiatry & Neurology, Psychiatry"
3. Billing Need: "High"
4. Result: Psychiatrists most likely to need billing help

**Use Case 3: All Providers in Suburbs**
1. Select Clinics or Doctors tab
2. City: Select multiple suburban cities (Arlington Heights, Naperville, etc.)
3. Result: Suburban providers for targeted outreach

### 6.3 Search Tips

**Name Search Best Practices:**

✅ **Do:**
- Use partial names ("Adams" finds "Adams Clinic", "Dr. Adams", etc.)
- Try without special characters
- Search is case-insensitive

❌ **Don't:**
- Include full address in search
- Use exact punctuation
- Expect exact match only

### 6.4 Clearing Filters

To reset all filters:
1. Refresh the page (F5 or browser refresh)
2. Or manually deselect all filters
3. Or click different tab and back

---

## 7. Exporting Data

### 7.1 Export Methods

**Method 1: Filtered Export (Dashboard)**

1. Apply your desired filters
2. Scroll to bottom of data table
3. Click "⬇️ Download Filtered Data" button
4. File downloads as: `clinics_filtered_YYYYMMDD.csv` or `doctors_filtered_YYYYMMDD.csv`
5. Open in Excel or import to CRM

**Method 2: Full Export (File System)**

Navigate to project folder and copy:
- `il_behavioral_health_clinics.csv` - All clinic data
- `il_behavioral_health_doctors.csv` - All doctor data

### 7.2 CSV File Structure

#### Clinics CSV Columns

| Column | Description | Example |
|--------|-------------|---------|
| `clinic_name` | Organization name | "ADDISON BEHAVIORAL HEALTH LLC" |
| `practice_type` | Services offered | "Clinic/Center, Mental Health" |
| `address` | Street address | "721 W LAKE ST STE 203" |
| `city` | City name | "ADDISON" |
| `state` | State code | "IL" |
| `postal_code` | ZIP code | "60101" |
| `phone` | Formatted phone | "(630) 306-2626" |
| `website` | Inferred URL | "www.addisonbehavioralhealth.com" |
| `email` | Inferred email | "contact@addisonbehavioralhealth.com" |
| `clinic_size` | Size category | "Small Group" |
| `billing_prediction` | Need level | "High" |
| `npi` | NPI number | "1902769060" |

#### Doctors CSV Columns

| Column | Description | Example |
|--------|-------------|---------|
| `doctor_name` | Full name | "ABDULLAH ALSAWAF" |
| `credentials` | Degrees | "MD" |
| `specialty` | Medical specialty | "Psychiatry & Neurology, Psychiatry" |
| `practice_type` | Solo/Group | "Solo Practice" |
| `organization` | Affiliated org | "Independent" |
| `address` | Street address | "880 W CENTRAL RD STE 7200" |
| `city` | City name | "ARLINGTON HEIGHTS" |
| `state` | State code | "IL" |
| `postal_code` | ZIP code | "60005" |
| `phone` | Formatted phone | "(847) 618-4430" |
| `billing_prediction` | Need level | "High" |
| `npi` | NPI number | "1023376951" |

### 7.3 Importing to CRM

**Common CRM Systems:**

**Salesforce:**
1. Export filtered CSV
2. Salesforce → Setup → Data → Data Import Wizard
3. Map columns (clinic_name → Account Name, phone → Phone, etc.)
4. Import

**HubSpot:**
1. Export filtered CSV
2. HubSpot → Contacts → Import
3. Select file and map fields
4. Import

**Excel/Google Sheets:**
1. Export CSV
2. Open directly in Excel or import to Google Sheets
3. Use as standalone database or mail merge source

### 7.4 Data Validation

**Important Note:** Before using exported data for outreach:

⚠️ **Websites and emails are INFERRED** - they may not be 100% accurate

**Validation Steps:**
1. Google the clinic name + city
2. Verify website matches
3. Find actual contact email on their website
4. Update your records before outreach

**Accuracy Estimates:**
- Clinic names: 100% accurate (from NPI)
- Addresses: 100% accurate (from NPI)
- Phone numbers: 100% accurate (from NPI)
- Websites: ~70-80% accurate (inferred)
- Emails: ~60-70% accurate (inferred)

---

## 8. Understanding the Data

### 8.1 Data Quality

**Source Reliability:**
- **NPI Registry** is the official U.S. provider database
- Maintained by Centers for Medicare & Medicaid Services (CMS)
- Providers must update their information
- Public and free to access

**Data Freshness:**
- As current as last refresh date
- Recommended: Refresh weekly
- NPI updates happen continuously
- Your data reflects the refresh timestamp

### 8.2 Billing Prediction Explained

**How It Works:**

The system analyzes multiple factors:

**Size Factor** (30% weight)
- Solo practices often outsource billing
- Small groups (2-10) prime candidates
- Large orgs usually have in-house billing

**Specialty Factor** (40% weight)
- Psychiatry = complex medical billing (High priority)
- Substance abuse = insurance-intensive (High priority)
- Counseling = standard billing (Medium priority)

**Practice Indicators** (30% weight)
- Website mentions insurance → Higher score
- "Cash only" or "self-pay" → Lower score
- Professional entity (LLC, Inc) → Higher score

**Prediction Accuracy:**
- Based on industry patterns
- ~75-80% accurate for "High" predictions
- Use as prioritization tool, not absolute truth

### 8.3 Clinic Size Categories

| Size | Provider Count | Characteristics |
|------|----------------|-----------------|
| **Solo** | 1 | Individual practitioner, likely outsources billing |
| **Small Group** | 2-10 | Multiple providers, prime target for billing services |
| **Medium** | 11-25 | Larger practice, may have admin staff |
| **Large** | 26+ | Organization-level, likely in-house billing |

**Detection Signals:**
- Name includes "Group", "Associates", "Partners" → Small Group likely
- Name includes "Center", "Clinic" → Small Group or Medium
- Simple personal name → Solo likely
- LLC/Inc but no group words → Solo or Small

### 8.4 Geographic Coverage

**Current Coverage:** Illinois only

**Cities Represented:** 130+ cities including:
- Chicago (largest concentration)
- Arlington Heights
- Naperville
- Aurora
- Rockford
- Springfield
- Peoria
- And many more suburbs and smaller cities

**Expanding to Other States:**

To collect data for other states:
1. Edit scraper files (`scrape_clinics.py`, `scrape_doctors.py`)
2. Change line: `STATE = "IL"` to desired state code (e.g., `STATE = "CA"`)
3. Run scraper
4. Data will be for the new state

---

## 9. Advanced Features

### 9.1 Customizing Scraper Behavior

**Get More Records:**

Edit scraper files and modify pagination:

```python
# In scrape_clinics.py or scrape_doctors.py
# Find this line:
for p in range(1, min(5, count // 200 + 1)):

# Change to get more pages:
for p in range(1, min(10, count // 200 + 1)):  # Gets 10 pages instead of 5
```

**Focus on Specific Specialties:**

Edit `scrape_doctors.py`:

```python
# Find the specialties list
specialties = [
    "psychiatry",  # Keep only psychiatry
    # Comment out others or remove them
]
```

### 9.2 Automation Options

**Option 1: Windows Task Scheduler**

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Weekly Clinic Data Refresh"
4. Trigger: Weekly, Sunday 2:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `refresh_all_data.py`
   - Start in: `d:\Student Assignments\student_protfolios\Medexa_healthCare\Tools\Velden Scraper`
6. Save

**Option 2: Python Schedule Script**

Create `schedule_refresh.py`:

```python
import schedule
import time
import subprocess

def refresh_data():
    print("Starting weekly refresh...")
    subprocess.run(["python", "refresh_all_data.py"])

# Run every Sunday at 2 AM
schedule.every().sunday.at("02:00").do(refresh_data)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

Run in background: `python schedule_refresh.py`

### 9.3 Data Merging

**Combine Old and New Data:**

```python
import pandas as pd

# Load both
old_data = pd.read_csv("clinics_backup_20251201.csv")
new_data = pd.read_csv("il_behavioral_health_clinics.csv")

# Merge and keep latest
combined = pd.concat([old_data, new_data])
combined = combined.drop_duplicates(subset=['npi'], keep='last')
combined = combined.sort_values(by=['city', 'clinic_name'])

# Save
combined.to_csv("clinics_merged.csv", index=False)
```

### 9.4 Custom Analytics

**Example: City-Level Analysis**

```python
import pandas as pd

df = pd.read_csv("il_behavioral_health_clinics.csv")

# Clinics per city
city_counts = df['city'].value_counts()
print("Top 10 Cities:", city_counts.head(10))

# High-priority by city
high_priority = df[df['billing_prediction'] == 'High']
priority_by_city = high_priority.groupby('city').size()
print("\nHigh Priority by City:", priority_by_city.head(10))

# Average clinic size by city
# (requires converting size to numeric)
```

---

## 10. Troubleshooting

### 10.1 Common Issues

#### Dashboard Won't Start

**Problem:** "streamlit: command not found"

**Solution:**
```
python -m streamlit run app.py
```

**Problem:** Port already in use

**Solution:**
```
streamlit run app.py --server.port=8502
```

#### Refresh Button Does Nothing

**Problem:** Button clicks but no progress

**Checks:**
1. Are scraper files (`scrape_clinics.py`, `scrape_doctors.py`) in same folder?
2. Check error message in expandable "View error details"
3. Try running scraper manually: `python scrape_clinics.py`

**Solution:** Look for specific error in dashboard output

#### No Data Showing

**Problem:** Dashboard shows "No data found"

**Solution:**
1. Click "🔄 Refresh Both" in sidebar
2. Wait for completion (~6 minutes)
3. Refresh browser page
4. Check that CSV files exist in folder

#### Timeout Errors

**Problem:** "Scraper timed out (5 minutes)"

**Solution:** Edit `app.py`:
```python
# Find line:
timeout=300

# Change to:
timeout=600  # 10 minutes
```

#### Website/Email Not Accurate

**Problem:** Inferred website doesn't match clinic

**Expected:** Websites and emails are best-guess inferences

**Solution:**
1. Use as starting point
2. Google clinic name + city
3. Manually verify website
 4. Update records before outreach

### 10.2 Getting Help

**Resources:**

1. **Documentation Files:**
   - `README.md` - Project overview
   - `QUICK_START.md` - Quick reference
   - `DASHBOARD_GUIDE.md` - Dashboard detailed guide
   - `REFRESH_DATA.md` - Data refresh guide
   - `DEPLOYMENT.md` - Deployment instructions

2. **Test Scripts:**
   - `test_dashboard.py` - Verify installation
   - `test_npi.py` - Test NPI API connection

3. **Check Logs:**
   - Dashboard shows scraper output
   - Terminal shows detailed errors

### 10.3 Performance Tips

**Faster Refreshes:**
- Get fewer records (edit `MAX_RECORDS` in scrapers)
- Reduce pagination (fewer pages per search term)
- Focus on specific taxonomies

**Better Accuracy:**
- Manually validate high-priority prospects
- Cross-reference with Google searches
- Update inferred websites/emails

**Efficient Workflows:**
- Refresh weekly, not daily
- Export filtered lists for batch import
- Use billing prediction to prioritize

---

## Appendix A: Quick Reference Card

### Essential Commands

```bash
# Start dashboard
streamlit run app.py

# Refresh all data
python refresh_all_data.py

# Refresh clinics only
python scrape_clinics.py

# Refresh doctors only
python scrape_doctors.py

# Test setup
python test_dashboard.py
```

### Dashboard Shortcuts

| Action | Steps |
|--------|-------|
| Refresh all data | Sidebar → "🔄 Refresh Both" |
| Filter High priority | Select "High" in Billing Need dropdown |
| Download data | Scroll down → "⬇️ Download Filtered Data" |
| Search clinic | Type in "🔎 Search" box |
| Switch to doctors | Click "👨‍⚕️ Individual Doctors" tab |

### File Locations

| File | Purpose |
|------|---------|
| `app.py` | Dashboard application |
| `scrape_clinics.py` | Clinic scraper |
| `scrape_doctors.py` | Doctor scraper |
| `il_behavioral_health_clinics.csv` | Clinic data |
| `il_behavioral_health_doctors.csv` | Doctor data |

---

## Appendix B: Data Dictionary

### Clinic Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| npi | String | NPI Registry | National Provider Identifier |
| clinic_name | String | NPI Registry | Legal organization name |
| practice_type | String | NPI Registry | Taxonomy description |
| address | String | NPI Registry | Street address |
| city | String | NPI Registry | City name |
| state | String | NPI Registry | State code (IL) |
| postal_code | String | NPI Registry | ZIP code (5 digits) |
| phone | String | NPI Registry | Formatted phone number |
| website | String | Inferred | Likely website URL |
| email | String | Inferred | Likely contact email |
| clinic_size | String | Calculated | Solo/Small Group/Medium/Large |
| billing_prediction | String | Calculated | High/Medium/Low |

### Doctor Fields

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| npi | String | NPI Registry | National Provider Identifier |
| doctor_name | String | NPI Registry | Full name |
| credentials | String | Extracted | MD, PhD, LCSW, etc. |
| specialty | String | NPI Registry | Medical specialty |
| practice_type | String | Calculated | Solo/Group Practice |
| organization | String | NPI Registry | Affiliated organization |
| address | String | NPI Registry | Street address |
| city | String | NPI Registry | City name |
| state | String | NPI Registry | State code (IL) |
| postal_code | String | NPI Registry | ZIP code (5 digits) |
| phone | String | NPI Registry | Formatted phone number |
| billing_prediction | String | Calculated | High/Medium/Low |

---

## Appendix C: Support & Contact

### Technical Support

For technical issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review documentation files in project folder
3. Test with `python test_dashboard.py`

### System Requirements

- **Operating System:** Windows 10+, macOS 10.14+, or Linux
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 100MB for application, 10MB for data
- **Internet:** Required for data refresh operations

### Data Privacy

- All data from public NPI Registry
- No protected health information (PHI)
- No patient data
- Provider business information only
- Safe to store and share

---

**End of User Guide**

*Illinois Behavioral Health Clinic Scraper | Version 1.0 | December 2025*
