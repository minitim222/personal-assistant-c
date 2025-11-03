from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .llm_utils import extract_result, think
from ..utils.logger import log
from ..utils.schema import DigestPacket
from ..utils import prompt_templates as prompts


def parse_inbox(path: str) -> List[DigestPacket]:
    inbox_path = Path(path)
    if not inbox_path.exists():
        raise FileNotFoundError(f"Inbox file not found: {path}")

    emails = json.loads(inbox_path.read_text(encoding="utf-8"))
    packets: List[DigestPacket] = []

    for email in emails:
        response = think(prompts.RECEIVER_PROMPT, {"task": "parse_email", "email": email})
        result = extract_result(response)
        packet = DigestPacket(
            subject=result["subject"],
            sender=result["sender"],
            summary=result["summary"],
            label=result.get("label"),
            timestamp=result.get("timestamp"),
        )
        packets.append(packet)
        log(f"ReceiverAgent parsed email: {packet.subject}")

    log(f"ReceiverAgent parsed {len(packets)} emails in total.")
    return packets
