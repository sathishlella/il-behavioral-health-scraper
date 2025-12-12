# 🏥 Illinois Behavioral Health Clinic Scraper

> Automated tool to collect comprehensive data about small outpatient behavioral health clinics in Illinois for medical billing outreach.

[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📊 What It Does

This tool scrapes the **NPI Registry** to find behavioral health clinics in Illinois and enriches the data with:

- ✅ Clinic Names & Practice Types
- ✅ Complete Addresses & Phone Numbers
- ✅ Inferred Websites & Emails
- ✅ Clinic Size Estimates (Solo vs Small Group)
- ✅ Medical Billing Need Predictions (High/Medium/Low)

**Perfect for:** Medical billing services looking to build a client pipeline.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/il-behavioral-health-scraper.git
cd il-behavioral-health-scraper

# Install dependencies
pip install -r requirements.txt
```

### Run the Scraper

```bash
python scrape_clinics.py
```

**Output:** `il_behavioral_health_clinics.csv` with 200+ clinics

### View the Dashboard

```bash
streamlit run app.py
```

Opens an interactive dashboard at `http://localhost:8501`

## 📁 Files

| File | Description |
|------|-------------|
| `scrape_clinics.py` | Main scraper script |
| `app.py` | Streamlit dashboard |
| `il_behavioral_health_clinics.csv` | Collected clinic data (224 clinics) |
| `requirements.txt` | Python dependencies |
| `DEPLOYMENT.md` | Deployment guide for Git/Streamlit Cloud |
| `QUICK_START.md` | Quick reference guide |

## 🎯 Features

### Scraper
- Searches NPI Registry by mental health taxonomies
- Filters for small outpatient clinics only
- Removes large hospital systems and government entities
- Handles pagination and deduplication
- Respectful rate limiting

### Dashboard
- **Filters:** City, clinic size, billing prediction
- **Search:** Find clinics by name
- **Visualizations:** Charts for size/billing/location distribution
- **Detail View:** Individual clinic profiles
- **Export:** Download filtered results as CSV

### Data Enrichment
- **Website Inference:** Generates likely URLs from clinic names
- **Email Inference:** Creates contact emails from domains
- **Size Detection:** Analyzes names for group indicators
- **Billing Prediction:** Heuristic model for service need

## 📊 Sample Output

```csv
clinic_name,practice_type,city,phone,website,clinic_size,billing_prediction
ADDISON BEHAVIORAL HEALTH LLC,Mental Health Clinic,ADDISON,(630) 306-2626,www.addisonbehavioralhealth.com,Solo or Small,Medium
ABSOLUTE MEDICAL & DIAGNOSTIC CENTER,Psychiatry & Neurology,ARLINGTON HEIGHTS,(847) 870-8955,www.absolutemedical.com,Small Group,High
```

**Current Dataset:** 224 clinics across 130+ Illinois cities

## ⚠️ Important Notes

### Data Validation Required

> **WARNING:** Websites and emails are INFERRED from clinic names and may not be accurate.

**Before using for outreach:**
1. Verify websites exist and belong to the correct clinic
2. Find actual contact emails on clinic websites
3. Update your records with validated information

### Data Source

- **Source:** Official NPI Registry (public U.S. provider database)
- **Coverage:** Illinois only
- **Focus:** Behavioral health organizations
- **Excluded:** Large hospitals, government agencies

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free!)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. **Main file:** `app.py`
6. Click Deploy!

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.**

## 🛠️ Customization

### Change State

Edit `scrape_clinics.py`:
```python
STATE = "CA"  # Change to any US state
```

### Adjust Filters

Edit filtering logic in `extract()` function to include/exclude different clinic types.

### Get More Results

Increase pagination in the scraper:
```python
# Get more pages per search
for p in range(1, min(10, count // 200 + 1)):  # Change 10 to higher number
```

## 📈 Roadmap

- [ ] Add actual web scraping for verified websites
- [ ] Integrate Google Maps API for validation
- [ ] Email validation API integration
- [ ] Multi-state support in dashboard
- [ ] Automated weekly data updates via GitHub Actions
- [ ] Export to CRM integrations

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

MIT License - feel free to use for personal or commercial purposes.

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/il-behavioral-health-scraper/issues)
- **Questions:** Check [DEPLOYMENT.md](DEPLOYMENT.md) and [QUICK_START.md](QUICK_START.md)
- **NPI API Docs:** [NPI Registry API](https://npiregistry.cms.hhs.gov/api-page)

## 📧 Contact

Built for medical billing outreach pipeline development.

---

**⭐ Star this repo if you find it useful!**
