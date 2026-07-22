"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/provider_info.py

Descrição:
Representa informações públicas de um
provedor de Inteligência Artificial.

Utilizado por:

- ProviderRegistry
- AIManager
- Diagnostics
- Dashboard
- Monitoramento

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
class ProviderInfo:
    """
    Informações de um provider registrado.
    """


    # =====================================================
    # IDENTIDADE
    # =====================================================

    id: str = field(
        default_factory=lambda: str(uuid4())
    )


    name: str = ""


    model: str = ""


    version: str = "Unknown"



    # =====================================================
    # ESTADO
    # =====================================================

    online: bool = False


    healthy: bool = False


    registered_at: datetime = field(
        default_factory=datetime.now
    )



    # =====================================================
    # PRIORIDADE
    # =====================================================

    priority: int = 0


    fallback_enabled: bool = True



    # =====================================================
    # CAPACIDADES
    # =====================================================

    supports_chat: bool = True


    supports_stream: bool = False


    supports_embeddings: bool = False


    supports_tools: bool = False



    # =====================================================
    # LIMITES
    # =====================================================

    max_tokens: int | None = None


    context_window: int | None = None



    # =====================================================
    # METADADOS
    # =====================================================

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Converte informações para diagnóstico.
        """


        return {

            "id":
                self.id,

            "name":
                self.name,

            "model":
                self.model,

            "version":
                self.version,

            "online":
                self.online,

            "healthy":
                self.healthy,

            "priority":
                self.priority,

            "fallback_enabled":
                self.fallback_enabled,

            "capabilities": {

                "chat":
                    self.supports_chat,

                "stream":
                    self.supports_stream,

                "embeddings":
                    self.supports_embeddings,

                "tools":
                    self.supports_tools

            },

            "limits": {

                "max_tokens":
                    self.max_tokens,

                "context_window":
                    self.context_window

            },

            "metadata":
                dict(self.metadata)

        }



    def __repr__(self) -> str:

        return (

            "ProviderInfo("

            f"name='{self.name}', "

            f"model='{self.model}', "

            f"online={self.online}"

            ")"

        )