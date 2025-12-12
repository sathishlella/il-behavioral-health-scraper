"""
Quick test to verify dashboard can be imported
"""
import sys
import os

print("Testing dashboard components...\n")

# Test imports
try:
    import pandas as pd
    print("✓ pandas installed")
except ImportError:
    print("✗ pandas NOT installed - run: pip install pandas")

try:
    import streamlit as st
    print("✓ streamlit installed")
except ImportError:
    print("✗ streamlit NOT installed - run: pip install streamlit")

# Test files exist
files_needed = [
    "app.py",
    "scrape_clinics.py",
    "scrape_doctors.py",
    "il_behavioral_health_clinics.csv",
    "il_behavioral_health_doctors.csv"
]

print("\nChecking files...")
for file in files_needed:
    if os.path.exists(file):
        print(f"✓ {file} exists")
    else:
        print(f"✗ {file} MISSING")

print("\n" + "=" * 50)
print("To run the dashboard:")
print("  streamlit run app.py")
print("\nOr if streamlit isn't in PATH:")
print("  python -m streamlit run app.py")
print("=" * 50)
