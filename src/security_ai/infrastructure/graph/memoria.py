from __future__ import annotations

from collections import defaultdict

from security_ai.domain.entities import PedidoReembolso, Sinal
from security_ai.domain.value_objects import Cnpj, Cpf


class GrafoEmMemoria:
    """Guarda as arestas beneficiário–prestador. Ainda não gera sinais de rede.

    A detecção de padrões de rede entra com o adaptador Neo4j (ver roadmap).
    """

    def __init__(self) -> None:
        self.prestadores_por_beneficiario: dict[Cpf, set[Cnpj]] = defaultdict(set)

    def registrar(self, pedido: PedidoReembolso) -> None:
        self.prestadores_por_beneficiario[pedido.beneficiario].add(pedido.prestador)

    def sinais_de_rede(self, pedido: PedidoReembolso) -> list[Sinal]:
        return []
