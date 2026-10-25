"""Composição dos sinais em uma pontuação de prioridade para a fila do auditor."""

from __future__ import annotations

from collections.abc import Iterable

from security_ai.domain.entities import Severidade, Sinal

PESOS: dict[Severidade, float] = {
    Severidade.BAIXA: 0.2,
    Severidade.MEDIA: 0.5,
    Severidade.ALTA: 0.8,
}


def pontuar(sinais: Iterable[Sinal]) -> float:
    """Combina sinais como evidências independentes: 1 - Π(1 - peso). Resultado em [0, 1)."""
    restante = 1.0
    for sinal in sinais:
        restante *= 1.0 - PESOS[sinal.severidade]
    return round(1.0 - restante, 4)
