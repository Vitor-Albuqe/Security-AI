from security_ai.domain.entities import TipoCampo
from security_ai.infrastructure.document_reading import LeitorGabaritoDokki


def test_le_campos_do_gabarito(caminho_gabarito, pasta_dados):
    leitor = LeitorGabaritoDokki(caminho_gabarito)
    documento = leitor.ler(pasta_dados / "5c4c46b2-79b6-4ad3-8a1c-93c007fc8b4d.jpeg")

    assert documento.valores(TipoCampo.CNPJ) == ["09.102-287/0029-36"]
    assert documento.proveniencia.fonte == "gabarito:train.jsonl"


def test_todos_os_documentos_tem_total(caminho_gabarito, pasta_dados):
    leitor = LeitorGabaritoDokki(caminho_gabarito)
    for imagem in sorted(pasta_dados.glob("*.jpeg")):
        assert leitor.ler(imagem).valores(TipoCampo.TOTAL), imagem.name
