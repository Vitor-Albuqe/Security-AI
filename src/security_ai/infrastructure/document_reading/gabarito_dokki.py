"""Leitor que devolve as anotações do gabarito (train.jsonl) em vez de chamar um modelo.

Serve como referência para medir o leitor real e para rodar o pipeline sem rede.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from security_ai.domain.entities import CampoExtraido, DocumentoLido, Proveniencia, TipoCampo

_ROTULOS = {t.value: t for t in TipoCampo}


class LeitorGabaritoDokki:
    def __init__(self, caminho_jsonl: Path) -> None:
        self._caminho = caminho_jsonl
        self._anotacoes: dict[str, dict[str, Any]] = {}
        with caminho_jsonl.open(encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip():
                    registro = json.loads(linha)
                    self._anotacoes[registro["imagePath"]] = registro

    def ler(self, caminho: Path) -> DocumentoLido:
        registro = self._anotacoes.get(caminho.name)
        if registro is None:
            raise KeyError(f"{caminho.name} não está no gabarito {self._caminho}")
        return DocumentoLido(
            id=registro["id"],
            caminho=str(caminho),
            campos=tuple(_agrupar_campos(registro["tokens"], registro["labels"])),
            proveniencia=Proveniencia(
                fonte=f"gabarito:{self._caminho.name}",
                registrado_em=datetime.now(UTC),
            ),
        )


def _agrupar_campos(tokens: list[str], rotulos: list[str]) -> list[CampoExtraido]:
    """Junta tokens consecutivos com o mesmo rótulo em um único campo."""
    campos: list[CampoExtraido] = []
    atual: TipoCampo | None = None
    partes: list[str] = []
    for token, rotulo in zip(tokens, rotulos, strict=True):
        tipo = _ROTULOS.get(rotulo)
        if tipo is not atual and partes and atual is not None:
            campos.append(CampoExtraido(atual, " ".join(partes)))
            partes = []
        atual = tipo
        if tipo is not None:
            partes.append(token)
    if partes and atual is not None:
        campos.append(CampoExtraido(atual, " ".join(partes)))
    return campos
