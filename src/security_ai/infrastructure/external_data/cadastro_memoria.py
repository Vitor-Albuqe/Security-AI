from __future__ import annotations

from collections.abc import Iterable

from security_ai.domain.entities import Prestador
from security_ai.domain.value_objects import Cnpj


class CadastroPrestadoresEmMemoria:
    """Cadastro carregado em memória; substituto da consulta a dados públicos de CNPJ."""

    def __init__(self, prestadores: Iterable[Prestador] = ()) -> None:
        self._por_cnpj = {p.cnpj: p for p in prestadores}

    def buscar(self, cnpj: Cnpj) -> Prestador | None:
        return self._por_cnpj.get(cnpj)
