"""
=========================================
JARVIS CORE

Arquivo:
core/mind/constants/thought_status.py

Descrição:
Estados possíveis de um pensamento
cognitivo.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from enum import Enum


class ThoughtStatus(str, Enum):
    """
    Estados possíveis de um pensamento.
    """

    CREATED = "created"

    ANALYZING = "analyzing"

    PLANNING = "planning"

    REASONING = "reasoning"

    EXECUTING = "executing"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"