"""
=========================================
GENESIS CORE

Arquivo:
core/managers/ai_manager.py

Descrição:
Gerenciador central da camada IA.

Responsável por:

- Controle de providers
- Contexto cognitivo
- Personas
- Roteamento
- Fallback
- Histórico
- Integração com Mind
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


from typing import Any



from core.ai.provider_registry import (
    ProviderRegistry
)


from core.ai.provider_factory import (
    ProviderFactory
)


from core.ai.ai_router import (
    AIRouter
)



from core.ai.models.ai_context import (
    AIContext
)


from core.ai.models.ai_request import (
    AIRequest
)


from core.ai.models.ai_response import (
    AIResponse
)



from core.ai.exceptions import (
    ProviderOfflineError
)





class AIManager:
    """
    Orquestrador principal da inteligência.

    O Genesis nunca acessa providers
    diretamente.

    Toda comunicação passa por aqui.
    """



    def __init__(self):


        self.registry = ProviderRegistry()


        self.router = AIRouter()



        self.active_provider = None



        self.mind = None



        self.initialized = False



        self.history = []



        # Núcleo cognitivo temporário
        self.context = AIContext(

            persona="jarvis"

        )






    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def initialize(
        self,
        provider_name: str = "mock"
    ) -> bool:
        """
        Inicializa camada IA.
        """


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
        """
        Desliga camada IA.
        """


        self.registry.clear()


        self.active_provider = None


        self.initialized = False






    # =====================================================
    # CONTEXTO
    # =====================================================


    def set_persona(
        self,
        persona: str
    ):
        """
        Troca personalidade ativa.
        """


        self.context.persona = (
            persona.lower().strip()
        )






    def remember(
        self,
        key: str,
        value: Any
    ):
        """
        Guarda memória temporária.
        """


        self.context.remember(

            key,

            value

        )






    def recall(
        self,
        key: str,
        default=None
    ):


        return self.context.recall(

            key,

            default

        )






    def clear_context(self):


        self.context.conversation.clear()


        self.context.variables.clear()






    # =====================================================
    # CONEXÕES
    # =====================================================


    def connect_mind(
        self,
        mind
    ):
        """
        Conecta Thought Engine.
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







    def get_provider(
        self
    ):


        return self.active_provider






    def providers(
        self
    ):


        return self.registry.names()







    # =====================================================
    # PROCESSAMENTO PRINCIPAL
    # =====================================================


    def ask(
        self,
        prompt: str
    ) -> AIResponse:
        """
        Entrada principal do Genesis.
        """



        self.context.add_message(

            "user",

            prompt

        )



        route = self.router.route(
            prompt
        )





        # =================================================
        # THOUGHT ENGINE
        # =================================================


        if route["route"] == "mind":


            if self.mind:


                response = self.mind.think(

                    prompt

                )


                self._save_context(

                    response

                )


                self._history(

                    prompt,

                    route,

                    response

                )


                return response







        # =================================================
        # PROVIDER IA
        # =================================================


        request = AIRequest(

            prompt=prompt,


            persona=self.context.persona,


            context=self.context.to_dict()

        )



        response = self.generate(
            request
        )



        self._save_context(

            response

        )



        self._history(

            prompt,

            route,

            response

        )



        return response







    # =====================================================
    # GERAÇÃO
    # =====================================================


    def generate(
        self,
        request: AIRequest,
        **kwargs: Any
    ) -> AIResponse:


        provider = self._resolve_provider()



        try:


            return provider.generate(

                request,

                **kwargs

            )



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
    ):


        providers = self.registry.all()



        for provider in providers:



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


            model="none",


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
    # CONTEXTO
    # =====================================================


    def _save_context(
        self,
        response
    ):


        self.context.add_message(

            "assistant",

            response.content

        )







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



            "persona":

                self.context.persona,



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


                "context": {


                    "persona":
                        self.context.persona,


                    "messages":
                        len(
                            self.context.conversation
                        )

                }


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

                len(self.history),



            "context": {


                "persona":

                    self.context.persona,


                "messages":

                    len(
                        self.context.conversation
                    ),


                "variables":

                    len(
                        self.context.variables
                    )


            }



        }