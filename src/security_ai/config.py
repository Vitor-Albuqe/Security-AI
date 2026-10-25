"""Configuração lida de variáveis de ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Configuracao:
    openrouter_api_key: str | None
    openrouter_modelo: str | None
    openrouter_url: str
    pasta_dados: Path
    caminho_gabarito: Path

    @classmethod
    def do_ambiente(cls) -> Configuracao:
        return cls(
            openrouter_api_key=os.environ.get("OPENROUTER_API_KEY") or None,
            openrouter_modelo=os.environ.get("OPENROUTER_MODEL") or None,
            openrouter_url=os.environ.get(
                "OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions"
            ),
            pasta_dados=Path(os.environ.get("SECURITY_AI_DATA_DIR", "Data")),
            caminho_gabarito=Path(os.environ.get("SECURITY_AI_GABARITO", "train.jsonl")),
        )
