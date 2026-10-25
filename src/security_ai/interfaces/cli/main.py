"""Linha de comando: `security-ai ler <imagem>` ou `python -m security_ai ler <imagem>`."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from security_ai.application.use_cases import LerDocumento
from security_ai.bootstrap import montar_leitor
from security_ai.config import Configuracao
from security_ai.infrastructure.persistence import RepositorioDocumentosEmMemoria


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="security-ai")
    comandos = parser.add_subparsers(dest="comando", required=True)
    ler = comandos.add_parser("ler", help="extrai CNPJ, CPF, data e total de um documento")
    ler.add_argument("caminho", type=Path)
    ler.add_argument("--leitor", choices=["gabarito", "openrouter"], default="gabarito")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    config = Configuracao.do_ambiente()
    caso_de_uso = LerDocumento(montar_leitor(config, args.leitor), RepositorioDocumentosEmMemoria())
    documento = caso_de_uso.executar(args.caminho)
    saida = {
        "id": documento.id,
        "caminho": documento.caminho,
        "fonte": documento.proveniencia.fonte,
        "registrado_em": documento.proveniencia.registrado_em.isoformat(),
        "campos": [{"tipo": c.tipo.value, "valor": c.valor_bruto} for c in documento.campos],
    }
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    return 0
