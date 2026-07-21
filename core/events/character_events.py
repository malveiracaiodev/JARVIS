"""
=========================================
GENESIS CORE - CHARACTER & AGENT EVENTS

Arquivo: core/events/character_events.py
Descrição: Eventos do sistema de personalidade, agentes e comportamento.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterEvents:
    """
    Barramento de eventos da camada de identidade e personalidade.
    """

    # Identidade
    CHARACTER_CREATED: str = "character.created"
    CHARACTER_LOADED: str = "character.loaded"
    CHARACTER_REMOVED: str = "character.removed"

    # Ativação
    CHARACTER_ACTIVATED: str = "character.activated"
    CHARACTER_DEACTIVATED: str = "character.deactivated"
    PERSONALITY_CHANGED: str = "character.personality.changed"
    MODE_CHANGED: str = "character.mode.changed"

    # Conversação
    GREETING: str = "character.greeting"
    RESPONSE_GENERATED: str = "character.response.generated"
    TONE_CHANGED: str = "character.tone.changed"

    # Estado Interno
    MOOD_CHANGED: str = "character.mood.changed"
    EMOTION_UPDATED: str = "character.emotion.updated"
    BEHAVIOR_ADAPTED: str = "character.behavior.adapted"

    # Memória Social
    MEMORY_CREATED: str = "character.memory.created"
    MEMORY_ACCESSED: str = "character.memory.accessed"
    USER_PREFERENCE_LEARNED: str = "character.user.preference.learned"

    # Conselho / Rafiki
    ADVICE_REQUESTED: str = "character.advice.requested"
    ADVICE_GENERATED: str = "character.advice.generated"
    LIFE_CONTEXT_UPDATED: str = "character.life.context.updated"

    # Aprendizado
    FEEDBACK_RECEIVED: str = "character.feedback.received"
    LEARNING_STARTED: str = "character.learning.started"
    LEARNING_COMPLETED: str = "character.learning.completed"

    # Erros
    CHARACTER_ERROR: str = "character.error"