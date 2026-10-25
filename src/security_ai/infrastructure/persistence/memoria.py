from __future__ import annotations

from security_ai.domain.entities import CasoAnalise, DocumentoLido, PedidoReembolso
from security_ai.domain.value_objects import Cpf


class RepositorioDocumentosEmMemoria:
    def __init__(self) -> None:
        self._itens: dict[str, DocumentoLido] = {}

    def salvar(self, documento: DocumentoLido) -> None:
        self._itens[documento.id] = documento

    def obter(self, documento_id: str) -> DocumentoLido | None:
        return self._itens.get(documento_id)


class RepositorioPedidosEmMemoria:
    def __init__(self) -> None:
        self._itens: dict[str, PedidoReembolso] = {}

    def salvar(self, pedido: PedidoReembolso) -> None:
        self._itens[pedido.id] = pedido

    def listar_por_beneficiario(self, cpf: Cpf) -> list[PedidoReembolso]:
        return [p for p in self._itens.values() if p.beneficiario == cpf]


class RepositorioCasosEmMemoria:
    def __init__(self) -> None:
        self._itens: dict[str, CasoAnalise] = {}

    def salvar(self, caso: CasoAnalise) -> None:
        self._itens[caso.pedido_id] = caso

    def listar(self) -> list[CasoAnalise]:
        return list(self._itens.values())
