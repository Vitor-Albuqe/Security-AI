from datetime import date
from decimal import Decimal

from security_ai.domain.entities import PedidoReembolso, Prestador, Severidade, Sinal
from security_ai.domain.services import (
    ContextoAnalise,
    RegraFracionamento,
    RegraPrestadorIrregular,
    pontuar,
)
from security_ai.domain.value_objects import Cnpj, Cpf

CPF = Cpf.de_texto("529.982.247-25")
CNPJ = Cnpj.de_texto("11.222.333/0001-81")


def _pedido(id_: str, dia: int = 10) -> PedidoReembolso:
    return PedidoReembolso(id_, CPF, CNPJ, date(2023, 3, dia), Decimal("300"))


def test_fracionamento_detecta_mesmo_cpf_clinica_e_data():
    sinais = RegraFracionamento().avaliar(
        _pedido("b"), ContextoAnalise(historico=[_pedido("a")])
    )
    assert len(sinais) == 1
    assert sinais[0].severidade is Severidade.ALTA
    assert sinais[0].evidencias == ("a",)


def test_fracionamento_ignora_datas_diferentes():
    contexto = ContextoAnalise(historico=[_pedido("a", dia=11)])
    assert RegraFracionamento().avaliar(_pedido("b"), contexto) == []


def test_prestador_fora_do_cadastro_gera_sinal_medio():
    sinais = RegraPrestadorIrregular().avaliar(_pedido("a"), ContextoAnalise())
    assert [s.severidade for s in sinais] == [Severidade.MEDIA]


def test_prestador_baixado_gera_sinal_alto():
    prestador = Prestador(CNPJ, "Clínica X", "BAIXADA")
    sinais = RegraPrestadorIrregular().avaliar(_pedido("a"), ContextoAnalise(prestador=prestador))
    assert [s.severidade for s in sinais] == [Severidade.ALTA]


def test_prestador_ativo_nao_gera_sinal():
    prestador = Prestador(CNPJ, "Clínica X", "ATIVA")
    assert RegraPrestadorIrregular().avaliar(_pedido("a"), ContextoAnalise(prestador=prestador)) == []


def test_pontuacao_combina_sinais():
    alto = Sinal("X", "", Severidade.ALTA)
    medio = Sinal("Y", "", Severidade.MEDIA)
    assert pontuar([]) == 0.0
    assert pontuar([alto]) == 0.8
    assert pontuar([alto, medio]) == 0.9
