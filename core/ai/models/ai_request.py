"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_request.py

Descrição:
Modelo oficial de requisição da camada IA.

Representa tudo que o Genesis envia
para um Provider de Inteligência Artificial.

Responsável por transportar:

- Prompt
- Histórico de conversa
- Persona
- Configurações do modelo
- Contexto cognitivo
- Metadados

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
from uuid import uuid4
from typing import Any

from core.ai.models.ai_message import AIMessage



@dataclass(slots=True)
class AIRequest:
    """
    Estrutura padrão de uma requisição IA.
    """


    # =====================================================
    # IDENTIDADE
    # =====================================================

    request_id: str = field(
        default_factory=lambda: str(uuid4())
    )


    created_at: datetime = field(
        default_factory=datetime.now
    )


    # =====================================================
    # CONTEÚDO
    # =====================================================

    prompt: str = ""


    system_prompt: str = ""


    messages: list[AIMessage] = field(
        default_factory=list
    )


    # =====================================================
    # PERSONA / COGNIÇÃO
    # =====================================================

    persona: str = "jarvis"


    intention: str | None = None


    priority: str = "normal"


    # =====================================================
    # CONFIGURAÇÃO DO MODELO
    # =====================================================

    temperature: float = 0.7


    max_tokens: int | None = None


    model: str | None = None


    stream: bool = False



    # =====================================================
    # CONTEXTO
    # =====================================================

    context: dict[str, Any] = field(
        default_factory=dict
    )


    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # =====================================================
    # UTILIDADES
    # =====================================================

    def add_message(
        self,
        message: AIMessage
    ) -> None:
        """
        Adiciona uma mensagem ao histórico.
        """


        self.messages.append(
            message
        )



    def message_dicts(self) -> list[dict]:
        """
        Converte mensagens para formato
        aceito pelos providers.
        """


        return [

            message.to_dict()

            for message in self.messages

        ]



    def has_history(self) -> bool:
        """
        Verifica se existe contexto
        conversacional.
        """


        return len(
            self.messages
        ) > 0



    def to_dict(self) -> dict[str, Any]:
        """
        Serialização para logs/debug.
        """


        return {

            "request_id":
                self.request_id,

            "prompt":
                self.prompt,

            "system_prompt":
                self.system_prompt,

            "persona":
                self.persona,

            "intention":
                self.intention,

            "priority":
                self.priority,

            "temperature":
                self.temperature,

            "max_tokens":
                self.max_tokens,

            "model":
                self.model,

            "stream":
                self.stream,

            "messages":
                self.message_dicts(),

            "context":
                self.context,

            "metadata":
                self.metadata

        }



    def __repr__(self) -> str:

        return (

            "AIRequest("

            f"id='{self.request_id[:8]}', "

            f"persona='{self.persona}', "

            f"prompt='{self.prompt[:40]}'"

            ")"

        )