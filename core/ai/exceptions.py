"""
=========================================
GENESIS CORE

Arquivo:
core/ai/exceptions.py

Descrição:
Exceções específicas da camada IA.

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""


class AIError(Exception):
    """
    Erro base da camada IA.
    """
    pass



class InvalidProviderError(AIError):
    """
    Provider inválido ou inexistente.
    """
    pass



class ProviderOfflineError(AIError):
    """
    Provider registrado mas offline.
    """
    pass



class ProviderInitializationError(AIError):
    """
    Falha durante inicialização.
    """
    pass



class ProviderGenerationError(AIError):
    """
    Erro durante geração de resposta.
    """
    pass



class InvalidRequestError(AIError):
    """
    Requisição IA inválida.
    """
    pass