"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_message.py

Descrição:
Modelo oficial de mensagens da camada IA.

Responsável por padronizar conversas
entre Genesis Core e Providers externos.

Compatível com:

- Ollama
- OpenAI
- Gemini
- Claude
- Mock Provider

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class AIMessage:
    """
    Representa uma mensagem individual
    dentro de uma conversa IA.
    """


    # =====================================================
    # TIPOS DE MENSAGEM
    # =====================================================

    role: str

    content: str


    # =====================================================
    # IDENTIFICAÇÃO
    # =====================================================

    name: str | None = None


    # =====================================================
    # CONTROLE
    # =====================================================

    timestamp: datetime = field(
        default_factory=datetime.now
    )


    metadata: dict[str, Any] = field(
        default_factory=dict
    )


    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    VALID_ROLES = {

        "system",

        "user",

        "assistant",

        "tool"

    }


    def __post_init__(self) -> None:
        """
        Valida criação da mensagem.
        """


        self.role = self.role.lower().strip()


        if self.role not in self.VALID_ROLES:

            raise ValueError(
                f"Role inválido: {self.role}. "
                f"Permitidos: {self.VALID_ROLES}"
            )


        if not isinstance(
            self.content,
            str
        ):

            raise TypeError(
                "Content deve ser string."
            )



    # =====================================================
    # CONVERSÃO PROVIDERS
    # =====================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Converte para formato universal
        aceito pelos providers.
        """


        data = {

            "role":
                self.role,

            "content":
                self.content

        }


        if self.name:

            data["name"] = self.name


        return data



    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any]
    ) -> "AIMessage":
        """
        Cria mensagem a partir de um dict.
        """


        return cls(

            role=data.get(
                "role",
                "user"
            ),

            content=data.get(
                "content",
                ""
            ),

            name=data.get(
                "name"
            ),

            metadata=data.get(
                "metadata",
                {}
            )

        )



    # =====================================================
    # DEBUG
    # =====================================================

    def __repr__(self) -> str:

        return (
            "AIMessage("
            f"role='{self.role}', "
            f"content='{self.content[:40]}'"
            ")"
        )