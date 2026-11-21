"""Classe principal do agente Archon."""

from __future__ import annotations

import logging

from .delegator import Delegator
from .models import ExecutionPlan, FinalReport, SubAgentResult, SubTask, TaskStatus
from .planner import Planner
from .subagents import BaseSubAgent, create_default_subagents
from .supervisor import Supervisor
from .synthesizer import Synthesizer

logger = logging.getLogger("archon")


class Archon:
    """Agente Orquestrador: planeja, delega, supervisiona e consolida resultados."""

    def __init__(
        self,
        subagents: list[BaseSubAgent] | None = None,
        planner: Planner | None = None,
        supervisor: Supervisor | None = None,
        synthesizer: Synthesizer | None = None,
        max_retries: int = 2,
    ) -> None:
        self.subagents = subagents if subagents is not None else create_default_subagents()
        self.planner = planner or Planner()
        self.delegator = Delegator(self.subagents)
        self.supervisor = supervisor or Supervisor()
        self.synthesizer = synthesizer or Synthesizer()
        self.max_retries = max_retries

    def run(self, goal: str, custom_plan: ExecutionPlan | None = None) -> FinalReport:
        """Executa o ciclo completo de orquestração para um objetivo."""
        plan = custom_plan or self.planner.create_plan(goal)
        results: dict[str, SubAgentResult] = {}

        ordered_tasks = self._resolve_execution_order(plan.subtasks)

        for subtask in ordered_tasks:
            subtask.status = TaskStatus.IN_PROGRESS
            dep_context = {
                dep_id: results[dep_id].output
                for dep_id in subtask.dependencies
                if dep_id in results
            }

            feedback: str | None = None
            final_result: SubAgentResult | None = None

            for _ in range(self.max_retries + 1):
                result = self.delegator.delegate(
                    subtask=subtask,
                    dependency_outputs=dep_context,
                    feedback=feedback,
                )
                verdict = self.supervisor.evaluate(subtask, result)
                final_result = result

                if verdict.approved:
                    subtask.status = TaskStatus.APPROVED
                    logger.info("Subtarefa %s aprovada (%s).", subtask.id, result.agent_name)
                    break

                subtask.status = TaskStatus.REVISION_REQUESTED
                feedback = verdict.feedback
                logger.warning("Subtarefa %s rejeitada na supervisão: %s", subtask.id, feedback)
            else:
                subtask.status = TaskStatus.FAILED

            if final_result is not None:
                results[subtask.id] = final_result

        return self.synthesizer.synthesize(plan=plan, results=results)

    @staticmethod
    def _resolve_execution_order(subtasks: list[SubTask]) -> list[SubTask]:
        """Ordenação topológica simples respeitando dependências entre subtarefas."""
        pending = {t.id: t for t in subtasks}
        resolved: list[SubTask] = []
        resolved_ids: set[str] = set()

        while pending:
            progressed = False
            for task_id in list(pending.keys()):
                task = pending[task_id]
                if all(dep in resolved_ids for dep in task.dependencies):
                    resolved.append(task)
                    resolved_ids.add(task_id)
                    del pending[task_id]
                    progressed = True
            if not progressed:
                raise ValueError("Dependência cíclica ou inválida detectada no plano de execução.")

        return resolved
