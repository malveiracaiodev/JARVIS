"""
=========================================
JARVIS CORE

Arquivo:
character_events.py

Descrição:
Tópicos de eventos para gerenciamento de persona, humor e tom.

Arquitetura:
Genesis Core

Mark:
III - Intelligence
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterEvents:
    """
    Eventos de modulação de comportamento e aconselhamento.
    """
    GREETING: str = "character.greeting"
    MOOD_CHANGED: str = "character.mood.changed"
    MEMORY_CREATED: str = "character.memory.created"
    ADVICE_REQUESTED: str = "character.advice.requested"