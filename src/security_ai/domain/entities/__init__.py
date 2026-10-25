"""Entidades do domínio."""

from security_ai.domain.entities.caso import CasoAnalise, Severidade, Sinal, StatusCaso
from security_ai.domain.entities.documento import (
    CampoExtraido,
    DocumentoLido,
    Proveniencia,
    TipoCampo,
)
from security_ai.domain.entities.reembolso import PedidoReembolso, Prestador

__all__ = [
    "CampoExtraido",
    "CasoAnalise",
    "DocumentoLido",
    "PedidoReembolso",
    "Prestador",
    "Proveniencia",
    "Severidade",
    "Sinal",
    "StatusCaso",
    "TipoCampo",
]
