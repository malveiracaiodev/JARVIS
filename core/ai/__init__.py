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
- Modelos de comunicação IA
- Interfaces com LLMs
- Abstração de inteligência

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.ai.provider_factory import ProviderFactory
from core.ai.provider_registry import ProviderRegistry


__all__ = [
    "ProviderFactory",
    "ProviderRegistry",
]