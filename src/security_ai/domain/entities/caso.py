"""Caso de análise: os sinais encontrados para um pedido, para revisão humana."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum


class Severidade(IntEnum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3


@dataclass(frozen=True, slots=True)
class Sinal:
    codigo: str
    descricao: str
    severidade: Severidade
    evidencias: tuple[str, ...] = ()


class StatusCaso(StrEnum):
    SEM_ALERTA = "sem_alerta"
    AGUARDANDO_REVISAO = "aguardando_revisao"


@dataclass(frozen=True, slots=True)
class CasoAnalise:
    """Sinais e pontuação de um pedido. Não é um veredito: a decisão é do auditor."""

    pedido_id: str
    sinais: tuple[Sinal, ...]
    pontuacao: float

    @property
    def status(self) -> StatusCaso:
        return StatusCaso.AGUARDANDO_REVISAO if self.sinais else StatusCaso.SEM_ALERTA
