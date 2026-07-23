"""
=========================================
GENESIS CORE

Arquivo:
core/events/ai_events.py

Descrição:
Barramento oficial de eventos da camada
de Inteligência Artificial.

Centraliza todos os eventos utilizados
pela infraestrutura de IA do Genesis,
incluindo:

- Requisições
- Respostas
- Streaming
- Providers
- Modelos
- Cognição
- Memória
- Ferramentas
- Agentes
- Aprendizado
- Erros

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AIEvents:
    """
    Eventos oficiais da camada de IA.

    Todos os módulos relacionados à
    inteligência artificial devem utilizar
    estes identificadores.

    Exemplo:

        event_bus.emit(
            AIEvents.REQUEST_STARTED,
            request
        )
    """

    # =====================================================
    # REQUISIÇÕES
    # =====================================================

    REQUEST_STARTED: str = "ai.request.started"

    REQUEST_COMPLETED: str = "ai.request.completed"

    REQUEST_CANCELLED: str = "ai.request.cancelled"

    REQUEST_FAILED: str = "ai.request.failed"

    # Compatibilidade
    REQUEST: str = "ai.request"
    RESPONSE: str = "ai.response"

    # =====================================================
    # RESPOSTAS
    # =====================================================

    RESPONSE_STARTED: str = "ai.response.started"

    RESPONSE_COMPLETED: str = "ai.response.completed"

    RESPONSE_FAILED: str = "ai.response.failed"

    # =====================================================
    # STREAMING
    # =====================================================

    STREAM_STARTED: str = "ai.stream.started"

    STREAM_CHUNK: str = "ai.stream.chunk"

    STREAM_COMPLETED: str = "ai.stream.completed"

    STREAM_CANCELLED: str = "ai.stream.cancelled"

    # Compatibilidade
    STREAM_START: str = "ai.stream.start"
    STREAM_UPDATE: str = "ai.stream.update"
    STREAM_END: str = "ai.stream.end"

    # =====================================================
    # PROVIDERS
    # =====================================================

    PROVIDER_SELECTED: str = "ai.provider.selected"

    PROVIDER_CHANGED: str = "ai.provider.changed"

    PROVIDER_REGISTERED: str = "ai.provider.registered"

    PROVIDER_UNREGISTERED: str = "ai.provider.unregistered"

    PROVIDER_ONLINE: str = "ai.provider.online"

    PROVIDER_OFFLINE: str = "ai.provider.offline"

    PROVIDER_FALLBACK: str = "ai.provider.fallback"

    PROVIDER_ERROR: str = "ai.provider.error"

    # =====================================================
    # MODELOS
    # =====================================================

    MODEL_LOADING: str = "ai.model.loading"

    MODEL_LOADED: str = "ai.model.loaded"

    MODEL_CHANGED: str = "ai.model.changed"

    MODEL_UNLOADED: str = "ai.model.unloaded"

    MODEL_ERROR: str = "ai.model.error"

    # =====================================================
    # COGNIÇÃO
    # =====================================================

    THINK_STARTED: str = "ai.think.started"

    THINK_COMPLETED: str = "ai.think.completed"

    REASONING_STARTED: str = "ai.reasoning.started"

    REASONING_COMPLETED: str = "ai.reasoning.completed"

    REFLECTION_CREATED: str = "ai.reflection.created"

    # =====================================================
    # CONTEXTO
    # =====================================================

    CONTEXT_CREATED: str = "ai.context.created"

    CONTEXT_UPDATED: str = "ai.context.updated"

    CONTEXT_CLEARED: str = "ai.context.cleared"

    # =====================================================
    # MEMÓRIA
    # =====================================================

    MEMORY_REQUIRED: str = "ai.memory.required"

    MEMORY_FOUND: str = "ai.memory.found"

    MEMORY_NOT_FOUND: str = "ai.memory.not_found"

    MEMORY_STORED: str = "ai.memory.stored"

    MEMORY_UPDATED: str = "ai.memory.updated"

    # =====================================================
    # FERRAMENTAS
    # =====================================================

    TOOL_SELECTED: str = "ai.tool.selected"

    TOOL_STARTED: str = "ai.tool.started"

    TOOL_COMPLETED: str = "ai.tool.completed"

    TOOL_FAILED: str = "ai.tool.failed"

    # =====================================================
    # APRENDIZADO
    # =====================================================

    LEARNING_STARTED: str = "ai.learning.started"

    LEARNING_COMPLETED: str = "ai.learning.completed"

    # =====================================================
    # AGENTES / PERSONAS
    # =====================================================

    AGENT_SELECTED: str = "ai.agent.selected"

    AGENT_CHANGED: str = "ai.agent.changed"

    PERSONALITY_CHANGED: str = "ai.personality.changed"

    # =====================================================
    # SISTEMA
    # =====================================================

    INITIALIZED: str = "ai.initialized"

    SHUTDOWN: str = "ai.shutdown"

    READY: str = "ai.ready"

    BUSY: str = "ai.busy"

    IDLE: str = "ai.idle"

    # =====================================================
    # ERROS
    # =====================================================

    ERROR: str = "ai.error"

    WARNING: str = "ai.warning"

    TIMEOUT: str = "ai.timeout"

    EXCEPTION: str = "ai.exception"