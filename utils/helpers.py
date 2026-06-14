"""
utils/helpers.py
================
Small utility functions used across the project.
"""

import re
from datetime import datetime


def extract_time_from_text(text: str):
    """
    Parse a time and optional label from natural language.

    Examples:
        "remind me at 5 PM"                    → ("5 PM", "Reminder")
        "remind me at 5:30 PM to drink water"  → ("5:30 PM", "drink water")
        "remind me at 17:00"                   → ("17:00", "Reminder")

    Returns:
        (time_str, label)  — or  (None, None) if no time found
    """
    # Pattern: optional hour:minute, then AM/PM or 24-hour
    pattern = r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)"

    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None, None

    time_str = match.group(1).strip()

    # Try to extract a label after "to ..."
    label_match = re.search(r"\bto\b (.+)", text[match.end():], re.IGNORECASE)
    label = label_match.group(1).strip() if label_match else "Reminder"

    return time_str, label


def format_task_list(tasks: list) -> str:
    """
    Turn a list of task dicts into a readable numbered string.

    Example output: "1. Finish report | 2. Call client | 3. Review PR"
    """
    if not tasks:
        return "No tasks."
    parts = [f"{i+1}. {t['name']}" for i, t in enumerate(tasks)]
    return " | ".join(parts)


def current_time_str() -> str:
    """Return the current time as a readable string, e.g. '09:45 AM'."""
    return datetime.now().strftime("%I:%M %p")


def current_date_str() -> str:
    """Return the current date as a readable string, e.g. 'Monday, Jan 15'."""
    return datetime.now().strftime("%A, %b %d")