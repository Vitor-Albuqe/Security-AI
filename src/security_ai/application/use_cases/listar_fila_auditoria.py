from __future__ import annotations

from security_ai.application.ports import RepositorioCasos
from security_ai.domain.entities import CasoAnalise, StatusCaso


class ListarFilaAuditoria:
    """Casos com alerta, do mais prioritário para o menos."""

    def __init__(self, casos: RepositorioCasos) -> None:
        self._casos = casos

    def executar(self) -> list[CasoAnalise]:
        pendentes = [c for c in self._casos.listar() if c.status is StatusCaso.AGUARDANDO_REVISAO]
        return sorted(pendentes, key=lambda c: c.pontuacao, reverse=True)
