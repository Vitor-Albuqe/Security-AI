from __future__ import annotations

from typing import Protocol

from security_ai.domain.entities import PedidoReembolso, Sinal


class GrafoRelacoes(Protocol):
    """Registra relações entre beneficiários, prestadores e contas, e detecta padrões de rede."""

    def registrar(self, pedido: PedidoReembolso) -> None: ...

    def sinais_de_rede(self, pedido: PedidoReembolso) -> list[Sinal]: ...
