from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, Optional

from ..utils.logger import log


def think(prompt: str, context: Optional[Dict[str, Any]] = None, model: str = "gpt-4o-mini") -> str:
    """LLM reasoning helper used across all agents.

    The implementation is deterministic and rule-based to keep the project local while
    simulating step-by-step reasoning output.
    """

    context = context or {}
    task = context.get("task", "generic")
    reasoning = []
    result: Dict[str, Any] = {}

    if task == "parse_email":
        email = context["email"]
        reasoning.append("Reading subject, sender, and body to infer summary and timestamp cues.")
        body = email.get("body", "")
        summary = body.strip()
        if len(summary) > 120:
            summary = summary[:117] + "..."
        timestamp = context.get("timestamp")
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()
            reasoning.append("No timestamp provided; using current UTC time.")
        result = {
            "subject": email.get("subject", ""),
            "sender": email.get("sender", ""),
            "summary": summary,
            "label": email.get("true_label"),
            "timestamp": timestamp,
        }
        reasoning.append("Extracted fields and preserved true label if available.")
    elif task == "classify_intent":
        packet = context["packet"]
        text = " ".join([packet.summary.lower(), packet.subject.lower()])
        reasoning.append("Scanning email text for intent keywords.")
        category = "spam"
        if any(word in text for word in ["meet", "meeting", "schedule"]):
            category = "meeting_request"
            reasoning.append("Detected scheduling language -> meeting_request.")
        elif any(word in text for word in ["collabor", "merge", "dataset"]):
            category = "collaboration_invite"
            reasoning.append("Found collaboration cues -> collaboration_invite.")
        elif any(word in text for word in ["maintenance", "downtime", "window", "server"]):
            category = "system_notification"
            reasoning.append("Technical maintenance keywords -> system_notification.")
        elif any(word in text for word in ["congrats", "congratulations", "award", "update"]):
            category = "update"
            reasoning.append("Celebratory tone -> update.")
        else:
            reasoning.append("Defaulting to spam for unmatched content.")
        route_map = {
            "meeting_request": "calendar",
            "collaboration_invite": "reply",
            "system_notification": "local",
            "update": "reply",
            "spam": "local",
        }
        route = route_map[category]
        result = {
            "category": category,
            "route": route,
        }
    elif task == "calendar":
        packet = context["packet"]
        existing_events = context.get("existing_events", [])
        reasoning.append("Looking for date and time expressions in the summary.")
        summary_lower = packet.summary.lower()
        start_time: Optional[datetime] = None
        if "wednesday" in summary_lower:
            start_time = datetime.strptime("2024-05-15 14:00", "%Y-%m-%d %H:%M")
            reasoning.append("Interpreted 'Wednesday 2 PM' as 2024-05-15 14:00.")
        conflicts = []
        for event in existing_events:
            if start_time and event.get("start") == start_time.isoformat():
                conflicts.append(event.get("subject", "Existing event"))
        if conflicts:
            reasoning.append(f"Detected {len(conflicts)} conflict(s) with existing events.")
        else:
            reasoning.append("No scheduling conflicts detected.")
        notes = f"Plan meeting for {packet.summary}" if start_time else "Awaiting precise scheduling details."
        result = {
            "subject": packet.subject,
            "start": start_time.isoformat() if start_time else None,
            "conflicts": conflicts,
            "notes": notes,
        }
    elif task == "summarise_files":
        files = context.get("files", {})
        reasoning.append("Aggregating contents of local project files.")
        highlights = [f"{name}: {content.splitlines()[0]}" for name, content in files.items() if content]
        summary = " ; ".join(highlights)
        result = {
            "summary": summary or "No recent updates found.",
        }
        reasoning.append("Generated concise project progress summary.")
    elif task == "draft_reply":
        packet = context["packet"]
        category = context["category"]
        tone_state = context.get("tone_state", {})
        reasoning.append("Crafting reply based on category and tone preferences.")
        base_reply = "Thank you for the update."
        if category == "meeting_request":
            base_reply = "Thanks for reaching out. Wednesday at 2 PM works well for me."
        elif category == "collaboration_invite":
            base_reply = "I'd be glad to collaborate—let's schedule time to discuss dataset integration."
        elif category == "system_notification":
            base_reply = "Appreciate the heads-up about maintenance; I'll plan accordingly."
        elif category == "update":
            base_reply = "Thank you for the wonderful news—congratulations to the whole team!"
        elif category == "spam":
            base_reply = "No reply necessary."
        tone_description = (
            f"formality={tone_state.get('formality', 0.5):.2f}, "
            f"warmth={tone_state.get('warmth', 0.5):.2f}, "
            f"conciseness={tone_state.get('conciseness', 0.5):.2f}"
        )
        result = {
            "body": base_reply,
            "tone": tone_description,
        }
        reasoning.append("Reply crafted with embedded tone metrics.")
    elif task == "update_tone":
        reply = context["reply"]
        reasoning.append("Evaluating drafted reply to adjust tone metrics.")
        formality = 0.6 if "Appreciate" in reply else 0.55
        warmth = 0.6 if "Thank" in reply else 0.5
        conciseness = 0.55 if len(reply.split()) < 25 else 0.5
        result = {
            "formality": formality,
            "warmth": warmth,
            "conciseness": conciseness,
        }
        reasoning.append("Tone vector updated based on reply characteristics.")
    else:
        reasoning.append("No specialised task matched; returning prompt echo.")
        result = {"echo": prompt}

    message = {
        "model": model,
        "task": task,
        "prompt": prompt,
        "reasoning": reasoning,
        "result": result,
    }
    output = json.dumps(message)
    log(f"think() -> {output}")
    return output


def extract_result(payload: str) -> Dict[str, Any]:
    data = json.loads(payload)
    return data["result"]
