"""
Refresh All Data - Clinics and Doctors
Run this to update both datasets at once
"""

import subprocess
import sys

print("\n" + "=" * 80)
print("  DATA REFRESH UTILITY")
print("=" * 80)
print("\nRefreshing all behavioral health data for Illinois...\n")

# Run clinic scraper
print("🏥 STEP 1: Fetching Clinics/Organizations")
print("=" * 80)
result1 = subprocess.run([sys.executable, "scrape_clinics.py"])

if result1.returncode != 0:
    print("\n⚠️  Clinic scraper failed!")
else:
    print("\n✅ Clinics updated successfully!")

print("\n" + "=" * 80)

# Run doctor scraper
print("\n👨‍⚕️ STEP 2: Fetching Individual Doctors")
print("=" * 80)
result2 = subprocess.run([sys.executable, "scrape_doctors.py"])

if result2.returncode != 0:
    print("\n⚠️  Doctor scraper failed!")
else:
    print("\n✅ Doctors updated successfully!")

print("\n" + "=" * 80)
print("  REFRESH COMPLETE")
print("=" * 80)

if result1.returncode == 0 and result2.returncode == 0:
    print("\n✅ All data refreshed successfully!")
    print("\nYou now have:")
    print("  • il_behavioral_health_clinics.csv")
    print("  • il_behavioral_health_doctors.csv")
    print("\n💡 Next: Run 'streamlit run app.py' to view the data")
else:
    print("\n⚠️  Some scrapers failed. Check error messages above.")

print("\n" + "=" * 80 + "\n")
