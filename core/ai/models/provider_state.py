"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/provider_state.py

Descrição:
Representa o estado operacional de um
Provider de Inteligência Artificial.

Responsável por:

- Estado operacional
- Métricas
- Tokens
- Diagnóstico
- Estatísticas
- Performance
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
from time import time
from typing import Any


@dataclass(slots=True)
class ProviderState:
    """
    Estado operacional de um Provider.
    """

    # =====================================================
    # ESTADO
    # =====================================================

    online: bool = False

    initialized: bool = False

    started_at: float | None = None

    last_boot_at: float | None = None

    last_request_at: float | None = None

    last_success_at: float | None = None

    last_failure_at: float | None = None

    restart_count: int = 0

    active_requests: int = 0

    # =====================================================
    # IDENTIDADE
    # =====================================================

    provider_name: str = ""

    provider_version: str = ""

    current_model: str = ""

    # =====================================================
    # MÉTRICAS
    # =====================================================

    requests: int = 0

    successes: int = 0

    failures: int = 0

    chat_requests: int = 0

    generation_requests: int = 0

    embedding_requests: int = 0

    streaming_requests: int = 0

    tool_requests: int = 0

    # =====================================================
    # PERFORMANCE
    # =====================================================

    total_latency: float = 0.0

    average_latency: float = 0.0

    last_latency: float = 0.0

    max_latency: float = 0.0

    min_latency: float = 0.0

    # =====================================================
    # TOKENS
    # =====================================================

    input_tokens: int = 0

    output_tokens: int = 0

    total_tokens: int = 0

    # =====================================================
    # DIAGNÓSTICO
    # =====================================================

    last_error: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # CICLO DE VIDA
    # =====================================================

    def initialize(
        self,
        provider_name: str | None = None,
        provider_version: str | None = None,
        model: str | None = None
    ) -> None:

        self.online = True
        self.initialized = True

        now = time()

        self.started_at = now
        self.last_boot_at = now

        self.restart_count += 1

        self.last_error = None

        if provider_name:
            self.provider_name = provider_name

        if provider_version:
            self.provider_version = provider_version

        if model:
            self.current_model = model

    def shutdown(self) -> None:

        self.online = False
        self.initialized = False
        self.active_requests = 0

    # =====================================================
    # CONTROLE
    # =====================================================

    def begin_request(self) -> None:

        self.active_requests += 1

        self.last_request_at = time()

    def finish_request(self) -> None:

        if self.active_requests > 0:
            self.active_requests -= 1

    # =====================================================
    # MÉTRICAS
    # =====================================================

    def register_request(
        self,
        latency: float = 0.0,
        success: bool = True,
        input_tokens: int = 0,
        output_tokens: int = 0
    ) -> None:

        self.requests += 1

        self.last_request_at = time()

        if success:

            self.successes += 1

            self.last_success_at = self.last_request_at

        else:

            self.failures += 1

            self.last_failure_at = self.last_request_at

        self.register_latency(latency)

        self.input_tokens += input_tokens

        self.output_tokens += output_tokens

        self.total_tokens += (
            input_tokens +
            output_tokens
        )

    def register_latency(
        self,
        latency: float
    ) -> None:

        self.last_latency = latency

        self.total_latency += latency

        if self.requests > 0:

            self.average_latency = (
                self.total_latency /
                self.requests
            )

        if latency > self.max_latency:

            self.max_latency = latency

        if self.min_latency == 0.0:

            self.min_latency = latency

        elif latency < self.min_latency:

            self.min_latency = latency

    def register_success(
        self,
        latency: float = 0.0,
        input_tokens: int = 0,
        output_tokens: int = 0
    ) -> None:

        self.register_request(

            latency=latency,

            success=True,

            input_tokens=input_tokens,

            output_tokens=output_tokens

        )

    def register_failure(
        self,
        error: str | None = None
    ) -> None:

        self.last_error = error

        self.register_request(
            success=False
        )

    # =====================================================
    # TIPOS
    # =====================================================

    def register_chat(self):

        self.chat_requests += 1

    def register_generation(self):

        self.generation_requests += 1

    def register_embedding(self):

        self.embedding_requests += 1

    def register_stream(self):

        self.streaming_requests += 1

    def register_tool(self):

        self.tool_requests += 1

    # =====================================================
    # RESET
    # =====================================================

    def reset(self) -> None:
        """
        Limpa apenas estatísticas,
        preservando identidade e estado.
        """

        self.requests = 0
        self.successes = 0
        self.failures = 0

        self.chat_requests = 0
        self.generation_requests = 0
        self.embedding_requests = 0
        self.streaming_requests = 0
        self.tool_requests = 0

        self.total_latency = 0.0
        self.average_latency = 0.0
        self.last_latency = 0.0
        self.max_latency = 0.0
        self.min_latency = 0.0

        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0

        self.last_error = None

    # =====================================================
    # CONSULTAS
    # =====================================================

    @property
    def uptime(self) -> float:

        if self.started_at is None:
            return 0.0

        return time() - self.started_at

    @property
    def success_rate(self) -> float:

        if self.requests == 0:
            return 0.0

        return (
            self.successes /
            self.requests
        ) * 100

    @property
    def failure_rate(self) -> float:

        if self.requests == 0:
            return 0.0

        return (
            self.failures /
            self.requests
        ) * 100

    @property
    def healthy(self) -> bool:

        return (
            self.online and
            self.initialized
        )

    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================

    def to_dict(self) -> dict[str, Any]:

        return {

            "online": self.online,

            "initialized": self.initialized,

            "healthy": self.healthy,

            "uptime": self.uptime,

            "provider": self.provider_name,

            "version": self.provider_version,

            "model": self.current_model,

            "restart_count": self.restart_count,

            "active_requests": self.active_requests,

            "requests": self.requests,

            "successes": self.successes,

            "failures": self.failures,

            "success_rate": self.success_rate,

            "failure_rate": self.failure_rate,

            "chat_requests": self.chat_requests,

            "generation_requests": self.generation_requests,

            "embedding_requests": self.embedding_requests,

            "streaming_requests": self.streaming_requests,

            "tool_requests": self.tool_requests,

            "average_latency": self.average_latency,

            "last_latency": self.last_latency,

            "max_latency": self.max_latency,

            "min_latency": self.min_latency,

            "input_tokens": self.input_tokens,

            "output_tokens": self.output_tokens,

            "total_tokens": self.total_tokens,

            "last_error": self.last_error,

            "metadata": dict(self.metadata)

        }