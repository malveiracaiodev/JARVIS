"""
=========================================
GENESIS CORE

Arquivo:
core/managers/ai_manager.py

Descrição:
Núcleo de orquestração da inteligência.

Responsável por:

- Providers
- Persona ativa
- Contexto cognitivo
- Memória
- Mind
- Roteamento
- Histórico
- Fallback

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


from core.ai.models.ai_context import AIContext
from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse


from core.ai.exceptions import ProviderOfflineError




class AIManager:


    """
    Orquestrador central da inteligência Genesis.

    Não conhece implementações concretas
    de personas.

    Recebe serviços especializados.
    """



    def __init__(self):


        # Providers

        self.registry = ProviderRegistry()


        self.router = AIRouter()



        # Dependências externas

        self.persona_manager = None


        self.memory = None


        self.mind = None



        # Estado


        self.active_provider = None


        self.initialized = False


        self.history = []



        # Contexto inicial

        self.context = AIContext(

            persona="jarvis"

        )



    # ==================================================
    # CONEXÕES
    # ==================================================


    def connect_persona_manager(
        self,
        manager
    ):


        self.persona_manager = manager



        persona = (
            manager.get_active()
        )


        if persona:

            self.context.persona = (
                persona.name.lower()
            )



    def connect_memory(
        self,
        memory
    ):

        self.memory = memory



    def connect_mind(
        self,
        mind
    ):

        self.mind = mind