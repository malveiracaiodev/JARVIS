"""
=========================================
GENESIS CORE

Arquivo:
core/ai/exceptions.py

Descrição:
Exceções específicas da camada IA.

Centraliza erros relacionados a:

- Providers
- Requests
- Contexto cognitivo
- Modelos
- Comunicação
- Geração
- Roteamento
- Memória

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""



# =====================================================
# BASE
# =====================================================


class AIError(Exception):
    """
    Erro raiz da camada de Inteligência Artificial.
    """

    pass





# =====================================================
# PROVIDERS
# =====================================================


class InvalidProviderError(AIError):
    """
    Provider inválido,
    inexistente ou incompatível.
    """

    pass




class ProviderOfflineError(AIError):
    """
    Provider registrado,
    porém indisponível.
    """

    pass




class ProviderInitializationError(AIError):
    """
    Falha durante boot
    ou preparação do provider.
    """

    pass




class ProviderConnectionError(AIError):
    """
    Falha de comunicação
    com provider externo.

    Exemplos:

    - Ollama desligado
    - API fora do ar
    - Timeout HTTP
    """

    pass




class ProviderTimeoutError(AIError):
    """
    Provider demorou além
    do limite permitido.
    """

    pass





# =====================================================
# GERAÇÃO
# =====================================================


class ProviderGenerationError(AIError):
    """
    Erro durante geração
    de resposta.
    """

    pass




class StreamingError(AIError):
    """
    Falha durante resposta
    em streaming.
    """

    pass




class EmbeddingError(AIError):
    """
    Falha na geração
    de embeddings.
    """

    pass





# =====================================================
# REQUEST
# =====================================================


class InvalidRequestError(AIError):
    """
    Requisição IA inválida.

    Exemplos:

    - Prompt vazio
    - Tipo incorreto
    - Dados ausentes
    """

    pass




class ContextError(AIError):
    """
    Erro relacionado ao
    AIContext.

    Exemplos:

    - Contexto corrompido
    - Memória inválida
    - Persona inexistente
    """

    pass





# =====================================================
# MODELOS
# =====================================================


class ModelError(AIError):
    """
    Erro relacionado ao modelo IA.
    """

    pass




class ModelNotFoundError(ModelError):
    """
    Modelo solicitado
    não encontrado.
    """

    pass




class ModelLoadError(ModelError):
    """
    Falha ao carregar modelo.
    """

    pass





# =====================================================
# ROTEAMENTO
# =====================================================


class AIRoutingError(AIError):
    """
    Falha no roteamento
    inteligente da IA.

    Exemplo:

    - Escolha de provider
    - Seleção de agente
    """

    pass





# =====================================================
# MEMÓRIA
# =====================================================


class MemoryContextError(AIError):
    """
    Erro ao recuperar
    ou salvar memória IA.
    """

    pass