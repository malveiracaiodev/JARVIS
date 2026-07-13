"""
=========================================
JARVIS CORE

Arquivo:
memory_events.py

Descrição:
Tópicos de eventos vinculados ao armazenamento semântico e memórias episódicas.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryEvents:
    """
    Eventos de indexação, busca e limpeza nas trilhas de memória.
    """
    CREATED: str = "memory.created"
    LOADED: str = "memory.loaded"
    SAVED: str = "memory.saved"
    SEARCH: str = "memory.search"
    DELETED: str = "memory.deleted"