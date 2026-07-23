"""
=========================================
GENESIS CORE

Pacote:
core.ai.providers

Descrição:
Camada de implementação dos Providers
de Inteligência Artificial.

Responsável por conectar o Genesis Core
a motores cognitivos externos ou locais.

Providers são responsáveis apenas por:

- Comunicação com modelos IA
- Geração de respostas
- Chat
- Embeddings
- Métricas operacionais

Não controlam:

- Personas
- Memória permanente
- Pensamento
- Planejamento
- Identidade


Providers disponíveis:

MockProvider
    Provider simulado local para testes
    arquiteturais.


OllamaProvider
    Integração com modelos locais Ollama.


Providers futuros:

- GeminiProvider
- OpenAIProvider
- ClaudeProvider
- LocalLLMProvider


Arquitetura:

Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.ai.providers.mock_provider import (
    MockProvider
)


from core.ai.providers.ollama_provider import (
    OllamaProvider
)



__version__ = "5.0-Evolution"



__all__ = [

    "MockProvider",

    "OllamaProvider",

]