"""
=========================================
GENESIS CORE

Arquivo:
core/services/ai_service.py

Descrição:
Serviço oficial da inteligência Genesis.

Responsável por:

- Expor camada IA ao Kernel
- Controlar ciclo de vida
- Integrar Persona
- Integrar Memória
- Integrar Mind
- Encaminhar requisições

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations

from typing import Any

from core.base.module import Module

from core.managers.ai_manager import AIManager

from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse



class AIService(Module):


    def __init__(self):

        super().__init__(
            name="ai_service"
        )


        self.ai_manager = AIManager()


        self.provider_name = "mock"


        self.persona_manager = None
        self.memory = None
        self.mind = None



    # ==================================================
    # LOG
    # ==================================================

    def _log(
        self,
        message,
        level="info"
    ):

        print(
            f"[AIService:{level.upper()}] {message}"
        )



    # ==================================================
    # INICIALIZAÇÃO
    # ==================================================

    def initialize(
        self,
        provider="mock"
    ):


        try:


            self.provider_name = provider


            self.ai_manager.initialize(
                provider
            )


            self._connect_dependencies()


            self._log(
                f"AIService ONLINE - Provider: {provider}"
            )


            return True



        except Exception as error:


            self._log(
                str(error),
                "error"
            )


            return False



    # ==================================================
    # DEPENDÊNCIAS
    # ==================================================

    def connect_persona_manager(
        self,
        manager
    ):


        self.persona_manager = manager


        self.ai_manager.connect_persona_manager(
            manager
        )



    def connect_memory(
        self,
        memory
    ):


        self.memory = memory


        self.ai_manager.connect_memory(
            memory
        )



    def connect_mind(
        self,
        mind
    ):


        self.mind = mind


        self.ai_manager.connect_mind(
            mind
        )



    def _connect_dependencies(self):


        if self.persona_manager:

            self.ai_manager.connect_persona_manager(
                self.persona_manager
            )


        if self.memory:

            self.ai_manager.connect_memory(
                self.memory
            )


        if self.mind:

            self.ai_manager.connect_mind(
                self.mind
            )



    # ==================================================
    # IA
    # ==================================================

    def ask(
        self,
        prompt:str
    ) -> AIResponse:


        return self.ai_manager.ask(
            prompt
        )



    def generate(
        self,
        request:AIRequest,
        **kwargs:Any
    ):


        return self.ai_manager.generate(
            request,
            **kwargs
        )



    def chat(
        self,
        messages:list[dict],
        **kwargs
    ):


        return self.ai_manager.chat(
            messages,
            **kwargs
        )



    # ==================================================
    # PROVIDERS
    # ==================================================

    def set_provider(
        self,
        provider_name
    ):


        self.ai_manager.set_provider(
            provider_name
        )


        self.provider_name = provider_name



    def providers(self):

        return self.ai_manager.providers()



    # ==================================================
    # STATUS
    # ==================================================

    def status(self):


        return {


            "service":
                "AIService",


            "provider":
                self.provider_name,


            "ai":
                self.ai_manager.status()


        }



    # ==================================================
    # DESLIGAMENTO
    # ==================================================

    def shutdown(self):


        self.ai_manager.shutdown()


        self._log(
            "AIService OFFLINE"
        )