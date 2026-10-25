"""Leitor que envia a imagem a um modelo de visão pela API do OpenRouter."""

from __future__ import annotations

import base64
import json
import mimetypes
import urllib.request
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from security_ai.domain.entities import CampoExtraido, DocumentoLido, Proveniencia, TipoCampo

PROMPT = (
    "Você recebe a imagem de um documento brasileiro de pagamento (recibo, nota fiscal ou "
    "comprovante). Responda somente com um objeto JSON com as chaves "
    '"cnpj", "cpf", "data" e "total", copiando o texto exatamente como aparece. '
    "Use null quando o campo não existir."
)


class LeitorOpenRouter:
    def __init__(self, api_key: str, modelo: str, url: str, timeout: float = 120.0) -> None:
        self._api_key = api_key
        self._modelo = modelo
        self._url = url
        self._timeout = timeout

    def ler(self, caminho: Path) -> DocumentoLido:
        resposta = self._chamar(caminho)
        conteudo = resposta["choices"][0]["message"]["content"]
        return DocumentoLido(
            id=str(uuid.uuid4()),
            caminho=str(caminho),
            campos=tuple(_campos_da_resposta(conteudo)),
            proveniencia=Proveniencia(
                fonte=f"openrouter:{self._modelo}",
                registrado_em=datetime.now(UTC),
            ),
        )

    def _chamar(self, caminho: Path) -> dict[str, Any]:
        tipo = mimetypes.guess_type(caminho.name)[0] or "image/jpeg"
        imagem = base64.b64encode(caminho.read_bytes()).decode("ascii")
        corpo = {
            "model": self._modelo,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:{tipo};base64,{imagem}"}},
                    ],
                }
            ],
        }
        requisicao = urllib.request.Request(
            self._url,
            data=json.dumps(corpo).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(requisicao, timeout=self._timeout) as resposta:
            dados: dict[str, Any] = json.loads(resposta.read())
            return dados


def _campos_da_resposta(conteudo: str) -> list[CampoExtraido]:
    inicio, fim = conteudo.find("{"), conteudo.rfind("}")
    if inicio == -1 or fim == -1:
        raise ValueError(f"Resposta do modelo sem JSON: {conteudo[:200]!r}")
    dados = json.loads(conteudo[inicio : fim + 1])
    return [
        CampoExtraido(tipo, str(dados[tipo.value]))
        for tipo in TipoCampo
        if dados.get(tipo.value) not in (None, "")
    ]
