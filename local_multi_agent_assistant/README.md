# Local Multi-Agent Assistant (LMAA-v2)

The Local Multi-Agent Assistant is a fully local, LLM-enabled research communication helper. All agents rely on a shared `think()` reasoning function to parse, classify, and respond to academic messages.

## Features
- Receiver agent parses labeled inbox data into structured digests.
- Commander agent classifies intents and routes tasks to Calendar, Reply, or Local agents.
- Calendar agent detects scheduling details and conflicts.
- Local agent summarises project files for quick updates.
- Reply agent drafts tone-aware responses with help from the Learner agent.
- Learner agent maintains tone metrics stored in `data/learner_state.json`.
- Dataset generator produces synthetic labeled messages and example project files.

## Project Layout
```
local_multi_agent_assistant/
├── main.py
├── core/
│   ├── receiver_agent.py
│   ├── commander_agent.py
│   ├── calendar_agent.py
│   ├── local_agent.py
│   ├── reply_agent.py
│   ├── learner_agent.py
│   └── llm_utils.py
├── data/
│   ├── inbox_labeled.json
│   ├── logs/
│   ├── learner_state.json
│   └── sample_files/
├── utils/
│   ├── schema.py
│   ├── logger.py
│   ├── prompt_templates.py
│   └── dataset_generator.py
├── tests/
│   ├── test_agents.py
│   └── test_dataset.py
└── README.md
```

## Getting Started
1. Install dependencies (standard library only).
2. Optionally regenerate the dataset: `python utils/dataset_generator.py`.
3. Run the demo pipeline: `python -m local_multi_agent_assistant.main --demo`.
4. Execute tests with `pytest` from the repository root.
