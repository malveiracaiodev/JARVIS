"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/provider_state.py

Descrição:
Representa o estado interno de um
Provider de Inteligência Artificial.

Responsável por:
- Estado operacional
- Métricas
- Tokens
- Diagnóstico
- Estatísticas

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations


from dataclasses import dataclass, field
from time import time



@dataclass(slots=True)
class ProviderState:
    """
    Estado interno de um Provider IA.
    """


    # =====================================================
    # ESTADO
    # =====================================================

    online: bool = False

    initialized: bool = False

    started_at: float | None = None

    last_request_at: float | None = None

    last_boot_at: float | None = None

    restart_count: int = 0



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



    total_latency: float = 0.0

    average_latency: float = 0.0

    last_latency: float = 0.0



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

    metadata: dict = field(
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


        self.started_at = time()

        self.last_boot_at = (
            self.started_at
        )


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



        if success:

            self.successes += 1

        else:

            self.failures += 1



        self.last_request_at = time()


        self.last_latency = latency


        self.total_latency += latency



        self.average_latency = (

            self.total_latency /

            self.requests

        )



        self.input_tokens += input_tokens

        self.output_tokens += output_tokens


        self.total_tokens += (

            input_tokens +

            output_tokens

        )





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





    # =====================================================
    # RESET
    # =====================================================


    def reset(self) -> None:
        """
        Limpa apenas estatísticas.
        Mantém identidade e estado.
        """


        self.requests = 0

        self.successes = 0

        self.failures = 0


        self.chat_requests = 0

        self.generation_requests = 0

        self.embedding_requests = 0


        self.total_latency = 0.0

        self.average_latency = 0.0

        self.last_latency = 0.0


        self.input_tokens = 0

        self.output_tokens = 0

        self.total_tokens = 0


        self.last_error = None





    # =====================================================
    # CONSULTAS
    # =====================================================


    @property
    def uptime(self):

        if self.started_at is None:

            return 0.0


        return time() - self.started_at




    @property
    def success_rate(self):

        if self.requests == 0:

            return 0.0


        return (

            self.successes /

            self.requests

        ) * 100




    @property
    def failure_rate(self):

        if self.requests == 0:

            return 0.0


        return (

            self.failures /

            self.requests

        ) * 100





    @property
    def healthy(self):

        return (

            self.online and

            self.initialized

        )





    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================


    def to_dict(self):

        return {


            "online":
                self.online,


            "initialized":
                self.initialized,


            "healthy":
                self.healthy,


            "uptime":
                self.uptime,


            "provider":
                self.provider_name,


            "version":
                self.provider_version,


            "model":
                self.current_model,


            "requests":
                self.requests,


            "successes":
                self.successes,


            "failures":
                self.failures,


            "success_rate":
                self.success_rate,


            "failure_rate":
                self.failure_rate,


            "chat_requests":
                self.chat_requests,


            "generation_requests":
                self.generation_requests,


            "embedding_requests":
                self.embedding_requests,


            "average_latency":
                self.average_latency,


            "last_latency":
                self.last_latency,


            "input_tokens":
                self.input_tokens,


            "output_tokens":
                self.output_tokens,


            "total_tokens":
                self.total_tokens,


            "last_error":
                self.last_error,


            "metadata":
                dict(self.metadata)

        }