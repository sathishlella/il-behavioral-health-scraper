# Deployment Guide

## 📦 Publishing to Git/GitHub

### 1. Initialize Git Repository

```bash
cd "d:\Student Assignments\student_protfolios\Medexa_healthCare\Tools\Velden Scraper"
git init
git add .
git commit -m "Initial commit: IL Behavioral Health Clinic Scraper"
```

### 2. Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Name it: `il-behavioral-health-scraper`
4. **Do NOT** initialize with README (we already have one)
5. Click "Create repository"

### 3. Push to GitHub

Copy the commands from GitHub and run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/il-behavioral-health-scraper.git
git branch -M main
git push -u origin main
```

## 🚀 Deploy Dashboard to Streamlit Cloud

### Prerequisites
- GitHub account (created above)
- Streamlit Cloud account (free): [share.streamlit.io](https://share.streamlit.io)

### Steps

1. **Sign up for Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign up" and connect your GitHub account

2. **Deploy Your App**
   - Click "New app"
   - Select your repository: `il-behavioral-health-scraper`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Wait for Deployment**
   - Streamlit Cloud will install dependencies from `requirements.txt`
   - Build usually takes 2-3 minutes
   - You'll get a public URL like: `https://your-app-name.streamlit.app`

4. **Share Your Dashboard**
   - Copy the URL and share with your team
   - The dashboard is now live and accessible worldwide!

### Configuration

The app will automatically:
- ✅ Install all dependencies from `requirements.txt`
- ✅ Use the `il_behavioral_health_clinics.csv` data
- ✅ Apply custom theme from `.streamlit/config.toml`

### Updating the App

When you want to update:
```bash
# Make your changes
git add .
git commit -m "Update clinic data"
git push

# Streamlit Cloud auto-redeploys on push!
```

## ⚠️ About Vercel

**Note:** Vercel is designed for Next.js/React applications, not Python/Streamlit apps.

For this Streamlit dashboard, use **Streamlit Cloud** instead (instructions above).

If you want to create a Next.js version later, let me know!

## 🔒 Security Notes

### Sensitive Data

If your clinic data contains sensitive information:

1. **Don't commit the CSV to Git:**
   ```bash
   # Add to .gitignore
   echo "il_behavioral_health_clinics.csv" >> .gitignore
   ```

2. **Use Streamlit Secrets for API keys:**
   - In Streamlit Cloud dashboard → Settings → Secrets
   - Add any API keys there instead of in code

### Public vs Private Repository

**Recommended:** Make the GitHub repo **Private** if:
- Data contains sensitive client information
- You don't want competitors to see your methodology

**Public is OK if:**
- Data is from public NPI Registry only
- You're comfortable sharing the tool

## 📊 Managing Data Updates

### Option 1: Manual Updates

1. Run `python scrape_clinics.py` locally
2. Commit the new CSV:
   ```bash
   git add il_behavioral_health_clinics.csv
   git commit -m "Update clinic data - $(date +%Y-%m-%d)"
   git push
   ```
3. Streamlit Cloud auto-updates

### Option 2: Scheduled Updates (Advanced)

Set up GitHub Actions to run the scraper weekly:

1. Create `.github/workflows/update-data.yml`
2. Schedule the scraper
3. Auto-commit results

(Let me know if you want this setup!)

## ✅ Deployment Checklist

Before deploying:

- [ ] Review CSV data (no sensitive info if public repo)
- [ ] Test dashboard locally: `streamlit run app.py`
- [ ] Commit all changes to Git
- [ ] Push to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Test live URL
- [ ] Share with team!

## 🆘 Troubleshooting

### "Module not found" error
- Check `requirements.txt` includes all packages
- Streamlit Cloud rebuilds from scratch each time

### CSV not found
- Make sure CSV is committed to Git
- Check file path in `app.py` matches CSV filename

### App not updating
- Clear cache in Streamlit Cloud settings
- Click "Reboot app"

## 📞 Getting Help

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- GitHub Docs: https://docs.github.com

---

**You're ready to deploy! 🎉**

Start with Git/GitHub, then deploy to Streamlit Cloud for a live dashboard!
