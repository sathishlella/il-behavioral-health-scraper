# 🌐 Website Contact Enrichment Guide

## What It Does

Scrapes **real emails and phone numbers** from clinic websites and adds them to your CSV.

**Before:**
- `email`: contact@clinicname.com (inferred/guessed)
- `phone`: (312) 555-1234 (from NPI registry)

**After:**
- `email`: contact@clinicname.com (inferred)
- `email_actual`: info@realclinic.com ✅ (scraped from website)
- `phone`: (312) 555-1234 (NPI)
- `phone_actual`: (312) 555-9999 ✅ (scraped from website)

---

## 🚀 How to Use

### Step 1: Run Basic Test (10 clinics)
```bash
python enrich_contacts.py
```

This tests on 10 clinics to make sure it works.

### Step 2: Run on All Clinics
```bash
python enrich_contacts.py il_behavioral_health_clinics.csv
```

This processes ALL clinics (takes ~10-15 minutes for 305 clinics).

### Step 3: Run on Specific Number
```bash
python enrich_contacts.py il_behavioral_health_clinics.csv 50
```

Processes first 50 clinics.

---

## ⚙️ How It Works

**For each clinic:**

1. **Visits website** (if available)
2. **Checks multiple pages:**
   - Homepage
   - /contact page
   - /contact-us page
   - /about page

3. **Extracts:**
   - Email addresses (using regex + mailto: links)
   - Phone numbers (US format)

4. **Filters out:**
   - Spam emails (example.com, test.com)
   - Invalid phone numbers
   - Duplicates

5. **Adds to CSV:**
   - `email_actual` - First email found
   - `phone_actual` - First phone found
   - `scrape_status` - Success/Failed/Error

---

## 📊 Expected Results

**Success Rate:** ~60-70%
- ✅ 60-70% of clinics will have actual contacts found
- ⏭️ 20-30% have no website or website down
- ❌ 10% have websites but no contacts visible

**Example Output:**
```
1/305: ABC Therapy Center              ✅ Email: info@abctherapy.com 📞 Phone: (312) 555-0123
2/305: XYZ Counseling                   ⏭️  No website
3/305: Smith Psychology LLC             ✅ Email: dr.smith@smithpsych.com
...
```

---

## 💡 Pro Tips

### Tip 1: Start Small
Test with 10-20 clinics first to see results before running all 305.

### Tip 2: Run During Off-Hours
Takes ~3 seconds per clinic, so:
- 10 clinics = 30 seconds
- 50 clinics = 2.5 minutes
- 305 clinics = 15 minutes

### Tip 3: Verify High-Value First
```bash
# Filter to high-value prospects first, then enrich
python enrich_contacts.py il_behavioral_health_clinics.csv 50
```

### Tip 4: Backup First
The script updates your CSV, so make a backup:
```bash
copy il_behavioral_health_clinics.csv il_behavioral_health_clinics_backup.csv
python enrich_contacts.py
```

---

## 🎯 Updated Dashboard

After enrichment, your dashboard will show:

| Clinic | Email (inferred) | Email (actual) ✅ | Phone (NPI) | Phone (actual) ✅ |
|--------|------------------|-------------------|-------------|-------------------|
| ABC Therapy | contact@abc.com | info@abctherapy.com | (312) 555-0001 | (312) 555-9999 |

**Benefits:**
- ✅ Real, working contact info
- ✅ Higher response rates
- ✅ Look more professional
- ✅ No more bounced emails

---

## ⚠️ Important Notes

### Rate Limiting
- Script waits 1 second between clinics
- Respects websites (doesn't hammer servers)
- Some websites may block automated requests (shows as "Failed")

### Data Quality
- Not all websites have contact info visible
- Some use contact forms instead of email
- Phone numbers may be office vs. billing

### Manual Verification
- Still verify important contacts manually
- Some scraped emails may be general inquiries
- Direct contact is always better

---

## 🔄 Re-run Anytime

You can re-run enrichment:
```bash
python enrich_contacts.py
```

It will update existing `email_actual` and `phone_actual` columns.

---

## 📈 Workflow Integration

**Recommended Process:**

1. **Run scraper** → Get 305 clinics
2. **Filter high-value** → Sort by revenue, billing prediction
3. **Enrich top 50** → Get real contacts for best prospects
4. **Start outreach** → Use actual emails/phones
5. **Track results** → Update status in dashboard
6. **Enrich more** → As you work through list

---

**This gives you REAL contact info automatically!** 🎉

Run `python enrich_contacts.py` to start!
