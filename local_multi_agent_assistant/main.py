from __future__ import annotations

import argparse
from pathlib import Path

from .core import calendar_agent, commander_agent, learner_agent, local_agent, receiver_agent, reply_agent
from .utils.logger import log

DATA_DIR = Path(__file__).resolve().parent / "data"


def run_demo() -> None:
    inbox_path = DATA_DIR / "inbox_labeled.json"
    packets = receiver_agent.parse_inbox(str(inbox_path))
    tone_state = learner_agent.load_tone_state()

    log("📥 Receiver parsed %d emails.", len(packets))
    for packet in packets:
        log("Processing email: %s", packet.subject)
        ticket = commander_agent.classify_and_route(packet)

        if ticket.route == "calendar":
            event = calendar_agent.handle(packet)
            log("📅 CalendarAgent: %s", event.notes)
        elif ticket.route == "reply":
            reply = reply_agent.draft_reply(packet, ticket, tone_state)
            log("📩 ReplyAgent drafted: %s", reply.body)
            tone_state = learner_agent.update_state(reply)
            log("🧠 LearnerAgent tone: %s", tone_state.as_dict())
        else:
            summary = local_agent.summarise_files()
            log("📚 LocalAgent summary: %s", summary)

    metrics_report = commander_agent.metrics_report()
    log("🔍 Commander metrics:\n%s", metrics_report)


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Multi-Agent Assistant Demo")
    parser.add_argument("--demo", action="store_true", help="Run the demo pipeline")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
