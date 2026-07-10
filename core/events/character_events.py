"""
=========================================
JARVIS CORE

Arquivo:
character_events.py

Descrição:
Eventos de personalidade.

Mark:
I - Heartbeat
=========================================
"""


class CharacterEvents:
    """
    Eventos da personalidade do JARVIS.
    """


    GREETING = (
        "character.greeting"
    )


    MOOD_CHANGED = (
        "character.mood.changed"
    )


    MEMORY_CREATED = (
        "character.memory.created"
    )


    ADVICE_REQUESTED = (
        "character.advice.requested"
    )