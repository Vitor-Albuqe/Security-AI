from datetime import date
from decimal import Decimal

from security_ai.application.use_cases import AnalisarPedido, ListarFilaAuditoria
from security_ai.domain.entities import PedidoReembolso, Prestador, StatusCaso
from security_ai.domain.value_objects import Cnpj, Cpf
from security_ai.infrastructure.external_data import CadastroPrestadoresEmMemoria
from security_ai.infrastructure.graph import GrafoEmMemoria
from security_ai.infrastructure.persistence import (
    RepositorioCasosEmMemoria,
    RepositorioPedidosEmMemoria,
)

CPF = Cpf.de_texto("529.982.247-25")
CNPJ = Cnpj.de_texto("11.222.333/0001-81")


def _montar():
    casos = RepositorioCasosEmMemoria()
    analisar = AnalisarPedido(
        pedidos=RepositorioPedidosEmMemoria(),
        cadastro=CadastroPrestadoresEmMemoria([Prestador(CNPJ, "Clínica X", "ATIVA")]),
        grafo=GrafoEmMemoria(),
        casos=casos,
    )
    return analisar, ListarFilaAuditoria(casos)


def _pedido(id_: str) -> PedidoReembolso:
    return PedidoReembolso(id_, CPF, CNPJ, date(2023, 3, 10), Decimal("300"))


def test_primeiro_pedido_nao_gera_alerta():
    analisar, _ = _montar()
    caso = analisar.executar(_pedido("a"))
    assert caso.status is StatusCaso.SEM_ALERTA
    assert caso.pontuacao == 0.0


def test_pedido_repetido_entra_na_fila_do_auditor():
    analisar, fila = _montar()
    analisar.executar(_pedido("a"))
    caso = analisar.executar(_pedido("b"))

    assert caso.status is StatusCaso.AGUARDANDO_REVISAO
    assert [s.codigo for s in caso.sinais] == ["FRACIONAMENTO"]
    assert [c.pedido_id for c in fila.executar()] == ["b"]
