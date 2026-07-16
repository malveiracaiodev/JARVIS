"""
=========================================
GENESIS CORE

Arquivo:
core/events/memory_events.py

Descrição:
Eventos relacionados ao sistema de memória
do Genesis Core.

Responsável por comunicação entre:

- MemoryManager
- Reflection
- Reasoner
- Agents
- Cognitive Pipeline

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from dataclasses import dataclass



@dataclass(
    frozen=True
)
class MemoryEvents:

    """
    Barramento de eventos da memória.

    Representa o ciclo de vida das
    informações armazenadas pelo Genesis.
    """



    # ==================================================
    # CRIAÇÃO
    # ==================================================


    CREATED: str = (
        "memory.created"
    )


    SAVED: str = (
        "memory.saved"
    )


    UPDATED: str = (
        "memory.updated"
    )



    # ==================================================
    # CARREGAMENTO
    # ==================================================


    LOADED: str = (
        "memory.loaded"
    )


    RESTORED: str = (
        "memory.restored"
    )



    # ==================================================
    # BUSCA
    # ==================================================


    SEARCH: str = (
        "memory.search"
    )


    SEARCH_STARTED: str = (
        "memory.search.started"
    )


    SEARCH_COMPLETED: str = (
        "memory.search.completed"
    )


    CONTEXT_REQUIRED: str = (
        "memory.context.required"
    )



    # ==================================================
    # TIPOS DE MEMÓRIA
    # ==================================================


    EPISODIC_CREATED: str = (
        "memory.episodic.created"
    )


    SEMANTIC_CREATED: str = (
        "memory.semantic.created"
    )


    WORKING_CONTEXT_CREATED: str = (
        "memory.working.created"
    )


    EXPERIENCE_CREATED: str = (
        "memory.experience.created"
    )



    # ==================================================
    # APRENDIZADO
    # ==================================================


    LESSON_LEARNED: str = (
        "memory.lesson.learned"
    )


    KNOWLEDGE_CONSOLIDATED: str = (
        "memory.knowledge.consolidated"
    )


    PATTERN_DISCOVERED: str = (
        "memory.pattern.discovered"
    )



    # ==================================================
    # REMOÇÃO
    # ==================================================


    DELETED: str = (
        "memory.deleted"
    )


    EXPIRED: str = (
        "memory.expired"
    )


    CLEANUP_STARTED: str = (
        "memory.cleanup.started"
    )


    CLEANUP_COMPLETED: str = (
        "memory.cleanup.completed"
    )



    # ==================================================
    # SINCRONIZAÇÃO
    # ==================================================


    INDEX_UPDATED: str = (
        "memory.index.updated"
    )


    CACHE_UPDATED: str = (
        "memory.cache.updated"
    )



    # ==================================================
    # ERROS
    # ==================================================


    ERROR: str = (
        "memory.error"
    )