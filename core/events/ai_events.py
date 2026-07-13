"""
=========================================
JARVIS CORE

Arquivo:
ai_events.py

Descrição:
Tópicos de eventos do ciclo de processamento dos modelos de linguagem.

Arquitetura:
Genesis Core

Mark:
III - Intelligence
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AIEvents:
    """
    Eventos do barramento de requisições e processamento cognitivo.
    """
    REQUEST: str = "ai.request"
    RESPONSE: str = "ai.response"
    MODEL_LOADED: str = "ai.model.loaded"
    MEMORY_REQUIRED: str = "ai.memory.required"