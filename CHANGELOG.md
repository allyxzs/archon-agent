# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [0.1.0] - 2026-11-20
### Adicionado
- Arquitetura modular do agente **Archon** (`Planner`, `Delegator`, `Supervisor`, `Synthesizer`, `Orchestrator`).
- Prompts oficiais de sistema, delegação e síntese em `prompts/`.
- Subagentes padrão prontos para uso (`ResearchSubAgent`, `AnalystSubAgent`, `WriterSubAgent`, `ReviewerSubAgent`).
- Camada de LLM plugável (`MockLLMClient` e `OpenAICompatibleClient`).
- CLI executável (`python -m archon.cli`), exemplo rápido, testes automatizados e pipeline GitHub Actions.
