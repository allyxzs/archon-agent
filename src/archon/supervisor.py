"""Módulo de supervisão e controle de qualidade do Archon."""

from __future__ import annotations

from .models import SubAgentResult, SubTask, SupervisionVerdict


class Supervisor:
    """Avalia entregas dos subagentes e decide por aprovação ou solicitação de revisão."""

    def __init__(self, min_output_length: int = 20) -> None:
        self.min_output_length = min_output_length

    def evaluate(self, subtask: SubTask, result: SubAgentResult) -> SupervisionVerdict:
        if not result.success:
            return SupervisionVerdict(
                approved=False,
                feedback="A execução falhou; refazer entregável garantindo conclusão válida.",
                score=0.0,
            )

        content = (result.output or "").strip()
        if len(content) < self.min_output_length:
            return SupervisionVerdict(
                approved=False,
                feedback=(
                    f"Entrega muito curta ({len(content)} caracteres). "
                    f"Detalhe melhor os critérios de aceitação de '{subtask.title}'."
                ),
                score=0.3,
            )

        return SupervisionVerdict(
            approved=True,
            feedback="Entrega aprovada pela supervisão do Archon.",
            score=1.0,
        )
