"""
=========================================
GENESIS CORE

Arquivo:
core/managers/ai_manager.py

Descrição:
Gerenciador central da camada IA.

Responsável por:

- Controle de providers
- Roteamento cognitivo
- Seleção dinâmica de IA
- Fallback
- Histórico
- Integração com Mind
- Monitoramento

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations

from typing import Any


from core.ai.provider_registry import ProviderRegistry
from core.ai.provider_factory import ProviderFactory
from core.ai.ai_router import AIRouter

from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse

from core.ai.exceptions import ProviderOfflineError



class AIManager:
    """
    Orquestrador principal da inteligência.

    O Genesis nunca acessa providers
    diretamente.
    """


    def __init__(self):

        self.registry = ProviderRegistry()

        self.router = AIRouter()

        self.active_provider = None

        self.mind = None

        self.initialized = False

        self.history = []



    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def initialize(
        self,
        provider_name: str = "mock"
    ) -> bool:


        provider = ProviderFactory.create(
            provider_name
        )


        self.registry.register(
            provider
        )


        self.active_provider = provider


        self.initialized = True


        return True



    def shutdown(self):


        self.registry.clear()


        self.active_provider = None

        self.initialized = False



    # =====================================================
    # CONEXÕES
    # =====================================================


    def connect_mind(
        self,
        mind
    ):

        """
        Conecta a Thought Engine.
        """

        self.mind = mind



    # =====================================================
    # PROVIDERS
    # =====================================================


    def register_provider(
        self,
        provider
    ):


        self.registry.register(
            provider
        )



    def set_provider(
        self,
        provider_name: str
    ):


        provider = self.registry.get(
            provider_name
        )


        if not provider.available():

            raise ProviderOfflineError(
                f"Provider offline: {provider_name}"
            )


        self.active_provider = provider



    def get_provider(self):

        return self.active_provider



    def providers(self):

        return self.registry.names()



    # =====================================================
    # PROCESSAMENTO PRINCIPAL
    # =====================================================


    def ask(
        self,
        prompt: str
    ) -> AIResponse:


        route = self.router.route(
            prompt
        )


        # -----------------------------
        # COMANDO
        # -----------------------------

        if route["route"] == "mind":


            if self.mind:


                response = self.mind.think(
                    prompt
                )


                self._history(
                    prompt,
                    route,
                    response
                )


                return response



        # -----------------------------
        # CHAT NORMAL
        # -----------------------------


        request = AIRequest(
            prompt=prompt
        )


        response = self.generate(
            request
        )


        self._history(
            prompt,
            route,
            response
        )


        return response



    # =====================================================
    # GENERATE
    # =====================================================


    def generate(
        self,
        request: AIRequest,
        **kwargs: Any
    ) -> AIResponse:


        provider = self._resolve_provider()


        try:


            response = provider.generate(
                request,
                **kwargs
            )


            return response



        except Exception as error:


            return self._fallback(
                request,
                error
            )



    # =====================================================
    # CHAT
    # =====================================================


    def chat(
        self,
        messages: list[dict],
        **kwargs
    ):


        provider = self._resolve_provider()


        return provider.chat(
            messages,
            **kwargs
        )



    # =====================================================
    # FALLBACK
    # =====================================================


    def _fallback(
        self,
        request,
        error
    ) -> AIResponse:


        for provider in self.registry.all():


            if provider == self.active_provider:

                continue



            if provider.available():


                try:


                    return provider.generate(
                        request
                    )


                except Exception:

                    continue



        return AIResponse(

            success=False,

            content="",

            provider="Genesis",

            model="None",

            error=str(error)

        )



    # =====================================================
    # RESOLUÇÃO
    # =====================================================


    def _resolve_provider(self):


        if self.active_provider is None:


            raise ProviderOfflineError(
                "Nenhum provider ativo."
            )



        if not self.active_provider.available():


            raise ProviderOfflineError(
                "Provider offline."
            )


        return self.active_provider



    # =====================================================
    # HISTÓRICO
    # =====================================================


    def _history(
        self,
        prompt,
        route,
        response
    ):


        self.history.append({

            "prompt":
                prompt,

            "route":
                route,

            "provider":
                response.provider,

            "success":
                response.success,

            "response":
                response.content

        })



    def clear_history(self):

        self.history.clear()



    # =====================================================
    # STATUS
    # =====================================================


    def status(self):


        provider = self.active_provider



        if provider is None:


            return {

                "online": False,

                "provider": None,

                "providers":
                    self.providers(),

                "history":
                    len(self.history)

            }



        return {


            "online":
                provider.available(),


            "provider":
                provider.provider_name,


            "model":
                provider.model_name,


            "providers":
                self.providers(),


            "requests":
                provider.state.requests,


            "success":
                provider.state.successes,


            "failures":
                provider.state.failures,


            "history":
                len(self.history)

        }