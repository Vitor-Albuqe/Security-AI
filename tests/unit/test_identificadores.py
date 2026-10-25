import pytest

from security_ai.domain.value_objects import Cnpj, Cpf


def test_cpf_valido_aceita_texto_formatado():
    cpf = Cpf.de_texto("529.982.247-25")
    assert cpf.numero == "52998224725"
    assert cpf.formatado() == "529.982.247-25"


@pytest.mark.parametrize("texto", ["529.982.247-26", "111.111.111-11", "123"])
def test_cpf_invalido(texto):
    assert Cpf.tentar(texto) is None


def test_cnpj_valido_aceita_texto_formatado():
    cnpj = Cnpj.de_texto("11.222.333/0001-81")
    assert cnpj.formatado() == "11.222.333/0001-81"


@pytest.mark.parametrize("texto", ["11.222.333/0001-82", "00.000.000/0000-00", "1122"])
def test_cnpj_invalido(texto):
    assert Cnpj.tentar(texto) is None
