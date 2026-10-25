from __future__ import annotations

from collections.abc import Sequence

from security_ai.application.ports import (
    CadastroPrestadores,
    GrafoRelacoes,
    RepositorioCasos,
    RepositorioPedidos,
)
from security_ai.domain.entities import CasoAnalise, PedidoReembolso
from security_ai.domain.services import ContextoAnalise, Regra, pontuar, regras_padrao


class AnalisarPedido:
    """Cruza o pedido com histórico, cadastro e grafo, e abre um caso para o auditor."""

    def __init__(
        self,
        pedidos: RepositorioPedidos,
        cadastro: CadastroPrestadores,
        grafo: GrafoRelacoes,
        casos: RepositorioCasos,
        regras: Sequence[Regra] | None = None,
    ) -> None:
        self._pedidos = pedidos
        self._cadastro = cadastro
        self._grafo = grafo
        self._casos = casos
        self._regras = list(regras) if regras is not None else regras_padrao()

    def executar(self, pedido: PedidoReembolso) -> CasoAnalise:
        contexto = ContextoAnalise(
            historico=self._pedidos.listar_por_beneficiario(pedido.beneficiario),
            prestador=self._cadastro.buscar(pedido.prestador),
        )
        self._pedidos.salvar(pedido)
        self._grafo.registrar(pedido)

        sinais = [s for regra in self._regras for s in regra.avaliar(pedido, contexto)]
        sinais += self._grafo.sinais_de_rede(pedido)

        caso = CasoAnalise(pedido_id=pedido.id, sinais=tuple(sinais), pontuacao=pontuar(sinais))
        self._casos.salvar(caso)
        return caso
