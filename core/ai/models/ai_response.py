"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_response.py

Descrição:
Modelo oficial de resposta da camada IA.

Representa a resposta produzida por
qualquer Provider integrado ao Genesis.

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
from uuid import uuid4



@dataclass(slots=True)
class AIResponse:
    """
    Estrutura padrão de resposta
    produzida pela camada IA.
    """


    # =====================================================
    # IDENTIDADE
    # =====================================================

    response_id: str = field(
        default_factory=lambda: str(uuid4())
    )


    request_id: str | None = None


    created_at: datetime = field(
        default_factory=datetime.now
    )


    # =====================================================
    # RESULTADO
    # =====================================================

    success: bool = True


    content: str = ""


    persona: str = "jarvis"



    # =====================================================
    # PROVIDER
    # =====================================================

    provider: str = ""


    model: str = ""



    # =====================================================
    # STREAMING
    # =====================================================

    stream: bool = False


    completed: bool = False


    chunks: list[str] = field(
        default_factory=list
    )


    finish_reason: str | None = None



    # =====================================================
    # TOOL CALLING
    # =====================================================

    tool_calls: list[dict[str, Any]] = field(
        default_factory=list
    )



    # =====================================================
    # MULTIMODAL
    # =====================================================

    attachments: list[Any] = field(
        default_factory=list
    )



    # =====================================================
    # PERFORMANCE
    # =====================================================

    latency: float = 0.0



    # =====================================================
    # TOKENS
    # =====================================================

    prompt_tokens: int = 0


    completion_tokens: int = 0


    total_tokens: int = 0



    # =====================================================
    # DIAGNÓSTICO
    # =====================================================

    error: str | None = None


    warnings: list[str] = field(
        default_factory=list
    )


    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # =====================================================
    # PROPRIEDADES
    # =====================================================

    @property
    def failed(self) -> bool:
        """
        Indica se houve falha.
        """

        return not self.success



    @property
    def empty(self) -> bool:
        """
        Verifica se a resposta está vazia.
        """

        return not bool(
            (self.content or "").strip()
        )



    @property
    def has_content(self) -> bool:
        """
        Verifica se existe conteúdo.
        """

        return not self.empty



    @property
    def has_chunks(self) -> bool:
        return bool(
            self.chunks
        )



    @property
    def has_tool_calls(self) -> bool:
        return bool(
            self.tool_calls
        )



    @property
    def has_attachments(self) -> bool:
        return bool(
            self.attachments
        )



    # =====================================================
    # STREAMING
    # =====================================================

    def add_chunk(
        self,
        chunk: str
    ) -> None:

        self.chunks.append(
            chunk
        )


        self.content += chunk



    def complete(
        self,
        reason: str = "stop"
    ) -> None:
        """
        Finaliza resposta.
        """

        self.completed = True

        self.finish_reason = reason



    # =====================================================
    # TOOL CALLING
    # =====================================================

    def add_tool_call(
        self,
        tool_call: dict[str, Any]
    ) -> None:

        self.tool_calls.append(
            tool_call
        )



    # =====================================================
    # ANEXOS
    # =====================================================

    def add_attachment(
        self,
        attachment: Any
    ) -> None:

        self.attachments.append(
            attachment
        )



    # =====================================================
    # AVISOS
    # =====================================================

    def add_warning(
        self,
        warning: str
    ) -> None:

        self.warnings.append(
            warning
        )



    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================

    def to_dict(
        self
    ) -> dict[str, Any]:

        return {

            "response_id":
                self.response_id,


            "request_id":
                self.request_id,


            "created_at":
                self.created_at.isoformat(),


            "success":
                self.success,


            "content":
                self.content,


            "persona":
                self.persona,


            "provider":
                self.provider,


            "model":
                self.model,


            "stream":
                self.stream,


            "completed":
                self.completed,


            "finish_reason":
                self.finish_reason,


            "chunks":
                list(self.chunks),


            "tool_calls":
                list(self.tool_calls),


            "attachments":
                list(self.attachments),


            "latency":
                self.latency,


            "prompt_tokens":
                self.prompt_tokens,


            "completion_tokens":
                self.completion_tokens,


            "total_tokens":
                self.total_tokens,


            "error":
                self.error,


            "warnings":
                list(self.warnings),


            "metadata":
                dict(self.metadata)

        }



    # =====================================================
    # CONSTRUTORES
    # =====================================================

    @classmethod
    def failure(
        cls,
        error: str,
        provider: str = "unknown",
        model: str = "unknown",
        persona: str = "jarvis"
    ) -> "AIResponse":


        return cls(

            success=False,

            content="",

            provider=provider,

            model=model,

            persona=persona,

            error=error,

            completed=True,

            finish_reason="error"

        )



    @classmethod
    def success_response(
        cls,
        content: str,
        provider: str,
        model: str,
        persona: str = "jarvis"
    ) -> "AIResponse":


        return cls(

            success=True,

            content=content,

            provider=provider,

            model=model,

            persona=persona,

            completed=True,

            finish_reason="stop"

        )



    # =====================================================
    # DEBUG
    # =====================================================

    def __repr__(self) -> str:


        preview = (
            self.content or ""
        ).replace(
            "\n",
            " "
        )


        if len(preview) > 40:

            preview = preview[:40] + "..."


        return (

            "AIResponse("

            f"provider='{self.provider}', "

            f"model='{self.model}', "

            f"success={self.success}, "

            f"completed={self.completed}, "

            f"content='{preview}'"

            ")"

        )