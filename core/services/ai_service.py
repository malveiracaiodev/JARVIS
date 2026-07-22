"""
=========================================
GENESIS CORE

Arquivo:
core/services/ai_service.py

Descrição:
Serviço de integração da camada IA.

Responsável por:

- Expor IA ao Genesis
- Gerenciar ciclo de vida
- Encaminhar requisições
- Integrar Kernel e Managers

A lógica cognitiva pertence ao AIManager.

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


from core.base.module import Module

from core.managers.ai_manager import AIManager

from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse



class AIService(Module):
    """
    Serviço oficial da camada IA.

    Atua como ponte entre o Genesis
    e o AIManager.
    """



    def __init__(self) -> None:


        super().__init__(
            name="ai_service"
        )


        self.ai_manager = AIManager()

        self.provider_name = "mock"



    # =====================================================
    # LOG
    # =====================================================


    def _log(
        self,
        message: str,
        level: str = "info"
    ):


        if hasattr(
            self,
            "logger"
        ):


            method = getattr(
                self.logger,
                level,
                None
            )


            if method:

                method(
                    message
                )

                return



        print(
            f"[AIService:{level.upper()}] {message}"
        )



    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def initialize(
        self,
        provider: str = "mock"
    ) -> bool:


        try:


            self.provider_name = provider



            self.ai_manager.initialize(
                provider
            )



            self._log(
                f"AIService online. Provider: {provider}"
            )



            return True



        except Exception as error:


            self._log(
                f"Falha ao iniciar IA: {error}",
                "error"
            )


            return False




    def shutdown(
        self
    ):


        try:


            self.ai_manager.shutdown()



        except Exception as error:


            self._log(
                f"Erro ao desligar IA: {error}",
                "error"
            )



        self._log(
            "AIService encerrado."
        )



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


        self.ai_manager.connect_mind(
            mind
        )


        self._log(
            "Mind conectado ao AIManager."
        )



    def register_provider(
        self,
        provider
    ):


        self.ai_manager.register_provider(
            provider
        )


    # =====================================================
    # REQUISIÇÕES
    # =====================================================


    def ask(
        self,
        prompt: str
    ) -> AIResponse:


        return self.ai_manager.ask(
            prompt
        )



    def generate(
        self,
        request: AIRequest,
        **kwargs: Any
    ) -> AIResponse:


        return self.ai_manager.generate(
            request,
            **kwargs
        )



    def chat(
        self,
        messages: list[dict],
        **kwargs
    ) -> AIResponse:


        return self.ai_manager.chat(
            messages,
            **kwargs
        )



    # =====================================================
    # CONTROLE
    # =====================================================


    def set_provider(
        self,
        provider_name: str
    ):


        self.ai_manager.set_provider(
            provider_name
        )


        self.provider_name = provider_name



    def providers(self):

        return self.ai_manager.providers()



    # =====================================================
    # STATUS
    # =====================================================


    def ai_status(
        self
    ) -> dict:


        return {

            "service":
                "AIService",

            "provider":
                self.provider_name,

            "manager":
                self.ai_manager.status()

        }