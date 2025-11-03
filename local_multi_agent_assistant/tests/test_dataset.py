from __future__ import annotations

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "inbox_labeled.json"


def test_dataset_structure():
    assert DATA_FILE.exists(), "Dataset file missing"
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    for record in payload:
        assert {"subject", "sender", "body", "true_label"}.issubset(record)
        assert record["subject"], "Subject should not be empty"
        assert record["sender"], "Sender should not be empty"
        assert record["true_label"] in {
            "meeting_request",
            "collaboration_invite",
            "system_notification",
            "update",
            "spam",
        }
