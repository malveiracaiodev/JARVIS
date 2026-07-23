"""
=========================================
GENESIS CORE

Arquivo:
core/ai/base/base_provider.py

Descrição:
Classe base oficial para Providers IA.

Responsável por:

- Identidade do provider
- Estado operacional
- Métricas
- Configuração
- Hooks
- Validação
- Integração AIContext

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


from core.interfaces.ai_provider_interface import (
    AIProviderInterface
)


from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse
from core.ai.models.provider_info import ProviderInfo
from core.ai.models.provider_state import ProviderState



class BaseProvider(
    AIProviderInterface,
    ABC
):
    """
    Implementação base compartilhada
    entre todos os Providers.
    """


    def __init__(
        self,
        provider_name: str,
        model_name: str,
        version: str = "1.0"
    ):


        self._provider_name = provider_name

        self._model_name = model_name

        self._version = version



        self._state = ProviderState(

            provider_name=provider_name,

            provider_version=version,

            current_model=model_name

        )



        # Configuração padrão

        self.timeout = 60

        self.max_tokens = None

        self.temperature = 0.7



    # =====================================================
    # IDENTIDADE
    # =====================================================


    @property
    def provider_name(self) -> str:

        return self._provider_name



    @property
    def model_name(self) -> str:

        return self._model_name



    @property
    def version(self) -> str:

        return self._version



    @property
    def state(self) -> ProviderState:

        return self._state



    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def initialize(self) -> bool:


        self.state.initialize(

            provider_name=self.provider_name,

            provider_version=self.version,

            model=self.model_name

        )


        return True



    def shutdown(self) -> None:

        self.state.shutdown()



    def available(self) -> bool:

        return self.state.online



    # =====================================================
    # CONFIGURAÇÃO
    # =====================================================


    def configure(
        self,
        **kwargs: Any
    ) -> None:


        for key, value in kwargs.items():


            if hasattr(
                self,
                key
            ):

                setattr(
                    self,
                    key,
                    value
                )



    # =====================================================
    # HOOKS
    # =====================================================


    def before_generate(
        self,
        request: AIRequest
    ) -> AIRequest:

        return request



    def after_generate(
        self,
        response: AIResponse
    ) -> AIResponse:

        return response



    # =====================================================
    # VALIDAÇÃO
    # =====================================================


    def validate_request(
        self,
        request: AIRequest
    ) -> None:


        if request is None:

            raise ValueError(
                "AIRequest inexistente."
            )


        if not request.prompt:

            raise ValueError(
                "Prompt vazio."
            )



    # =====================================================
    # MÉTRICAS
    # =====================================================


    def start_request(self):

        self.state.begin_request()



    def finish_request(self):

        self.state.finish_request()



    def register_success(
        self,
        latency: float = 0.0,
        input_tokens: int = 0,
        output_tokens: int = 0
    ):


        self.state.register_success(

            latency=latency,

            input_tokens=input_tokens,

            output_tokens=output_tokens

        )



    def register_failure(
        self,
        error: str | None = None
    ):


        self.state.register_failure(
            error
        )



    def reset_stats(self) -> dict:

        """
        Limpa métricas mantendo
        estado do provider.
        """


        self.state.reset()


        return self.state.to_dict()



    # =====================================================
    # INFORMAÇÕES
    # =====================================================


    def info(self) -> ProviderInfo:


        return ProviderInfo(

            name=self.provider_name,

            model=self.model_name,

            version=self.version,

            online=self.available(),

            healthy=self.state.healthy,

            metadata={

                "state":

                    self.state.to_dict()

            }

        )



    def stats(self) -> dict:


        return self.state.to_dict()



    def health(self) -> dict:


        return {


            "healthy":
                self.state.healthy,


            "online":
                self.state.online,


            "initialized":
                self.state.initialized,


            "uptime":
                self.state.uptime,


            "active_requests":
                self.state.active_requests

        }



    # =====================================================
    # IA
    # =====================================================


    @abstractmethod
    def generate(
        self,
        request: AIRequest,
        **kwargs: Any
    ) -> AIResponse:

        pass



    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        **kwargs
    ) -> AIResponse:

        pass



    @abstractmethod
    def embeddings(
        self,
        text: str
    ) -> Any:

        pass



    # =====================================================
    # DEBUG
    # =====================================================


    def __repr__(self):

        return (

            f"{self.__class__.__name__}("

            f"provider='{self.provider_name}', "

            f"model='{self.model_name}', "

            f"online={self.available()}"

            ")"

        )