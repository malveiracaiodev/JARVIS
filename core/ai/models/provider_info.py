"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/provider_info.py

Descrição:
Modelo oficial de informações de um
Provider de Inteligência Artificial.

Representa as capacidades, limites,
estado e recursos de um Provider.

Utilizado por:

- ProviderRegistry
- ProviderManager
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
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class ProviderInfo:
    """
    Informações públicas de um Provider.

    Não representa estado operacional,
    apenas características e capacidades.
    """

    # =====================================================
    # IDENTIDADE
    # =====================================================

    provider_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    model: str = ""

    version: str = "Unknown"

    vendor: str = "Unknown"

    description: str = ""

    # =====================================================
    # ESTADO
    # =====================================================

    online: bool = False

    healthy: bool = False

    enabled: bool = True

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

    supports_images: bool = False

    supports_audio: bool = False

    supports_vision: bool = False

    supports_reasoning: bool = False

    supports_json_mode: bool = False

    # =====================================================
    # LIMITES
    # =====================================================

    max_tokens: int | None = None

    context_window: int | None = None

    max_output_tokens: int | None = None

    # =====================================================
    # LOCALIZAÇÃO
    # =====================================================

    local: bool = False

    endpoint: str | None = None

    # =====================================================
    # CUSTOS
    # =====================================================

    paid: bool = False

    cost_per_1k_prompt: float | None = None

    cost_per_1k_completion: float | None = None

    # =====================================================
    # METADADOS
    # =====================================================

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # PROPRIEDADES
    # =====================================================

    @property
    def available(self) -> bool:
        """
        Indica se o Provider está
        disponível para uso.
        """

        return self.enabled and self.online

    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Serialização completa.
        """

        return {

            "provider_id": self.provider_id,

            "name": self.name,

            "model": self.model,

            "version": self.version,

            "vendor": self.vendor,

            "description": self.description,

            "online": self.online,

            "healthy": self.healthy,

            "enabled": self.enabled,

            "registered_at": self.registered_at.isoformat(),

            "priority": self.priority,

            "fallback_enabled": self.fallback_enabled,

            "capabilities": {

                "chat": self.supports_chat,

                "stream": self.supports_stream,

                "embeddings": self.supports_embeddings,

                "tools": self.supports_tools,

                "images": self.supports_images,

                "audio": self.supports_audio,

                "vision": self.supports_vision,

                "reasoning": self.supports_reasoning,

                "json_mode": self.supports_json_mode

            },

            "limits": {

                "context_window": self.context_window,

                "max_tokens": self.max_tokens,

                "max_output_tokens": self.max_output_tokens

            },

            "location": {

                "local": self.local,

                "endpoint": self.endpoint

            },

            "pricing": {

                "paid": self.paid,

                "prompt_per_1k": self.cost_per_1k_prompt,

                "completion_per_1k": self.cost_per_1k_completion

            },

            "metadata": dict(self.metadata)

        }

    # =====================================================
    # DEBUG
    # =====================================================

    def __repr__(self) -> str:

        return (

            "ProviderInfo("

            f"name='{self.name}', "

            f"model='{self.model}', "

            f"vendor='{self.vendor}', "

            f"online={self.online}"

            ")"

        )