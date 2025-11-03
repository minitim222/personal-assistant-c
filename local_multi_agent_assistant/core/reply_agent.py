from __future__ import annotations

from .llm_utils import extract_result, think
from ..utils.logger import log
from ..utils.schema import DigestPacket, ReplyDraft, TaskTicket, ToneState
from ..utils import prompt_templates as prompts


def draft_reply(packet: DigestPacket, ticket: TaskTicket, tone_state: ToneState) -> ReplyDraft:
    response = think(
        prompts.REPLY_PROMPT,
        {
            "task": "draft_reply",
            "packet": packet,
            "category": ticket.category,
            "tone_state": tone_state.as_dict(),
        },
    )
    result = extract_result(response)
    reply = ReplyDraft(
        subject=packet.subject,
        body=result.get("body", ""),
        tone=result.get("tone", ""),
        reasoning=response,
    )
    log(f"ReplyAgent drafted reply for {packet.subject}")
    return reply
