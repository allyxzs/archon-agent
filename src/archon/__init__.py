"""Archon: Agente de orquestração, delegação, planejamento e supervisão."""

from .models import (
    ExecutionPlan,
    FinalReport,
    SubAgentResult,
    SubTask,
    SupervisionVerdict,
    TaskStatus,
)
from .orchestrator import Archon
from .subagents import (
    AnalystSubAgent,
    BaseSubAgent,
    ResearchSubAgent,
    ReviewerSubAgent,
    WriterSubAgent,
    create_default_subagents,
)

__all__ = [
    "Archon",
    "BaseSubAgent",
    "ResearchSubAgent",
    "AnalystSubAgent",
    "WriterSubAgent",
    "ReviewerSubAgent",
    "create_default_subagents",
    "ExecutionPlan",
    "FinalReport",
    "SubAgentResult",
    "SubTask",
    "SupervisionVerdict",
    "TaskStatus",
]
__version__ = "0.1.0"
