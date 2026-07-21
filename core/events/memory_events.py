"""
=========================================
GENESIS CORE - KNOWLEDGE & MEMORY EVENTS

Arquivo: core/events/memory_events.py
Descrição: Eventos relacionados ao sistema de memória do Genesis Core.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryEvents:
    """
    Barramento de eventos da memória e indexação contextual.
    """

    # Criação
    CREATED: str = "memory.created"
    SAVED: str = "memory.saved"
    UPDATED: str = "memory.updated"

    # Carregamento
    LOADED: str = "memory.loaded"
    RESTORED: str = "memory.restored"

    # Busca
    SEARCH: str = "memory.search"
    SEARCH_STARTED: str = "memory.search.started"
    SEARCH_COMPLETED: str = "memory.search.completed"
    CONTEXT_REQUIRED: str = "memory.context.required"

    # Tipos de Memória
    EPISODIC_CREATED: str = "memory.episodic.created"
    SEMANTIC_CREATED: str = "memory.semantic.created"
    WORKING_CONTEXT_CREATED: str = "memory.working.created"
    EXPERIENCE_CREATED: str = "memory.experience.created"

    # Aprendizado
    LESSON_LEARNED: str = "memory.lesson.learned"
    KNOWLEDGE_CONSOLIDATED: str = "memory.knowledge.consolidated"
    PATTERN_DISCOVERED: str = "memory.pattern.discovered"

    # Remoção
    DELETED: str = "memory.deleted"
    EXPIRED: str = "memory.expired"
    CLEANUP_STARTED: str = "memory.cleanup.started"
    CLEANUP_COMPLETED: str = "memory.cleanup.completed"

    # Sincronização
    INDEX_UPDATED: str = "memory.index.updated"
    CACHE_UPDATED: str = "memory.cache.updated"

    # Erros
    ERROR: str = "memory.error"