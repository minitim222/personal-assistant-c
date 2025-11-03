from __future__ import annotations

import json
from pathlib import Path

from .llm_utils import extract_result, think
from ..utils.logger import log
from ..utils.schema import ReplyDraft, ToneState
from ..utils import prompt_templates as prompts

STATE_FILE = Path(__file__).resolve().parents[1] / "data" / "learner_state.json"


def load_tone_state() -> ToneState:
    if STATE_FILE.exists():
        payload = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return ToneState.from_dict(payload)
    return ToneState()


def update_state(reply: ReplyDraft) -> ToneState:
    response = think(prompts.LEARNER_PROMPT, {"task": "update_tone", "reply": reply.body})
    result = extract_result(response)
    tone = ToneState.from_dict(result)
    STATE_FILE.write_text(json.dumps(tone.as_dict(), indent=2), encoding="utf-8")
    log("LearnerAgent updated tone state: %s", tone.as_dict())
    return tone
