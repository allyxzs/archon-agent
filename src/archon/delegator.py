"""Módulo de delegação e roteamento de responsabilidades do Archon."""

from __future__ import annotations

from .models import SubAgentResult, SubTask
from .subagents import BaseSubAgent


class Delegator:
    """Seleciona o subagente apropriado e distribui subtarefas."""

    def __init__(self, subagents: list[BaseSubAgent]) -> None:
        if not subagents:
            raise ValueError("Archon precisa de pelo menos um subagente registrado para delegação.")
        self.subagents = subagents

    def select_agent(self, subtask: SubTask) -> BaseSubAgent:
        for agent in self.subagents:
            if subtask.required_capability in agent.capabilities:
                return agent
        return self.subagents[0]

    def delegate(
        self,
        subtask: SubTask,
        dependency_outputs: dict[str, str],
        feedback: str | None = None,
    ) -> SubAgentResult:
        agent = self.select_agent(subtask)
        subtask.assigned_agent = agent.name
        subtask.attempts += 1
        return agent.execute(subtask=subtask, context=dependency_outputs, feedback=feedback)
