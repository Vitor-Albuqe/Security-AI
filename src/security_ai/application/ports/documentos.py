from __future__ import annotations

from pathlib import Path
from typing import Protocol

from security_ai.domain.entities import DocumentoLido


class LeitorDocumentos(Protocol):
    """Extrai campos de uma imagem ou PDF de documento de reembolso."""

    def ler(self, caminho: Path) -> DocumentoLido: ...


class RepositorioDocumentos(Protocol):
    def salvar(self, documento: DocumentoLido) -> None: ...

    def obter(self, documento_id: str) -> DocumentoLido | None: ...
