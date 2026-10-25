"""CPF e CNPJ com validação dos dígitos verificadores."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

_PESOS_CNPJ_1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_PESOS_CNPJ_2 = (6, *_PESOS_CNPJ_1)


def _somente_digitos(texto: str) -> str:
    return "".join(c for c in texto if c.isdigit())


def _cpf_valido(numero: str) -> bool:
    if len(numero) != 11 or len(set(numero)) == 1:
        return False
    digitos = [int(c) for c in numero]
    for tamanho in (9, 10):
        soma = sum(d * p for d, p in zip(digitos[:tamanho], range(tamanho + 1, 1, -1), strict=True))
        if (soma * 10 % 11) % 10 != digitos[tamanho]:
            return False
    return True


def _cnpj_valido(numero: str) -> bool:
    if len(numero) != 14 or len(set(numero)) == 1:
        return False
    digitos = [int(c) for c in numero]
    for pesos in (_PESOS_CNPJ_1, _PESOS_CNPJ_2):
        resto = sum(d * p for d, p in zip(digitos, pesos, strict=False)) % 11
        esperado = 0 if resto < 2 else 11 - resto
        if esperado != digitos[len(pesos)]:
            return False
    return True


@dataclass(frozen=True, slots=True)
class Cpf:
    numero: str

    def __post_init__(self) -> None:
        if not _cpf_valido(self.numero):
            raise ValueError(f"CPF inválido: {self.numero!r}")

    @classmethod
    def de_texto(cls, texto: str) -> Self:
        return cls(_somente_digitos(texto))

    @classmethod
    def tentar(cls, texto: str) -> Self | None:
        """Retorna None em vez de erro; útil para texto vindo de OCR."""
        try:
            return cls.de_texto(texto)
        except ValueError:
            return None

    def formatado(self) -> str:
        n = self.numero
        return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"


@dataclass(frozen=True, slots=True)
class Cnpj:
    numero: str

    def __post_init__(self) -> None:
        if not _cnpj_valido(self.numero):
            raise ValueError(f"CNPJ inválido: {self.numero!r}")

    @classmethod
    def de_texto(cls, texto: str) -> Self:
        return cls(_somente_digitos(texto))

    @classmethod
    def tentar(cls, texto: str) -> Self | None:
        """Retorna None em vez de erro; útil para texto vindo de OCR."""
        try:
            return cls.de_texto(texto)
        except ValueError:
            return None

    def formatado(self) -> str:
        n = self.numero
        return f"{n[:2]}.{n[2:5]}.{n[5:8]}/{n[8:12]}-{n[12:]}"
