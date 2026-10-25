from __future__ import annotations

from typing import Protocol

from security_ai.domain.entities import Prestador
from security_ai.domain.value_objects import Cnpj


class CadastroPrestadores(Protocol):
    """Consulta a cadastros públicos (CNPJ, estabelecimentos de saúde)."""

    def buscar(self, cnpj: Cnpj) -> Prestador | None: ...
