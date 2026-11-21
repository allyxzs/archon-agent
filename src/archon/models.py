"""Modelos de dados centrais do agente Archon."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REVISION_REQUESTED = "revision_requested"
    FAILED = "failed"


@dataclass
class SubTask:
    id: str
    title: str
    description: str
    required_capability: str
    dependencies: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: str | None = None
    attempts: int = 0


@dataclass
class ExecutionPlan:
    goal: str
    subtasks: list[SubTask]

    def get_subtask(self, subtask_id: str) -> SubTask | None:
        for task in self.subtasks:
            if task.id == subtask_id:
                return task
        return None


@dataclass
class SubAgentResult:
    subtask_id: str
    agent_name: str
    output: str
    success: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SupervisionVerdict:
    approved: bool
    feedback: str
    score: float = 1.0


@dataclass
class FinalReport:
    goal: str
    plan: ExecutionPlan
    results: dict[str, SubAgentResult]
    conclusion: str
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_markdown(self) -> str:
        lines = [
            "# Relatório Final — Archon",
            "",
            f"**Objetivo:** {self.goal}",
            "",
            "## Plano Executado e Delegações",
        ]
        for task in self.plan.subtasks:
            result = self.results.get(task.id)
            status_icon = "✅" if task.status == TaskStatus.APPROVED else "⚠️"
            lines.append(
                f"- {status_icon} **{task.id} — {task.title}** "
                f"(Responsável: `{task.assigned_agent or 'N/A'}` | Tentativas: {task.attempts})"
            )
            if result:
                lines.append(f"  - Entrega: {result.output}")

        lines.extend(["", "## Conclusão Consolidada", "", self.conclusion])

        if self.metrics:
            lines.extend(["", "## Métricas de Supervisão"])
            for key, value in self.metrics.items():
                lines.append(f"- **{key}**: {value}")

        return "\n".join(lines)
