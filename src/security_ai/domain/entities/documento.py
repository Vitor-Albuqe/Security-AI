"""Documento lido e os campos extraídos dele, com proveniência."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class TipoCampo(StrEnum):
    CNPJ = "cnpj"
    CPF = "cpf"
    DATA = "data"
    TOTAL = "total"


@dataclass(frozen=True, slots=True)
class Proveniencia:
    fonte: str
    registrado_em: datetime


@dataclass(frozen=True, slots=True)
class CampoExtraido:
    tipo: TipoCampo
    valor_bruto: str
    confianca: float | None = None


@dataclass(frozen=True, slots=True)
class DocumentoLido:
    id: str
    caminho: str
    campos: tuple[CampoExtraido, ...]
    proveniencia: Proveniencia

    def valores(self, tipo: TipoCampo) -> list[str]:
        return [c.valor_bruto for c in self.campos if c.tipo is tipo]
