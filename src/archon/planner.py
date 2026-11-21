"""Módulo de planejamento e decomposição de tarefas do Archon."""

from __future__ import annotations

from .models import ExecutionPlan, SubTask


class Planner:
    """Decompõe um objetivo de alto nível em subtarefas ordenadas com dependências."""

    def create_plan(self, goal: str) -> ExecutionPlan:
        cleaned_goal = goal.strip()
        if not cleaned_goal:
            raise ValueError("O objetivo fornecido ao Archon não pode estar vazio.")

        subtasks = [
            SubTask(
                id="T1",
                title="Levantamento de Contexto e Requisitos",
                description=f"Pesquisar contexto, restrições e referências essenciais para: {cleaned_goal}",
                required_capability="research",
                dependencies=[],
                acceptance_criteria=[
                    "Identificar requisitos principais",
                    "Listar restrições e premissas",
                ],
            ),
            SubTask(
                id="T2",
                title="Análise Estratégica e Mapeamento de Riscos",
                description=f"Analisar alternativas, prioridades e riscos envolvidos em: {cleaned_goal}",
                required_capability="analysis",
                dependencies=["T1"],
                acceptance_criteria=[
                    "Definir prioridades",
                    "Mapear riscos e mitigações",
                ],
            ),
            SubTask(
                id="T3",
                title="Estruturação do Plano de Ação",
                description=f"Redigir entregável estruturado com ações, responsáveis e entregas para: {cleaned_goal}",
                required_capability="writing",
                dependencies=["T1", "T2"],
                acceptance_criteria=[
                    "Apresentar etapas acionáveis",
                    "Manter clareza executiva",
                ],
            ),
            SubTask(
                id="T4",
                title="Revisão de Qualidade e Conformidade",
                description=f"Revisar coerência, completude e aderência ao objetivo: {cleaned_goal}",
                required_capability="review",
                dependencies=["T3"],
                acceptance_criteria=[
                    "Validar alinhamento ao objetivo original",
                    "Confirmar ausência de lacunas críticas",
                ],
            ),
        ]
        return ExecutionPlan(goal=cleaned_goal, subtasks=subtasks)
