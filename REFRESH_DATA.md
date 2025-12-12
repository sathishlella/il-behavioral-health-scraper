# 🔄 How to Fetch New Data

## Option 1: Refresh Clinic List (Organizations)

To get updated clinic data, just run the scraper again:

```bash
python scrape_clinics.py
```

This will:
- Query the NPI Registry for current data
- Overwrite `il_behavioral_health_clinics.csv` with fresh data
- Include any new clinics added to NPI since last run
- Update existing clinic information

**How often to refresh:**
- Weekly: Get new clinics
- Monthly: Keep data current
- Before major outreach campaigns

---

## Option 2: Fetch Individual Doctors

The current scraper focuses on **organizations (clinics)**. To get **individual doctors**, I've created a new scraper!

### Run the Doctors Scraper:

```bash
python scrape_doctors.py
```

**Output:** `il_behavioral_health_doctors.csv` with individual practitioners

### What You'll Get:

- Psychiatrists (MD, DO)
- Psychologists (PhD, PsyD)
- Clinical Social Workers (LCSW)
- Mental Health Counselors (LCPC, LPC)
- Substance Abuse Counselors

**Fields:**
- Doctor Name
- Credentials (MD, PhD, LCSW, etc.)
- Specialty (Psychiatry, Psychology, etc.)
- Practice Address
- Phone Number
- Solo or Group Practice
- Billing Prediction

---

## Option 3: Get Both Clinics AND Doctors

Run both scrapers:

```bash
# Get clinics/organizations
python scrape_clinics.py

# Get individual doctors
python scrape_doctors.py
```

You'll have two CSV files:
- `il_behavioral_health_clinics.csv` - Organizations
- `il_behavioral_health_doctors.csv` - Individual providers

---

## Automating Data Refresh

### Windows Task Scheduler (Weekly Updates)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Refresh Clinic Data"
4. Trigger: Weekly
5. Action: Start a program
   - Program: `python`
   - Arguments: `scrape_clinics.py`
   - Start in: `d:\Student Assignments\student_protfolios\Medexa_healthCare\Tools\Velden Scraper`

### Python Script (Run Both)

Create `refresh_all_data.py`:

```python
import subprocess

print("🔄 Refreshing clinic data...")
subprocess.run(["python", "scrape_clinics.py"])

print("\n🔄 Refreshing doctor data...")
subprocess.run(["python", "scrape_doctors.py"])

print("\n✅ All data refreshed!")
```

Run: `python refresh_all_data.py`

---

## Customizing Your Search

### Get More Records

Edit `scrape_clinics.py` or `scrape_doctors.py`:

```python
# Change this line
for p in range(1, min(10, count // 200 + 1)):  # Currently gets 10 pages

# To get more
for p in range(1, min(20, count // 200 + 1)):  # Gets 20 pages (more data)
```

### Search Different States

```python
# Change state
STATE = "CA"  # California
STATE = "NY"  # New York
STATE = "TX"  # Texas
```

### Focus on Specific Specialties

Edit the taxonomy searches:

```python
# In scrape_doctors.py, change:
tax_searches = ["psychiatry", "psychology"]  # Only psychiatrists and psychologists
```

---

## Data Quality Tips

### After Fetching New Data

1. **Check record count:**
   ```bash
   python -c "import pandas as pd; print(f'Clinics: {len(pd.read_csv(\"il_behavioral_health_clinics.csv\"))}')"
   ```

2. **Remove duplicates:**
   The scraper already does this by NPI, but you can double-check

3. **Validate critical data:**
   - Check phone numbers are formatted
   - Verify cities are in Illinois
   - Ensure no missing NPIs

### Merging Old and New Data

If you want to keep historical data:

```python
import pandas as pd

# Load old and new
old = pd.read_csv("il_behavioral_health_clinics_backup.csv")
new = pd.read_csv("il_behavioral_health_clinics.csv")

# Combine and remove duplicates by NPI
combined = pd.concat([old, new]).drop_duplicates(subset=['npi'], keep='last')
combined.to_csv("il_behavioral_health_clinics_merged.csv", index=False)
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Refresh clinics | `python scrape_clinics.py` |
| Get doctors | `python scrape_doctors.py` |
| Get both | `python refresh_all_data.py` |
| Check data | View CSV in Excel/dashboard |

---

**Next:** Run `python scrape_doctors.py` to get individual practitioners! 👨‍⚕️
