"""
=========================================
GENESIS CORE

Arquivo:
core/ai/provider_factory.py

Descrição:
Fábrica central responsável pela criação
e gerenciamento de Providers de IA.

Responsável por:

- Registrar providers
- Criar instâncias
- Resolver aliases
- Validar implementações
- Descobrir providers disponíveis

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations

from typing import Type


from core.interfaces.ai_provider_interface import (
    AIProviderInterface
)

from core.ai.exceptions import (
    InvalidProviderError
)


from core.ai.providers.mock_provider import (
    MockProvider
)

from core.ai.providers.ollama_provider import (
    OllamaProvider
)



class ProviderFactory:
    """
    Fábrica oficial de Providers IA.

    O Genesis nunca cria providers
    diretamente.

    Tudo passa por aqui.
    """



    _providers: dict[
        str,
        Type[AIProviderInterface]
    ] = {


        "mock":
            MockProvider,


        "ollama":
            OllamaProvider,


    }



    _aliases = {


        "local":
            "ollama",


        "simulation":
            "mock",


        "test":
            "mock",


        "llama":
            "ollama"


    }



    # =====================================================
    # CREATE
    # =====================================================


    @classmethod
    def create(
        cls,
        provider_name: str
    ) -> AIProviderInterface:
        """
        Cria e inicializa um provider.
        """


        name = cls.resolve_alias(
            cls.normalize(provider_name)
        )


        if not cls.exists(name):

            raise InvalidProviderError(

                f"Provider não suportado: {provider_name}"

            )



        provider_class = cls._providers[name]



        provider = provider_class()



        if not isinstance(
            provider,
            AIProviderInterface
        ):

            raise InvalidProviderError(

                f"{name} não implementa AIProviderInterface"

            )



        if not provider.initialize():

            raise InvalidProviderError(

                f"Falha ao inicializar provider: {name}"

            )



        return provider



    # =====================================================
    # REGISTRO
    # =====================================================


    @classmethod
    def register(
        cls,
        name: str,
        provider_class: Type[AIProviderInterface]
    ) -> None:
        """
        Registra novo provider.
        """


        normalized = cls.normalize(
            name
        )


        if not issubclass(
            provider_class,
            AIProviderInterface
        ):

            raise InvalidProviderError(

                "Classe provider inválida."

            )


        cls._providers[
            normalized
        ] = provider_class



    @classmethod
    def unregister(
        cls,
        name: str
    ) -> None:
        """
        Remove provider.
        """


        normalized = cls.resolve_alias(

            cls.normalize(name)

        )


        cls._providers.pop(
            normalized,
            None
        )



    # =====================================================
    # CONSULTA
    # =====================================================


    @classmethod
    def exists(
        cls,
        name: str
    ) -> bool:
        """
        Verifica provider existente.
        """


        normalized = cls.resolve_alias(

            cls.normalize(name)

        )


        return normalized in cls._providers



    @classmethod
    def available(
        cls
    ) -> list[str]:
        """
        Lista providers registrados.
        """


        return list(
            cls._providers.keys()
        )



    @classmethod
    def info(
        cls
    ) -> dict:
        """
        Informações dos providers.
        """


        return {

            name: {

                "class":
                    provider.__name__

            }

            for name, provider

            in cls._providers.items()

        }



    # =====================================================
    # DEFAULT
    # =====================================================


    @classmethod
    def create_default(
        cls
    ) -> AIProviderInterface:
        """
        Provider padrão.
        """


        return cls.create(
            "mock"
        )



    # =====================================================
    # UTIL
    # =====================================================


    @staticmethod
    def normalize(
        name: str
    ) -> str:


        return (

            name
            .strip()
            .lower()

        )



    @classmethod
    def resolve_alias(
        cls,
        name: str
    ) -> str:


        return cls._aliases.get(

            name,

            name

        )