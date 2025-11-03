from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
INBOX_FILE = DATA_DIR / "inbox_labeled.json"
SAMPLE_DIR = DATA_DIR / "sample_files"

SAMPLE_EMAILS: List[Dict[str, str]] = [
    {
        "subject": "Weekly Lab Meeting",
        "sender": "prof.smith@university.edu",
        "body": "Let's meet Wednesday 2 PM to discuss results.",
        "true_label": "meeting_request",
    },
    {
        "subject": "Collaboration on dataset",
        "sender": "bharti@childrens.harvard.edu",
        "body": "Can we merge the E14 and MIA datasets?",
        "true_label": "collaboration_invite",
    },
    {
        "subject": "Server downtime tonight",
        "sender": "it@institute.org",
        "body": "Maintenance window from 11PM to 1AM.",
        "true_label": "system_notification",
    },
    {
        "subject": "Congratulations!",
        "sender": "admin@school.edu",
        "body": "Congrats on your recent award!",
        "true_label": "update",
    },
    {
        "subject": "AI conference ad",
        "sender": "noreply@randommail.com",
        "body": "Join our free AI event!",
        "true_label": "spam",
    },
]

SAMPLE_FILES = {
    "progress_report.txt": "Completed analysis of week 12 cohort data. Preparing visualization scripts.",
    "todo.txt": "- Finalize manuscript draft\n- Prepare slides for lab meeting\n- Review collaborator feedback",
}


def ensure_sample_environment() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    for name, content in SAMPLE_FILES.items():
        file_path = SAMPLE_DIR / name
        file_path.write_text(content, encoding="utf-8")


def generate_dataset() -> None:
    ensure_sample_environment()
    INBOX_FILE.write_text(json.dumps(SAMPLE_EMAILS, indent=2), encoding="utf-8")


if __name__ == "__main__":
    generate_dataset()
    print(f"Dataset written to {INBOX_FILE}")
