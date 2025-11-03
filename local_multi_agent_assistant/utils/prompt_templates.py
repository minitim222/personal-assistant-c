"""Prompt snippets centralised for the Local Multi-Agent Assistant."""

RECEIVER_PROMPT = (
    "Parse the email into structured fields. Identify and preserve the labeled intent if provided."
)

COMMANDER_PROMPT = (
    "Classify the email intent into meeting_request, collaboration_invite, system_notification, spam, or update."
)

CALENDAR_PROMPT = (
    "Given these events and this request, generate a human-readable meeting summary and detect conflicts."
)

LOCAL_PROMPT = "Summarise project progress based on the latest local files."

REPLY_PROMPT = (
    "Write a concise professional reply confirming or acknowledging this message, following the user's tone."
)

LEARNER_PROMPT = "Infer tone drift and signature style from the drafted reply."
