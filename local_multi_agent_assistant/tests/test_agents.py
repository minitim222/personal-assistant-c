from __future__ import annotations

from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))

from local_multi_agent_assistant.core import (
    calendar_agent,
    commander_agent,
    learner_agent,
    local_agent,
    receiver_agent,
    reply_agent,
)
from local_multi_agent_assistant.utils.schema import DigestPacket, ToneState

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
INBOX = DATA_DIR / "inbox_labeled.json"


def test_receiver_outputs_packets():
    packets = receiver_agent.parse_inbox(str(INBOX))
    assert isinstance(packets, list)
    assert all(isinstance(p, DigestPacket) for p in packets)
    assert packets, "Receiver should return at least one packet"


def test_commander_accuracy():
    packets = receiver_agent.parse_inbox(str(INBOX))
    correct = 0
    for packet in packets:
        ticket = commander_agent.classify_and_route(packet)
        if packet.label == ticket.category:
            correct += 1
    assert correct >= 4, "Commander should match at least 4/5 labels"


def test_reply_and_learner_integration():
    packets = receiver_agent.parse_inbox(str(INBOX))
    tone_state = ToneState()
    for packet in packets:
        ticket = commander_agent.classify_and_route(packet)
        if ticket.route == "reply":
            reply = reply_agent.draft_reply(packet, ticket, tone_state)
            assert reply.body
            tone_state = learner_agent.update_state(reply)
            assert 0 <= tone_state.formality <= 1


def test_calendar_and_local_agents():
    packets = receiver_agent.parse_inbox(str(INBOX))
    calendar_events = [packet for packet in packets if packet.label == "meeting_request"]
    if calendar_events:
        summary = calendar_agent.handle(calendar_events[0])
        assert summary.subject
    local_summary = local_agent.summarise_files()
    assert isinstance(local_summary, str)
    assert local_summary
