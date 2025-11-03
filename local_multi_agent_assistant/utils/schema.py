from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class DigestPacket:
    """Structured representation of an incoming message."""

    subject: str
    sender: str
    summary: str
    label: Optional[str]
    timestamp: Optional[str]
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class TaskTicket:
    """Commander output describing a routed task."""

    subject: str
    category: str
    route: str
    reasoning: str
    true_label: Optional[str] = None
    annotations: Dict[str, str] = field(default_factory=dict)


@dataclass
class EventSummary:
    """Calendar agent output representing a scheduled event."""

    subject: str
    start: Optional[datetime]
    conflicts: List[str]
    notes: str


@dataclass
class ReplyDraft:
    """Reply agent result containing the drafted reply and reasoning."""

    subject: str
    body: str
    tone: str
    reasoning: str


@dataclass
class ToneState:
    """Learner agent tone vector persisted across runs."""

    formality: float = 0.5
    warmth: float = 0.5
    conciseness: float = 0.5

    def as_dict(self) -> Dict[str, float]:
        return {
            "formality": self.formality,
            "warmth": self.warmth,
            "conciseness": self.conciseness,
        }

    @classmethod
    def from_dict(cls, payload: Dict[str, float]) -> "ToneState":
        return cls(
            formality=payload.get("formality", 0.5),
            warmth=payload.get("warmth", 0.5),
            conciseness=payload.get("conciseness", 0.5),
        )
