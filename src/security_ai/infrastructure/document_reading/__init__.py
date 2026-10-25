"""Integração com modelos de leitura de documentos."""

from security_ai.infrastructure.document_reading.gabarito_dokki import LeitorGabaritoDokki
from security_ai.infrastructure.document_reading.openrouter import LeitorOpenRouter

__all__ = ["LeitorGabaritoDokki", "LeitorOpenRouter"]
