"""Testes automatizados para o agente Archon (compatível com pytest e unittest)."""

import unittest

from archon import (
    Archon,
    BaseSubAgent,
    ExecutionPlan,
    SubAgentResult,
    SubTask,
    TaskStatus,
    create_default_subagents,
)


class FlakySubAgent(BaseSubAgent):
    """Subagente que falha na primeira tentativa e entrega corretamente após feedback."""

    name = "FlakyAgent"
    capabilities = {"research"}

    def __init__(self) -> None:
        self.calls = 0

    def execute(self, subtask: SubTask, context: dict[str, str], feedback: str | None = None) -> SubAgentResult:
        self.calls += 1
        if self.calls == 1:
            return SubAgentResult(subtask_id=subtask.id, agent_name=self.name, output="curto")
        return SubAgentResult(
            subtask_id=subtask.id,
            agent_name=self.name,
            output=f"Entrega revisada e completa após supervisão: {feedback}",
        )


class TestArchon(unittest.TestCase):
    def test_end_to_end_default_workflow(self) -> None:
        archon = Archon(subagents=create_default_subagents())
        report = archon.run("Criar estratégia de lançamento de produto")

        self.assertEqual(len(report.plan.subtasks), 4)
        self.assertTrue(all(task.status == TaskStatus.APPROVED for task in report.plan.subtasks))
        self.assertEqual(report.metrics["Subtarefas aprovadas"], 4)
        self.assertIn("Conclusão Consolidada", report.to_markdown())

    def test_supervision_retry_succeeds(self) -> None:
        flaky = FlakySubAgent()
        archon = Archon(subagents=[flaky], max_retries=2)
        plan = ExecutionPlan(
            goal="Testar supervisão",
            subtasks=[
                SubTask(
                    id="T1",
                    title="Pesquisa inicial",
                    description="Levantar dados",
                    required_capability="research",
                )
            ],
        )

        report = archon.run("Testar supervisão", custom_plan=plan)
        self.assertEqual(flaky.calls, 2)
        self.assertEqual(report.plan.subtasks[0].status, TaskStatus.APPROVED)
        self.assertEqual(report.plan.subtasks[0].attempts, 2)

    def test_detects_cyclic_dependencies(self) -> None:
        archon = Archon(subagents=create_default_subagents())
        cyclic_plan = ExecutionPlan(
            goal="Plano inválido",
            subtasks=[
                SubTask(id="A", title="A", description="A", required_capability="research", dependencies=["B"]),
                SubTask(id="B", title="B", description="B", required_capability="analysis", dependencies=["A"]),
            ],
        )
        with self.assertRaises(ValueError):
            archon.run("Plano inválido", custom_plan=cyclic_plan)

    def test_rejects_empty_goal(self) -> None:
        archon = Archon()
        with self.assertRaises(ValueError):
            archon.run("   ")


if __name__ == "__main__":
    unittest.main()
