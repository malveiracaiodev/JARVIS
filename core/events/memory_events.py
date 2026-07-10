"""
=========================================
JARVIS CORE

Arquivo:
memory_events.py

Descrição:
Eventos relacionados ao sistema
de memória do JARVIS.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


class MemoryEvents:
    """
    Eventos do sistema de memória.
    """


    CREATED = (
        "memory.created"
    )


    LOADED = (
        "memory.loaded"
    )


    SAVED = (
        "memory.saved"
    )


    SEARCH = (
        "memory.search"
    )


    DELETED = (
        "memory.deleted"
    )