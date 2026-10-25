from __future__ import annotations

from typing import Protocol

from security_ai.domain.entities import CasoAnalise, PedidoReembolso
from security_ai.domain.value_objects import Cpf


class RepositorioPedidos(Protocol):
    def salvar(self, pedido: PedidoReembolso) -> None: ...

    def listar_por_beneficiario(self, cpf: Cpf) -> list[PedidoReembolso]: ...


class RepositorioCasos(Protocol):
    def salvar(self, caso: CasoAnalise) -> None: ...

    def listar(self) -> list[CasoAnalise]: ...
