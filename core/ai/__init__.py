"""
=========================================
GENESIS CORE

Pacote:
core.ai

Descrição:
Camada de Inteligência Artificial do
Genesis Core.

Responsável por:

- Gerenciamento de providers
- Roteamento cognitivo
- Contexto de conversação
- Modelos IA
- Comunicação com LLMs
- Abstração de inteligência


Arquitetura:

Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


__version__ = "5.0-Evolution"



# =====================================================
# MODELOS
# =====================================================

from core.ai.models import (

    AIContext,

    AIMessage,

    AIRequest,

    AIResponse,

    ProviderInfo,

    ProviderState

)



# =====================================================
# BASE
# =====================================================

from core.ai.base import (
    BaseProvider
)



# =====================================================
# PROVIDERS
# =====================================================

from core.ai.providers import (

    MockProvider,

    OllamaProvider

)



# =====================================================
# FACTORY / REGISTRY
# =====================================================

from core.ai.provider_factory import (
    ProviderFactory
)


from core.ai.provider_registry import (
    ProviderRegistry
)



# =====================================================
# ROUTER
# =====================================================

from core.ai.ai_router import (
    AIRouter
)



# =====================================================
# EXCEPTIONS
# =====================================================

from core.ai.exceptions import (

    AIError,

    InvalidProviderError,

    ProviderOfflineError,

    ProviderInitializationError,

    ProviderGenerationError,

    InvalidRequestError

)



__all__ = [

    # Version

    "__version__",


    # Models

    "AIContext",

    "AIMessage",

    "AIRequest",

    "AIResponse",

    "ProviderInfo",

    "ProviderState",


    # Base

    "BaseProvider",


    # Providers

    "MockProvider",

    "OllamaProvider",


    # Infrastructure

    "ProviderFactory",

    "ProviderRegistry",

    "AIRouter",


    # Exceptions

    "AIError",

    "InvalidProviderError",

    "ProviderOfflineError",

    "ProviderInitializationError",

    "ProviderGenerationError",

    "InvalidRequestError",

]