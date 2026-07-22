"""
=========================================
GENESIS CORE

Arquivo:
core/ai/base/base_provider.py

Descrição:
Classe base para todos os Providers IA.

Arquitetura:
Genesis Core

Mark:
V - Evolution
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



        self.timeout = 60

        self.max_tokens = None

        self.temperature = 0.7





    # =====================================================
    # IDENTIDADE
    # =====================================================


    @property
    def provider_name(self):

        return self._provider_name



    @property
    def model_name(self):

        return self._model_name



    @property
    def version(self):

        return self._version



    @property
    def state(self):

        return self._state





    # =====================================================
    # CICLO
    # =====================================================


    def initialize(self):


        self.state.initialize(

            provider_name=self.provider_name,

            provider_version=self.version,

            model=self.model_name

        )


        return True





    def shutdown(self):

        self.state.shutdown()





    def available(self):

        return self.state.online





    # =====================================================
    # CONFIG
    # =====================================================


    def configure(
        self,
        **kwargs
    ):


        for key, value in kwargs.items():


            if hasattr(self, key):

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
        request
    ):

        return request




    def after_generate(
        self,
        response
    ):

        return response





    # =====================================================
    # VALIDAÇÃO
    # =====================================================


    def validate_request(
        self,
        request
    ):


        if request is None:

            raise ValueError(
                "AIRequest inválido."
            )



        if not request.prompt:

            raise ValueError(
                "Prompt vazio."
            )





    # =====================================================
    # MÉTRICAS
    # =====================================================


    def register_success(
        self,
        latency=0.0,
        input_tokens=0,
        output_tokens=0
    ):


        self.state.register_success(

            latency,

            input_tokens,

            output_tokens

        )





    def register_failure(
        self,
        error=None
    ):


        self.state.register_failure(
            error
        )





    def reset_stats(self):

        self.state.reset()





    # =====================================================
    # STATUS
    # =====================================================


    def info(self):


        return ProviderInfo(

            name=self.provider_name,

            model=self.model_name,

            version=self.version,

            online=self.available()

        )





    def stats(self):

        return self.state.to_dict()





    def health(self):


        return {

            "healthy":
                self.state.healthy,


            "online":
                self.state.online,


            "initialized":
                self.state.initialized,


            "uptime":
                self.state.uptime

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
    ):
        pass





    # =====================================================
    # DEBUG
    # =====================================================


    def __repr__(self):

        return (

            f"{self.__class__.__name__}("

            f"provider='{self.provider_name}', "

            f"model='{self.model_name}', "

            f"online={self.available()})"

        )