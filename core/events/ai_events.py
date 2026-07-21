"""
=========================================
GENESIS CORE - AI COGNITION EVENTS

Arquivo: core/events/ai_events.py
Descrição: Eventos do ciclo de vida dos sistemas de inteligência artificial.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AIEvents:
    """
    Barramento de eventos da inteligência artificial.
    """

    # Requisições
    REQUEST: str = "ai.request"
    RESPONSE: str = "ai.response"
    STREAM_START: str = "ai.stream.start"
    STREAM_UPDATE: str = "ai.stream.update"
    STREAM_END: str = "ai.stream.end"

    # Modelos
    MODEL_LOADING: str = "ai.model.loading"
    MODEL_LOADED: str = "ai.model.loaded"
    MODEL_UNLOADED: str = "ai.model.unloaded"
    MODEL_ERROR: str = "ai.model.error"

    # Cognição
    THINK_STARTED: str = "ai.think.started"
    THINK_COMPLETED: str = "ai.think.completed"
    REASONING_STARTED: str = "ai.reasoning.started"
    REASONING_COMPLETED: str = "ai.reasoning.completed"

    # Memória
    MEMORY_REQUIRED: str = "ai.memory.required"
    MEMORY_FOUND: str = "ai.memory.found"
    MEMORY_STORED: str = "ai.memory.stored"

    # Aprendizado
    LEARNING_STARTED: str = "ai.learning.started"
    LEARNING_COMPLETED: str = "ai.learning.completed"
    REFLECTION_CREATED: str = "ai.reflection.created"

    # Agentes
    AGENT_SELECTED: str = "ai.agent.selected"
    PERSONALITY_CHANGED: str = "ai.personality.changed"

    # Erros
    ERROR: str = "ai.error"
    TIMEOUT: str = "ai.timeout"