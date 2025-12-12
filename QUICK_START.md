# Quick Start Guide

## ✅ Your Data is Ready!

📁 **File:** `il_behavioral_health_clinics.csv`  
📊 **Clinics:** 224 behavioral health clinics in Illinois  

## 🚀 How to Use

### Option 1: View in Excel/Sheets
Just open the CSV file directly!

### Option 2: Interactive Dashboard

```bash
streamlit run app.py
```

Then open your browser to the URL shown (usually http://localhost:8501)

**Dashboard Features:**
- Filter by city, clinic size, billing prediction
- Search clinic names
- View detailed clinic profiles
- Download filtered results

## 📋 Data Fields

| Field | What It Is |
|-------|-------------|
| `clinic_name` | Organization name |
| `practice_type` | What services they offer |
| `address`, `city`, `state`, `postal_code` | Full address |
| `phone` | Phone number (formatted) |
| `website` | ⚠️ INFERRED - needs validation |
| `email` | ⚠️ INFERRED - needs validation |
| `clinic_size` | Solo or Small Group |
| `billing_prediction` | High/Medium (likelihood they need billing services) |
| `npi` | National Provider ID |

## 🎯 Recommended Workflow

### 1. Find High-Priority Clinics

Filter for:
- **Billing Prediction:** High
- **Clinic Size:** Small Group

These are your best prospects!

### 2. Validate Contact Info

> **IMPORTANT:** Websites and emails are inferred (guessed) from clinic names.  
> You MUST validate them before outreach!

**How to validate:**
1. Google the clinic name + city
2. Visit the actual website
3. Find their real contact page/email
4. Update your records

### 3. Start Outreach

- Use the validated emails
- Mention their specific services (practice_type)
 - Tailor pitch to clinic size (solo vs group)

## 📊 Quick Stats

Run this to see the data:
```bash
python -c "import pandas as pd; df=pd.read_csv('il_behavioral_health_clinics.csv'); print(f'Total: {len(df)}'); print(f'High Priority: {(df['billing_prediction']==\"High\").sum()}'); print('\nTop Cities:'); print(df['city'].value_counts().head(10))"
```

## 🔄 Get More Data

To collect more clinics:
```bash
python scrape_clinics.py
```

This will refresh the data from the NPI Registry.

## ❓ Need Help?

- See [README.md](README.md) for detailed documentation
- See [walkthrough.md](C:\Users\Sathish\.gemini\antigravity\brain\f5a36ce3-3545-44b4-8354-9cd528ed9cc5\walkthrough.md) for technical details
- Review the CSV directly to understand the data

---

**You're all set! Start reviewing the data and prioritize your outreach list! 🎉**
