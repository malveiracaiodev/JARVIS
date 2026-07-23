"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_response.py

Descrição:
Modelo oficial de resposta da camada
de Inteligência Artificial.

Representa a resposta produzida por
qualquer Provider integrado ao Genesis.

Responsável por transportar:

- Conteúdo gerado
- Informações do Provider
- Modelo utilizado
- Tokens
- Streaming
- Tool Calling
- Métricas
- Diagnóstico
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

    persona: str | None = None

    # =====================================================
    # PROVIDER
    # =====================================================

    provider: str = ""

    model: str = ""

    # =====================================================
    # STREAMING
    # =====================================================

    stream: bool = False

    completed: bool = True

    chunks: list[str] = field(
        default_factory=list
    )

    finish_reason: str = "completed"

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
            self.content.strip()
        )

    @property
    def has_chunks(self) -> bool:
        """
        Indica se existem chunks.
        """

        return bool(self.chunks)

    @property
    def has_tool_calls(self) -> bool:
        """
        Indica se houve Tool Calling.
        """

        return bool(self.tool_calls)

    @property
    def has_attachments(self) -> bool:
        """
        Indica se existem anexos.
        """

        return bool(self.attachments)

    # =====================================================
    # UTILIDADES
    # =====================================================

    def add_chunk(
        self,
        chunk: str
    ) -> None:
        """
        Adiciona um chunk recebido
        durante streaming.
        """

        self.chunks.append(chunk)

        self.content += chunk

    def add_tool_call(
        self,
        tool_call: dict[str, Any]
    ) -> None:
        """
        Registra uma chamada de ferramenta.
        """

        self.tool_calls.append(tool_call)

    def add_attachment(
        self,
        attachment: Any
    ) -> None:
        """
        Adiciona um anexo retornado
        pelo Provider.
        """

        self.attachments.append(
            attachment
        )

    def add_warning(
        self,
        warning: str
    ) -> None:
        """
        Registra um aviso.
        """

        self.warnings.append(
            warning
        )

    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Serialização completa.
        """

        return {

            "response_id": self.response_id,

            "request_id": self.request_id,

            "created_at": self.created_at.isoformat(),

            "success": self.success,

            "content": self.content,

            "persona": self.persona,

            "provider": self.provider,

            "model": self.model,

            "stream": self.stream,

            "completed": self.completed,

            "finish_reason": self.finish_reason,

            "chunks": list(self.chunks),

            "tool_calls": list(self.tool_calls),

            "attachments": list(self.attachments),

            "latency": self.latency,

            "prompt_tokens": self.prompt_tokens,

            "completion_tokens": self.completion_tokens,

            "total_tokens": self.total_tokens,

            "error": self.error,

            "warnings": list(self.warnings),

            "metadata": dict(self.metadata)

        }

    # =====================================================
    # CONSTRUTORES
    # =====================================================

    @classmethod
    def failure(
        cls,
        error: str,
        provider: str = "unknown",
        model: str = "unknown"
    ) -> "AIResponse":
        """
        Cria uma resposta de erro.
        """

        return cls(

            success=False,

            content="",

            provider=provider,

            model=model,

            error=error,

            completed=True

        )

    @classmethod
    def success_response(
        cls,
        content: str,
        provider: str,
        model: str
    ) -> "AIResponse":
        """
        Cria uma resposta simples.
        """

        return cls(

            success=True,

            content=content,

            provider=provider,

            model=model

        )

    # =====================================================
    # DEBUG
    # =====================================================

    def __repr__(self) -> str:

        preview = self.content.replace(
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

            f"stream={self.stream}, "

            f"content='{preview}'"

            ")"

        )