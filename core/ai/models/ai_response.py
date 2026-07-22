"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_response.py

Descrição:
Representa uma resposta padronizada de
qualquer provedor de Inteligência Artificial.

Responsável por transportar:

- Conteúdo gerado
- Informações do provider
- Métricas
- Tokens
- Diagnóstico
- Metadados cognitivos

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



@dataclass(slots=True)
class AIResponse:
    """
    Estrutura padrão de resposta dos providers.
    """


    # =====================================================
    # IDENTIDADE
    # =====================================================

    response_id: str = field(
        default_factory=lambda: str(uuid4())
    )


    created_at: datetime = field(
        default_factory=datetime.now
    )


    request_id: str | None = None



    # =====================================================
    # RESULTADO
    # =====================================================

    success: bool = True


    content: str = ""



    # =====================================================
    # PROVIDER
    # =====================================================

    provider: str = ""


    model: str = ""


    persona: str | None = None



    # =====================================================
    # FINALIZAÇÃO
    # =====================================================

    finish_reason: str = "completed"



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



    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # =====================================================
    # ESTADOS
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
        Verifica resposta vazia.
        """

        return not bool(
            self.content.strip()
        )



    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Converte resposta para logs,
        memória ou eventos.
        """


        return {

            "response_id":
                self.response_id,

            "request_id":
                self.request_id,

            "success":
                self.success,

            "content":
                self.content,

            "provider":
                self.provider,

            "model":
                self.model,

            "persona":
                self.persona,

            "finish_reason":
                self.finish_reason,

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
        model: str = "unknown"
    ) -> "AIResponse":
        """
        Cria resposta de erro padronizada.
        """


        return cls(

            success=False,

            content="",

            provider=provider,

            model=model,

            error=error

        )



    def __repr__(self) -> str:

        return (

            "AIResponse("

            f"provider='{self.provider}', "

            f"model='{self.model}', "

            f"success={self.success}"

            ")"

        )