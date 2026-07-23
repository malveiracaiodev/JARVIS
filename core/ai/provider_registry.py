"""
=========================================
GENESIS CORE

Arquivo:
core/ai/provider_registry.py

Descrição:
Registro central de Providers IA.

Responsável por:

- Armazenamento de providers
- Descoberta
- Ciclo de vida
- Diagnóstico
- Seleção saudável

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from __future__ import annotations


from core.interfaces.ai_provider_interface import (
    AIProviderInterface
)


from core.ai.exceptions import (
    InvalidProviderError
)





class ProviderRegistry:
    """
    Registro oficial dos providers IA.

    Mantém os cérebros disponíveis
    para o Genesis.
    """



    def __init__(self):

        self._providers: dict[
            str,
            AIProviderInterface
        ] = {}





    # =====================================================
    # REGISTRO
    # =====================================================


    def register(
        self,
        provider: AIProviderInterface,
        initialize: bool = True
    ) -> None:
        """
        Adiciona provider ao Genesis.
        """


        self._validate(
            provider
        )


        name = self.normalize(
            provider.provider_name
        )



        if initialize:


            if not provider.available():

                provider.initialize()



        self._providers[name] = provider





    def unregister(
        self,
        provider_name: str
    ) -> None:


        name = self.normalize(
            provider_name
        )


        provider = self._providers.pop(
            name,
            None
        )


        if provider:


            try:

                provider.shutdown()

            except Exception:

                pass





    def clear(self):


        for provider in self._providers.values():


            try:

                provider.shutdown()

            except Exception:

                pass



        self._providers.clear()





    # =====================================================
    # BUSCA
    # =====================================================


    def get(
        self,
        provider_name: str
    ) -> AIProviderInterface:


        name = self.normalize(
            provider_name
        )



        if name not in self._providers:


            raise InvalidProviderError(

                f"Provider não encontrado: {provider_name}"

            )



        return self._providers[name]





    def get_available(
        self
    ) -> list[AIProviderInterface]:
        """
        Retorna somente providers online.
        """


        return [

            provider

            for provider

            in self._providers.values()

            if provider.available()

        ]





    def exists(
        self,
        provider_name: str
    ) -> bool:


        return (

            self.normalize(provider_name)

            in self._providers

        )





    def all(
        self
    ) -> list[AIProviderInterface]:


        return list(
            self._providers.values()
        )





    def names(
        self
    ) -> list[str]:


        return list(
            self._providers.keys()
        )





    # =====================================================
    # DIAGNÓSTICO
    # =====================================================


    def status(
        self
    ) -> dict:


        result = {}



        for name, provider in self._providers.items():


            result[name] = {


                "provider":

                    provider.provider_name,


                "model":

                    provider.model_name,


                "online":

                    provider.available(),


                "stats":

                    provider.stats()

            }



        return result





    @property
    def count(
        self
    ) -> int:


        return len(
            self._providers
        )





    # =====================================================
    # UTILIDADES
    # =====================================================


    @staticmethod
    def normalize(
        name: str
    ) -> str:


        return (

            name

            .strip()

            .lower()

            .replace(
                " ",
                "_"
            )

        )





    @staticmethod
    def _validate(
        provider
    ):


        required = [

            "provider_name",

            "model_name",

            "initialize",

            "shutdown",

            "available",

            "generate",

            "chat",

            "stats"

        ]



        for item in required:


            if not hasattr(
                provider,
                item
            ):


                raise InvalidProviderError(

                    f"Provider inválido. "
                    f"Ausente: {item}"

                )