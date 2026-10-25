"""Conversão de texto extraído de documentos brasileiros em valores tipados."""

from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

_DATA = re.compile(r"\d{1,4}[/.-]\d{1,2}[/.-]\d{2,4}")
_DATA_MES_ABREVIADO = re.compile(r"(\d{1,2})[/.-]([A-Za-z]{3})[/.-](\d{4})")
_FORMATOS_DATA = ("%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d")
_MESES = {
    "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12,
}  # fmt: skip


def converter_valor(texto: str) -> Decimal | None:
    """Converte "R$ 1.234,56" em Decimal("1234.56")."""
    limpo = re.sub(r"[^\d,.]", "", texto)
    if not limpo:
        return None
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        return Decimal(limpo)
    except InvalidOperation:
        return None


def converter_data(texto: str) -> date | None:
    """Encontra a primeira data no texto, aceitando os formatos usuais no Brasil."""
    abreviado = _DATA_MES_ABREVIADO.search(texto)
    if abreviado is not None and abreviado.group(2).upper() in _MESES:
        dia, mes, ano = abreviado.groups()
        try:
            return date(int(ano), _MESES[mes.upper()], int(dia))
        except ValueError:
            return None
    encontrado = _DATA.search(texto)
    if encontrado is None:
        return None
    for formato in _FORMATOS_DATA:
        try:
            return datetime.strptime(encontrado.group(), formato).date()
        except ValueError:
            continue
    return None
