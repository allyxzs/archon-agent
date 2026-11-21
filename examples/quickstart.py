"""Exemplo rápido de execução do agente Archon."""

from archon import Archon, create_default_subagents


def main() -> None:
    archon = Archon(subagents=create_default_subagents(), max_retries=2)
    goal = "Planejar e lançar um programa de onboarding automatizado para novos clientes B2B"
    report = archon.run(goal)
    print(report.to_markdown())


if __name__ == "__main__":
    main()
