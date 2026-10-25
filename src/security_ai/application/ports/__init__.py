"""Contratos entre a aplicação e os adaptadores externos."""

from security_ai.application.ports.dados_externos import CadastroPrestadores
from security_ai.application.ports.documentos import LeitorDocumentos, RepositorioDocumentos
from security_ai.application.ports.grafo import GrafoRelacoes
from security_ai.application.ports.repositorios import RepositorioCasos, RepositorioPedidos

__all__ = [
    "CadastroPrestadores",
    "GrafoRelacoes",
    "LeitorDocumentos",
    "RepositorioCasos",
    "RepositorioDocumentos",
    "RepositorioPedidos",
]
