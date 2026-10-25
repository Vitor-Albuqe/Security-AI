import json

from security_ai.interfaces.cli.main import main


def test_cli_ler_com_gabarito(caminho_gabarito, pasta_dados, monkeypatch, capsys):
    monkeypatch.setenv("SECURITY_AI_GABARITO", str(caminho_gabarito))
    imagem = pasta_dados / "5c4c46b2-79b6-4ad3-8a1c-93c007fc8b4d.jpeg"

    assert main(["ler", str(imagem)]) == 0

    saida = json.loads(capsys.readouterr().out)
    assert saida["fonte"] == "gabarito:train.jsonl"
    assert {"tipo": "cnpj", "valor": "09.102-287/0029-36"} in saida["campos"]
