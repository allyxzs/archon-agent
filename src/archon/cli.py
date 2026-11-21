"""Interface de linha de comando para o agente Archon."""

from __future__ import annotations

import argparse
import sys

from .orchestrator import Archon


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="archon",
        description="Archon — Agente de orquestração, delegação, planejamento e supervisão.",
    )
    parser.add_argument(
        "goal",
        type=str,
        help="Objetivo de alto nível a ser orquestrado pelo Archon.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="Número máximo de retentativas supervisionadas por subtarefa (padrão: 2).",
    )
    args = parser.parse_args(argv)

    archon = Archon(max_retries=args.max_retries)
    report = archon.run(args.goal)
    print(report.to_markdown())
    return 0


if __name__ == "__main__":
    sys.exit(main())
