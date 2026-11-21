"""Interface e implementações de exemplo para subagentes delegados pelo Archon."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .models import SubAgentResult, SubTask


class BaseSubAgent(ABC):
    """Contrato base para qualquer agente especialista coordenado pelo Archon."""

    name: str
    capabilities: set[str]

    @abstractmethod
    def execute(self, subtask: SubTask, context: dict[str, str], feedback: str | None = None) -> SubAgentResult:
        """Executa uma subtarefa atribuída pelo Archon."""


class ResearchSubAgent(BaseSubAgent):
    name = "ResearchAgent"
    capabilities = {"research", "discovery", "benchmarking"}

    def execute(self, subtask: SubTask, context: dict[str, str], feedback: str | None = None) -> SubAgentResult:
        revision_note = f" (Revisão aplicada: {feedback})" if feedback else ""
        output = (
            f"Levantamento concluído para '{subtask.title}': identificados requisitos centrais, "
            f"referências de mercado e restrições críticas.{revision_note}"
        )
        return SubAgentResult(subtask_id=subtask.id, agent_name=self.name, output=output)


class AnalystSubAgent(BaseSubAgent):
    name = "AnalystAgent"
    capabilities = {"analysis", "strategy", "risk"}

    def execute(self, subtask: SubTask, context: dict[str, str], feedback: str | None = None) -> SubAgentResult:
        deps = ", ".join(context.keys()) if context else "sem dependências prévias"
        revision_note = f" (Ajustado conforme supervisão: {feedback})" if feedback else ""
        output = (
            f"Análise estruturada de '{subtask.title}' considerando [{deps}]: "
            f"prioridades definidas, riscos mapeados e plano de mitigação estabelecido.{revision_note}"
        )
        return SubAgentResult(subtask_id=subtask.id, agent_name=self.name, output=output)


class WriterSubAgent(BaseSubAgent):
    name = "WriterAgent"
    capabilities = {"writing", "documentation", "communication"}

    def execute(self, subtask: SubTask, context: dict[str, str], feedback: str | None = None) -> SubAgentResult:
        revision_note = f" (Refinado após feedback: {feedback})" if feedback else ""
        output = (
            f"Documento executivo elaborado para '{subtask.title}' consolidando diretrizes, "
            f"responsabilidades e cronograma de entrega.{revision_note}"
        )
        return SubAgentResult(subtask_id=subtask.id, agent_name=self.name, output=output)


class ReviewerSubAgent(BaseSubAgent):
    name = "ReviewerAgent"
    capabilities = {"review", "qa", "compliance"}

    def execute(self, subtask: SubTask, context: dict[str, str], feedback: str | None = None) -> SubAgentResult:
        output = (
            f"Revisão de qualidade concluída para '{subtask.title}': consistência verificada, "
            f"critérios de aceitação atendidos e entregáveis prontos para consolidação."
        )
        return SubAgentResult(subtask_id=subtask.id, agent_name=self.name, output=output)


def create_default_subagents() -> list[BaseSubAgent]:
    """Retorna o conjunto padrão de subagentes especialistas."""
    return [
        ResearchSubAgent(),
        AnalystSubAgent(),
        WriterSubAgent(),
        ReviewerSubAgent(),
    ]
