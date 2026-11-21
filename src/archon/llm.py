"""Camada de abstração de LLM para o Archon."""

from __future__ import annotations

import json
import os
import urllib.request
from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """Interface comum para provedores de LLM."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Gera uma resposta textual a partir dos prompts fornecidos."""


class MockLLMClient(BaseLLMClient):
    """Cliente determinístico local para desenvolvimento, testes e demonstrações sem API."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        first_line = user_prompt.strip().splitlines()[0] if user_prompt.strip() else "tarefa"
        return f"[MockLLM] Resposta estruturada gerada para: {first_line}"


class OpenAICompatibleClient(BaseLLMClient):
    """Cliente HTTP leve compatível com endpoints OpenAI Chat Completions."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or os.getenv("ARCHON_API_KEY", "")
        self.base_url = (base_url or os.getenv("ARCHON_API_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
        self.model = model or os.getenv("ARCHON_MODEL", "gpt-4o-mini")
        self.timeout = timeout

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("ARCHON_API_KEY não configurada para o provedor openai_compatible.")

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()


def build_llm_client() -> BaseLLMClient:
    """Instancia o cliente LLM conforme variáveis de ambiente."""
    provider = os.getenv("ARCHON_LLM_PROVIDER", "mock").lower()
    if provider == "openai_compatible":
        return OpenAICompatibleClient()
    return MockLLMClient()
