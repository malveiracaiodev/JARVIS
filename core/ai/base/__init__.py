"""
=========================================
GENESIS CORE

Pacote:
core.ai.base

Descrição:
Classes abstratas e implementações base
da camada de Inteligência Artificial.

Responsável por fornecer:

- Contratos compartilhados
- Ciclo de vida dos Providers
- Métricas
- Configuração
- Hooks de processamento

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from .base_provider import BaseProvider


__all__ = [
    "BaseProvider",
]