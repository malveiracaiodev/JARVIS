"""
=========================================
JARVIS CORE

Arquivo:
core/mind/constants/priorities.py

Descrição:
Prioridades cognitivas do sistema.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from enum import IntEnum


class Priority(IntEnum):

    LOWEST = 0

    LOW = 25

    NORMAL = 50

    HIGH = 75

    CRITICAL = 100