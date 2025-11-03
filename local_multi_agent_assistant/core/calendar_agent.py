from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from .llm_utils import extract_result, think
from ..utils.logger import log
from ..utils.schema import DigestPacket, EventSummary
from ..utils import prompt_templates as prompts


EXISTING_EVENTS: List[Dict[str, str]] = [
    {
        "subject": "Weekly sync",
        "start": "2024-05-15T13:00:00",
    }
]


def handle(packet: DigestPacket) -> EventSummary:
    response = think(
        prompts.CALENDAR_PROMPT,
        {"task": "calendar", "packet": packet, "existing_events": EXISTING_EVENTS},
    )
    result = extract_result(response)
    start = result.get("start")
    start_dt = datetime.fromisoformat(start) if start else None
    summary = EventSummary(
        subject=result.get("subject", packet.subject),
        start=start_dt,
        conflicts=result.get("conflicts", []),
        notes=result.get("notes", ""),
    )
    log(f"CalendarAgent created event summary for {summary.subject}")
    return summary
