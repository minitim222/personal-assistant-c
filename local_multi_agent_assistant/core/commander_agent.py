from __future__ import annotations

from typing import Dict, List, Tuple

from .llm_utils import extract_result, think
from ..utils.logger import log
from ..utils.schema import DigestPacket, TaskTicket
from ..utils import prompt_templates as prompts


class CommanderMetrics:
    def __init__(self) -> None:
        self._records: List[Tuple[str, str]] = []

    def add(self, true_label: str | None, predicted: str) -> None:
        if true_label:
            self._records.append((true_label, predicted))

    def accuracy(self) -> float:
        if not self._records:
            return 0.0
        correct = sum(1 for true, pred in self._records if true == pred)
        return correct / len(self._records)

    def confusion_matrix(self) -> Dict[str, Dict[str, int]]:
        labels = sorted({true for true, _ in self._records} | {pred for _, pred in self._records})
        matrix: Dict[str, Dict[str, int]] = {label: {l: 0 for l in labels} for label in labels}
        for true, pred in self._records:
            matrix[true][pred] += 1
        return matrix

    def summary(self) -> str:
        acc = self.accuracy()
        matrix = self.confusion_matrix()
        matrix_lines = [f"{true}: {row}" for true, row in matrix.items()]
        return "\n".join([f"Accuracy: {acc:.2f}"] + matrix_lines)


metrics = CommanderMetrics()


def classify_and_route(packet: DigestPacket) -> TaskTicket:
    response = think(prompts.COMMANDER_PROMPT, {"task": "classify_intent", "packet": packet})
    result = extract_result(response)
    category = result["category"]
    route = result["route"]

    ticket = TaskTicket(
        subject=packet.subject,
        category=category,
        route=route,
        reasoning=response,
        true_label=packet.label,
    )

    metrics.add(packet.label, category)
    log(
        "CommanderAgent classified '%s' as %s (true=%s)",
        packet.subject,
        category,
        packet.label,
    )
    return ticket


def metrics_report() -> str:
    return metrics.summary()
