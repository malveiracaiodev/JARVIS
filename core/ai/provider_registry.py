"""
=========================================
GENESIS CORE

Arquivo:
core/ai/provider_registry.py

Descrição:
Registro central de Providers de IA.

Responsável por:

- Armazenar providers ativos
- Localizar providers
- Controlar ciclo de vida
- Diagnóstico da camada IA

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
    Registro central dos Providers IA.

    Mantém providers carregados
    pelo Genesis Core.
    """



    def __init__(self) -> None:


        self._providers: dict[
            str,
            AIProviderInterface
        ] = {}



    # =====================================================
    # REGISTRO
    # =====================================================


    def register(
        self,
        provider: AIProviderInterface
    ) -> None:
        """
        Registra um provider.
        """


        self._validate(
            provider
        )


        name = self.normalize(
            provider.provider_name
        )


        self._providers[
            name
        ] = provider



    def unregister(
        self,
        provider_name: str
    ) -> None:
        """
        Remove provider e encerra.
        """


        name = self.normalize(
            provider_name
        )


        provider = self._providers.get(
            name
        )


        if provider:


            try:

                provider.shutdown()

            except Exception:

                pass



            del self._providers[
                name
            ]



    def clear(self) -> None:
        """
        Remove todos os providers.
        """


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
        """
        Busca provider.
        """


        name = self.normalize(
            provider_name
        )


        if name not in self._providers:


            raise InvalidProviderError(
                f"Provider não encontrado: {provider_name}"
            )


        return self._providers[name]



    def exists(
        self,
        provider_name: str
    ) -> bool:
        """
        Verifica existência.
        """


        return (
            self.normalize(provider_name)
            in self._providers
        )



    def all(
        self
    ) -> list[AIProviderInterface]:
        """
        Retorna todos.
        """


        return list(
            self._providers.values()
        )



    def names(
        self
    ) -> list[str]:
        """
        Retorna nomes registrados.
        """


        return list(
            self._providers.keys()
        )



    # =====================================================
    # DIAGNÓSTICO
    # =====================================================


    def status(
        self
    ) -> dict:
        """
        Retorna diagnóstico completo.
        """


        result = {}


        for name, provider in self._providers.items():


            result[name] = {


                "provider":
                    provider.provider_name,


                "model":
                    provider.model_name,


                "online":
                    provider.available(),


                "state":
                    provider.state.to_dict()

            }


        return result



    @property
    def count(
        self
    ) -> int:
        """
        Quantidade de providers.
        """


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
        """
        Padroniza nomes.
        """


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
    ) -> None:
        """
        Valida provider.
        """


        if not isinstance(
            provider,
            AIProviderInterface
        ):

            raise InvalidProviderError(
                "Objeto não é um AIProvider válido."
            )