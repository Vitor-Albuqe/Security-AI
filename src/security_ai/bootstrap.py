"""Raiz de composição: o único lugar que escolhe quais adaptadores concretos usar."""

from __future__ import annotations

from typing import Literal

from security_ai.application.ports import LeitorDocumentos
from security_ai.config import Configuracao
from security_ai.infrastructure.document_reading import LeitorGabaritoDokki, LeitorOpenRouter

OrigemLeitura = Literal["gabarito", "openrouter"]


def montar_leitor(config: Configuracao, origem: OrigemLeitura) -> LeitorDocumentos:
    if origem == "gabarito":
        return LeitorGabaritoDokki(config.caminho_gabarito)
    if not config.openrouter_api_key or not config.openrouter_modelo:
        raise RuntimeError("Defina OPENROUTER_API_KEY e OPENROUTER_MODEL (veja .env.example).")
    return LeitorOpenRouter(
        api_key=config.openrouter_api_key,
        modelo=config.openrouter_modelo,
        url=config.openrouter_url,
    )
