from __future__ import annotations

from pathlib import Path
from typing import Dict

from .llm_utils import extract_result, think
from ..utils.logger import log
from ..utils import prompt_templates as prompts


SAMPLE_DIR = Path(__file__).resolve().parents[1] / "data" / "sample_files"


def summarise_files() -> str:
    files: Dict[str, str] = {}
    for path in SAMPLE_DIR.glob("*"):
        if path.is_file():
            files[path.name] = path.read_text(encoding="utf-8")
    response = think(prompts.LOCAL_PROMPT, {"task": "summarise_files", "files": files})
    result = extract_result(response)
    summary = result.get("summary", "")
    log("LocalAgent summary: %s", summary)
    return summary
