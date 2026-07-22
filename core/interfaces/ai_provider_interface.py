"""
=========================================
GENESIS CORE

Arquivo:
core/interfaces/ai_provider_interface.py

Descrição:
Contrato oficial para provedores de IA.

Todo provider integrado ao Genesis Core
deve implementar esta interface.

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


from core.ai.models.ai_request import AIRequest
from core.ai.models.ai_response import AIResponse
from core.ai.models.provider_info import ProviderInfo



class AIProviderInterface(ABC):
    """
    Interface base dos Providers de IA.

    O Genesis Core trabalha apenas
    com este contrato.

    Implementações possíveis:

    - MockProvider
    - OllamaProvider
    - GeminiProvider
    - OpenAIProvider
    - ClaudeProvider
    - LocalLLMProvider
    """



    # =====================================================
    # IDENTIDADE
    # =====================================================

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Nome identificador do provider.
        """
        pass



    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Modelo ativo.
        """
        pass



    # =====================================================
    # CICLO DE VIDA
    # =====================================================

    @abstractmethod
    def initialize(self) -> bool:
        """
        Inicializa conexão,
        modelo ou recursos necessários.
        """
        pass



    @abstractmethod
    def shutdown(self) -> None:
        """
        Libera recursos.
        """
        pass



    @abstractmethod
    def available(self) -> bool:
        """
        Retorna se o provider
        está pronto para uso.
        """
        pass



    # =====================================================
    # GERAÇÃO
    # =====================================================

    @abstractmethod
    def generate(
        self,
        request: AIRequest,
        **kwargs: Any
    ) -> AIResponse:
        """
        Geração simples de resposta.
        """
        pass



    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        **kwargs: Any
    ) -> AIResponse:
        """
        Conversação com histórico.
        """
        pass



    # =====================================================
    # EMBEDDINGS
    # =====================================================

    @abstractmethod
    def embeddings(
        self,
        text: str
    ) -> Any:
        """
        Geração de embeddings.

        Providers sem suporte podem
        lançar NotImplementedError.
        """
        pass



    # =====================================================
    # INFORMAÇÕES
    # =====================================================

    @abstractmethod
    def info(self) -> ProviderInfo:
        """
        Informações do provider.
        """
        pass



    @abstractmethod
    def stats(self) -> dict:
        """
        Estatísticas operacionais.
        """
        pass