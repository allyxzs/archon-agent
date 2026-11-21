"""Módulo de síntese e apresentação de conclusão do Archon."""

from __future__ import annotations

from .models import ExecutionPlan, FinalReport, SubAgentResult, TaskStatus


class Synthesizer:
    """Consolida os resultados aprovados de todos os subagentes em uma conclusão final."""

    def synthesize(self, plan: ExecutionPlan, results: dict[str, SubAgentResult]) -> FinalReport:
        approved_count = sum(1 for t in plan.subtasks if t.status == TaskStatus.APPROVED)
        total_count = len(plan.subtasks)
        total_attempts = sum(t.attempts for t in plan.subtasks)

        highlights = []
        for task in plan.subtasks:
            res = results.get(task.id)
            if res:
                highlights.append(f"- **{task.title}** ({res.agent_name}): {res.output}")

        status_summary = (
            "todas as subtarefas foram concluídas e aprovadas pela supervisão"
            if approved_count == total_count
            else f"{approved_count} de {total_count} subtarefas foram aprovadas"
        )

        highlights_block = "\n".join(highlights)
        conclusion = (
            f'O Archon coordenou o objetivo **"{plan.goal}"**, organizando o trabalho em '
            f"{total_count} etapas especializadas. Ao final da supervisão, {status_summary}.\n\n"
            f"### Síntese Integrada\n{highlights_block}\n\n"
            f"### Recomendação Final\n"
            f"Os resultados estão consolidados e prontos para execução imediata com governança contínua."
        )

        metrics = {
            "Subtarefas planejadas": total_count,
            "Subtarefas aprovadas": approved_count,
            "Taxa de aprovação": f"{(approved_count / total_count) * 100:.0f}%" if total_count else "0%",
            "Total de execuções/tentativas": total_attempts,
        }

        return FinalReport(
            goal=plan.goal,
            plan=plan,
            results=results,
            conclusion=conclusion,
            metrics=metrics,
        )
