"""
Outreach Tracking System for Velden Health RCM
Manages prospect status, contact dates, and notes
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

TRACKING_FILE = "outreach_tracking.json"

# Valid status options
VALID_STATUSES = [
    "Not Contacted",
    "Contacted",
    "Follow-up Scheduled",
    "Meeting Scheduled",
    "Proposal Sent",
    "Negotiating",
    "Won",
    "Lost",
    "Not Interested"
]


def load_tracking() -> Dict:
    """Load tracking data from JSON file."""
    if os.path.exists(TRACKING_FILE):
        try:
            with open(TRACKING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_tracking(data: Dict):
    """Save tracking data to JSON file."""
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def update_status(npi: str, status: str, notes: str = "", contact_date: str = None):
    """
    Update tracking status for a clinic.
    
    Args:
        npi (str): Clinic NPI number (unique ID)
        status (str): New status from VALID_STATUSES
        notes (str): Optional notes about this update
        contact_date (str): Date of contact (YYYY-MM-DD), defaults to today
    
    Returns:
        bool: Success status
    """
    if status not in VALID_STATUSES:
        return False
    
    tracking = load_tracking()
    
    if contact_date is None:
        contact_date = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize or update record
    if npi not in tracking:
        tracking[npi] = {
            "status": status,
            "contact_date": contact_date,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "history": []
        }
    else:
        # Save history
        tracking[npi]["history"].append({
            "old_status": tracking[npi]["status"],
            "new_status": status,
            "date": datetime.now().isoformat(),
            "notes": notes
        })
        
        tracking[npi]["status"] = status
        tracking[npi]["contact_date"] = contact_date
        if notes:
            tracking[npi]["notes"] = notes
        tracking[npi]["updated_at"] = datetime.now().isoformat()
    
    save_tracking(tracking)
    return True


def get_status(npi: str) -> Optional[Dict]:
    """
    Get tracking status for a clinic.
    
    Args:
        npi (str): Clinic NPI number
    
    Returns:
        dict or None: Tracking data or None if not found
    """
    tracking = load_tracking()
    return tracking.get(npi)


def get_all_statuses() -> Dict:
    """Get all tracking data."""
    return load_tracking()


def get_pipeline_summary() -> Dict:
    """
    Get summary of pipeline by status.
    
    Returns:
        dict: {"status": count, ...} plus aggregates
    """
    tracking = load_tracking()
    
    summary = {status: 0 for status in VALID_STATUSES}
    summary["total"] = len(tracking)
    
    for npi, data in tracking.items():
        status = data.get("status", "Not Contacted")
        if status in summary:
            summary[status] += 1
    
    # Calculate active pipeline (excluding won/lost/not interested)
    summary["active_pipeline"] = (
        summary["Contacted"] +
        summary["Follow-up Scheduled"] +
        summary["Meeting Scheduled"] +
        summary["Proposal Sent"] +
        summary["Negotiating"]
    )
    
    return summary


def add_note(npi: str, note: str):
    """
    Add a note to an existing tracking record.
    
    Args:
        npi (str): Clinic NPI number
        note (str): Note to add
    
    Returns:
        bool: Success status
    """
    tracking = load_tracking()
    
    if npi in tracking:
        current_notes = tracking[npi].get("notes", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_note = f"[{timestamp}] {note}"
        
        if current_notes:
            tracking[npi]["notes"] = f"{current_notes}\n{new_note}"
        else:
            tracking[npi]["notes"] = new_note
        
        tracking[npi]["updated_at"] = datetime.now().isoformat()
        save_tracking(tracking)
        return True
    
    return False


def get_by_status(status: str) -> List[str]:
    """
    Get list of NPIs with a specific status.
    
    Args:
        status (str): Status to filter by
    
    Returns:
        list: List of NPI numbers
    """
    tracking = load_tracking()
    return [npi for npi, data in tracking.items() if data.get("status") == status]


# Example usage
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("OUTREACH TRACKING SYSTEM - TEST")
    print("=" * 80)
    
    # Test updates
    test_npi = "1234567890"
    
    print(f"\nAdding test clinic {test_npi}...")
    update_status(test_npi, "Not Contacted", "Found via IL scraper")
    
    print(f"Updating to Contacted...")
    update_status(test_npi, "Contacted", "Spoke with office manager Jane", "2025-12-13")
    
    print(f"Adding follow-up note...")
    add_note(test_npi, "Jane requested proposal for 3 providers")
    
    print(f"\nGetting status...")
    status = get_status(test_npi)
    if status:
        print(f"  Status: {status['status']}")
        print(f"  Contact Date: {status['contact_date']}")
        print(f"  Notes:\n{status['notes']}")
    
    print(f"\nPipeline Summary:")
    summary = get_pipeline_summary()
    print(f"  Total Tracked: {summary['total']}")
    print(f"  Active Pipeline: {summary['active_pipeline']}")
    for status, count in summary.items():
        if count > 0 and status not in ["total", "active_pipeline"]:
            print(f"  {status}: {count}")
    
    print("\n" + "=" * 80 + "\n")
