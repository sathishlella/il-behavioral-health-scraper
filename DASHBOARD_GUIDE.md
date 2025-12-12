# 🎛️ Enhanced Dashboard with Data Refresh

## 🎉 What's New

Your Streamlit dashboard now has **built-in data refresh buttons**! No more running scripts in the terminal.

## ✨ New Features

### 1. **Data Refresh Buttons** (in Sidebar)

- **🏢 Refresh Clinics** - Updates clinic data from NPI Registry
- **👨‍⚕️ Refresh Doctors** - Updates doctor data from NPI Registry  
- **🔄 Refresh Both** - Updates everything at once

### 2. **Dual Tabs**

- **Clinics/Organizations Tab** - View and filter clinics
- **Individual Doctors Tab** - View and filter doctors

### 3. **Last Updated Timestamps**

See when data was last refreshed in the sidebar

### 4. **Real-Time Progress**

Watch scraper progress right in the dashboard

## 🚀 How to Use

### Start the Dashboard

```bash
streamlit run app.py
```

Or if streamlit isn't in PATH:

```bash
python -m streamlit run app.py
```

### Refresh Data

1. Open the dashboard
2. Look at the **sidebar** on the left
3. Click refresh button:
   - **Refresh Clinics** - Get updated clinic data
   - **Refresh Doctors** - Get updated doctor data
   - **Refresh Both** - Update everything

4. Wait for progress (shows in dashboard)
5. Data automatically reloads when done!

### View Data

**Clinics Tab:**
- Filter by city, size, billing prediction
- Search by clinic name
- Download filtered results

**Doctors Tab:**
- Filter by city, specialty, billing prediction
- Search by doctor name
- Download filtered results

## 📊 Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│  🏥 Velden Health – IL Behavioral Health Pipeline      │
├───────────────┬─────────────────────────────────────────┤
│ SIDEBAR       │  MAIN CONTENT                           │
│               │                                          │
│ Data Mgmt:    │  Tabs: [Clinics] [Doctors]             │
│ ┌───────────┐ │  ┌────────────────────────────────────┐│
│ │ 🏢 Refresh││  │ Filters:                           ││
│ │  Clinics  ││  │ City | Size | Billing | Search     ││
│ └───────────┘ │  └────────────────────────────────────┘│
│ ┌───────────┐ │  ┌────────────────────────────────────┐│
│ │ 👨‍⚕️ Refresh││  │ Summary:                           ││
│ │  Doctors  ││  │ Total | Filtered | High | Email    ││
│ └───────────┘ │  └────────────────────────────────────┘│
│ ┌───────────┐ │  ┌────────────────────────────────────┐│
│ │🔄 Refresh ││  │ Data Table                         ││
│ │   Both    ││  │ [Scrollable list of clinics/docs]  ││
│ └───────────┘ │  └────────────────────────────────────┘│
│               │  [⬇️ Download Filtered Data]           │
│ Last Updated: │                                          │
│ Clinics: ...  │                                          │
│ Doctors: ...  │                                          │
└───────────────┴─────────────────────────────────────────┘
```

## 🎯 Typical Workflow

### Initial Setup
1. Start dashboard: `streamlit run app.py`
2. Click **"🔄 Refresh Both"** to get data
3. Wait 3-5 minutes for  both scrapers to complete

### Weekly Updates
1. Open dashboard
2. Click **"🔄 Refresh Both"**
3. Get coffee ☕
4. Come back to fresh data!

### Targeted Updates
- Only need clinics? Click **"🏢 Refresh Clinics"**
- Only need doctors? Click **"👨‍⚕️ Refresh Doctors"**

## 💡 Pro Tips

### 1. **Monitor Progress**

When you click a refresh button:
- 🔄 Progress indicator appears
- You'll see scraper output in an expandable section
- ✅ Success message when done
- ❌ Error message if something goes wrong

### 2. **Download Filtered Data**

1. Apply filters (city, size, billing, etc.)
2. Click **"⬇️ Download Filtered Data"**
3. Get CSV with only filtered records
4. Import to your CRM!

### 3. **Check Last Updated**

Sidebar shows when data was last refreshed:
- **Clinics:** Last updated 2025-12-13 02:15
- **Doctors:** Last updated 2025-12-13 02:18

### 4. **Switch Between Clinics & Doctors**

Click tabs at top to switch:
- **🏢 Clinics/Organizations** - 224 records
- **👨‍⚕️ Individual Doctors** - 197 records

## ⚙️ Configuration

### Increase Scraper Timeout

If scraping takes > 5 minutes, edit `app.py`:

```python
# Find this line:
timeout=300  # 5 minute timeout

# Change to:
timeout=600  # 10 minute timeout
```

### Auto-Refresh Schedule

Want automatic daily updates? Use Task Scheduler (Windows) or cron (Linux/Mac) to run:

```bash
python scrape_clinics.py
python scrape_doctors.py
```

Then just view updated data in the dashboard!

## 🆘 Troubleshooting

### "Streamlit not recognized"

Run with:
```bash
python -m streamlit run app.py
```

### Refresh Button Does Nothing

- Check if scraper files (`scrape_clinics.py`, `scrape_doctors.py`) exist
- Look for error messages in expandable "View error details"

### Data Not Updating

- Wait for green ✅ success message
- Check "Last Updated" timestamp in sidebar
- Try manually: `python scrape_clinics.py`

### Timeout Error

- Normal for large datasets
- Increase timeout in `app.py` (see Configuration above)
- Or run scrapers manually in terminal

## 🎉 Benefits

✅ **No Terminal Needed** - Everything in the UI  
✅ **Visual Progress** - See what's happening  
✅ **Automatic Reload** - Data updates instantly  
✅ **Dual View** - Clinics and doctors in one place  
✅ **Easy Filtering** - Find exactly what you need  
✅ **Quick Export** - Download filtered results  

## 📝 Technical Details

### How It Works

1. **Button Click** → Triggers `run_scraper()` function
2. **Subprocess** → Runs Python scraper script
3. **Progress Tracking** → Shows status in UI
4. **Cache Clear** → Clears Streamlit cache
5. **Auto Rerun** → Reloads dashboard with new data

### Files Used

- `app.py` - Dashboard with refresh buttons
- `scrape_clinics.py` - Clinic scraper
- `scrape_doctors.py` - Doctor scraper
- `il_behavioral_health_clinics.csv` - Clinic data
- `il_behavioral_health_doctors.csv` - Doctor data

---

**🎉 Enjoy your new self-service data refresh dashboard!**

No more command line needed - just click and wait for fresh data! 🚀
