from __future__ import annotations

from pathlib import Path

from security_ai.application.ports import LeitorDocumentos, RepositorioDocumentos
from security_ai.domain.entities import DocumentoLido


class LerDocumento:
    """Lê um documento e guarda o resultado com sua proveniência."""

    def __init__(self, leitor: LeitorDocumentos, documentos: RepositorioDocumentos) -> None:
        self._leitor = leitor
        self._documentos = documentos

    def executar(self, caminho: Path) -> DocumentoLido:
        documento = self._leitor.ler(caminho)
        self._documentos.salvar(documento)
        return documento
