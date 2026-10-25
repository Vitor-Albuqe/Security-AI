from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


@pytest.fixture
def caminho_gabarito() -> Path:
    caminho = RAIZ / "train.jsonl"
    if not caminho.exists():
        pytest.skip("train.jsonl não encontrado")
    return caminho


@pytest.fixture
def pasta_dados() -> Path:
    pasta = RAIZ / "Data"
    if not any(pasta.glob("*.jpeg")):
        pytest.skip("imagens de Data/ não encontradas (ficam fora do git)")
    return pasta
