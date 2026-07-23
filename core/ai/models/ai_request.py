"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_request.py

Descrição:
Modelo oficial de requisição da camada IA.

Representa uma solicitação enviada pelo
Genesis Core para um Provider.

O Request contém o objetivo da execução.

O estado cognitivo permanece no AIContext.

Arquitetura:

Genesis Core

Mark:
V - Evolution
=========================================
"""


from __future__ import annotations


from dataclasses import dataclass, field

from datetime import datetime

from uuid import uuid4

from typing import Any


from core.ai.models.ai_context import AIContext



@dataclass(slots=True)
class AIRequest:
    """
    Solicitação de processamento IA.
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



    session_id: str | None = None



    # =====================================================
    # CONTEÚDO
    # =====================================================


    prompt: str = ""



    system_prompt: str | None = None



    # =====================================================
    # CONTEXTO COGNITIVO
    # =====================================================


    context: AIContext | None = None



    # =====================================================
    # PROVIDER
    # =====================================================


    preferred_provider: str | None = None


    model: str | None = None



    # =====================================================
    # PARÂMETROS DE GERAÇÃO
    # =====================================================


    temperature: float = 0.7


    top_p: float = 1.0


    max_tokens: int | None = None


    seed: int | None = None


    timeout: float | None = None


    stream: bool = False



    stop_sequences: list[str] = field(
        default_factory=list
    )



    # =====================================================
    # FERRAMENTAS
    # =====================================================


    allowed_tools: list[str] = field(
        default_factory=list
    )



    attachments: list[Any] = field(
        default_factory=list
    )



    # =====================================================
    # METADATA
    # =====================================================


    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # =====================================================
    # UTILIDADES
    # =====================================================


    def add_tool(
        self,
        tool_name: str
    ):


        if tool_name not in self.allowed_tools:

            self.allowed_tools.append(
                tool_name
            )



    def has_context(self) -> bool:


        return self.context is not None



    def to_dict(self):


        return {


            "request_id":
                self.request_id,


            "created_at":
                self.created_at.isoformat(),


            "session_id":
                self.session_id,


            "prompt":
                self.prompt,


            "system_prompt":
                self.system_prompt,


            "context":

                self.context.to_dict()

                if self.context

                else None,



            "provider":
                self.preferred_provider,


            "model":
                self.model,


            "temperature":
                self.temperature,


            "top_p":
                self.top_p,


            "max_tokens":
                self.max_tokens,


            "stream":
                self.stream,


            "tools":
                self.allowed_tools,


            "metadata":
                self.metadata

        }



    def __repr__(self):


        return (

            "AIRequest("

            f"id='{self.request_id[:8]}', "

            f"model='{self.model}', "

            f"stream={self.stream}"

            ")"

        )