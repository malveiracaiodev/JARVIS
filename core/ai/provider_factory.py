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
- Descoberta de providers
- Configuração dinâmica

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from __future__ import annotations


from typing import (
    Type,
    Any
)


from core.interfaces.ai_provider_interface import (
    AIProviderInterface
)


from core.ai.exceptions import (
    InvalidProviderError
)



class ProviderFactory:
    """
    Fábrica oficial de Providers IA.

    O Genesis nunca instancia
    providers diretamente.

    Tudo passa por esta camada.
    """



    # =====================================================
    # REGISTRO INTERNO
    # =====================================================


    _providers: dict[
        str,
        Type[AIProviderInterface]
    ] = {}



    _aliases: dict[str, str] = {

        "local":
            "ollama",

        "llama":
            "ollama",

        "simulation":
            "mock",

        "test":
            "mock"

    }



    # =====================================================
    # REGISTRO PADRÃO
    # =====================================================


    @classmethod
    def bootstrap(cls):
        """
        Registra providers oficiais.

        Executado uma vez
        durante inicialização.
        """


        from core.ai.providers.mock_provider import (
            MockProvider
        )


        from core.ai.providers.ollama_provider import (
            OllamaProvider
        )


        cls.register(
            "mock",
            MockProvider
        )


        cls.register(
            "ollama",
            OllamaProvider
        )



    # =====================================================
    # CREATE
    # =====================================================


    @classmethod
    def create(
        cls,
        provider_name: str,
        initialize: bool = True,
        **kwargs: Any
    ) -> AIProviderInterface:
        """
        Cria um provider.

        Permite configuração dinâmica.
        """


        name = cls.resolve_alias(
            cls.normalize(provider_name)
        )



        if not cls.exists(name):

            cls.bootstrap()



        if not cls.exists(name):

            raise InvalidProviderError(

                f"Provider não encontrado: {provider_name}"

            )



        provider_class = cls._providers[name]



        provider = provider_class(
            **kwargs
        )



        cls.validate(
            provider
        )



        if initialize:


            success = provider.initialize()


            if not success:


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


        if not issubclass(
            provider_class,
            AIProviderInterface
        ):

            raise InvalidProviderError(

                "Provider inválido."

            )



        cls._providers[
            cls.normalize(name)
        ] = provider_class





    @classmethod
    def unregister(
        cls,
        name: str
    ) -> None:


        name = cls.resolve_alias(
            cls.normalize(name)
        )


        cls._providers.pop(
            name,
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


        return (

            cls.normalize(
                cls.resolve_alias(name)
            )

            in cls._providers

        )




    @classmethod
    def available(
        cls
    ) -> list[str]:


        if not cls._providers:

            cls.bootstrap()



        return list(
            cls._providers.keys()
        )




    @classmethod
    def info(
        cls
    ) -> dict:


        return {


            name:
            {

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
    ):


        return cls.create(
            "mock"
        )



    # =====================================================
    # VALIDAÇÃO
    # =====================================================


    @staticmethod
    def validate(
        provider
    ):


        if not isinstance(
            provider,
            AIProviderInterface
        ):

            raise InvalidProviderError(

                "Objeto não implementa AIProviderInterface"

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