"""Regras de detecção. Cada regra gera sinais explicáveis, nunca um veredito."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol

from security_ai.domain.entities import PedidoReembolso, Prestador, Severidade, Sinal


@dataclass(frozen=True, slots=True)
class ContextoAnalise:
    historico: Sequence[PedidoReembolso] = field(default_factory=tuple)
    prestador: Prestador | None = None


class Regra(Protocol):
    codigo: str

    def avaliar(self, pedido: PedidoReembolso, contexto: ContextoAnalise) -> list[Sinal]: ...


class RegraFracionamento:
    """Mesmo beneficiário, mesmo prestador e mesma data em mais de um pedido."""

    codigo = "FRACIONAMENTO"

    def avaliar(self, pedido: PedidoReembolso, contexto: ContextoAnalise) -> list[Sinal]:
        repetidos = [
            outro.id
            for outro in contexto.historico
            if outro.id != pedido.id
            and outro.beneficiario == pedido.beneficiario
            and outro.prestador == pedido.prestador
            and outro.data_atendimento == pedido.data_atendimento
        ]
        if not repetidos:
            return []
        return [
            Sinal(
                codigo=self.codigo,
                descricao=(
                    f"{len(repetidos) + 1} pedidos do mesmo beneficiário no mesmo prestador "
                    f"em {pedido.data_atendimento:%d/%m/%Y}"
                ),
                severidade=Severidade.ALTA,
                evidencias=tuple(repetidos),
            )
        ]


class RegraPrestadorIrregular:
    """Prestador ausente do cadastro público ou com situação cadastral diferente de ativa."""

    codigo = "PRESTADOR_IRREGULAR"

    def avaliar(self, pedido: PedidoReembolso, contexto: ContextoAnalise) -> list[Sinal]:
        prestador = contexto.prestador
        if prestador is None:
            return [
                Sinal(
                    codigo=self.codigo,
                    descricao=f"CNPJ {pedido.prestador.formatado()} não encontrado no cadastro",
                    severidade=Severidade.MEDIA,
                )
            ]
        if not prestador.ativo:
            return [
                Sinal(
                    codigo=self.codigo,
                    descricao=(
                        f"Prestador {prestador.razao_social} com situação cadastral "
                        f"{prestador.situacao_cadastral}"
                    ),
                    severidade=Severidade.ALTA,
                )
            ]
        return []


def regras_padrao() -> list[Regra]:
    return [RegraFracionamento(), RegraPrestadorIrregular()]
