"""
=========================================
GENESIS CORE

Pacote:
core.ai.models

Descrição:
Modelos de dados da camada de
Inteligência Artificial.

Responsável por estruturas compartilhadas
entre:

- AIService
- AIManager
- ProviderFactory
- Providers
- Thought Engine
- Memory System
- Event Bus

Inclui:

- Contexto cognitivo temporário
- Mensagens
- Requisições
- Respostas
- Estado de Providers

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.ai.models.ai_context import AIContext

from core.ai.models.ai_message import AIMessage

from core.ai.models.ai_request import AIRequest

from core.ai.models.ai_response import AIResponse


from core.ai.models.provider_info import ProviderInfo

from core.ai.models.provider_state import ProviderState



__all__ = [

    "AIContext",

    "AIMessage",

    "AIRequest",

    "AIResponse",

    "ProviderInfo",

    "ProviderState",

]