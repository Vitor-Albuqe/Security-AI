"""Pedido de reembolso e as partes envolvidas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from security_ai.domain.value_objects import Cnpj, Cpf


@dataclass(frozen=True, slots=True)
class Prestador:
    cnpj: Cnpj
    razao_social: str
    situacao_cadastral: str
    cnae_principal: str | None = None

    @property
    def ativo(self) -> bool:
        return self.situacao_cadastral.strip().upper() == "ATIVA"


@dataclass(frozen=True, slots=True)
class PedidoReembolso:
    id: str
    beneficiario: Cpf
    prestador: Cnpj
    data_atendimento: date
    valor: Decimal
    documentos: tuple[str, ...] = ()
