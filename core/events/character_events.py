"""
=========================================
GENESIS CORE

Arquivo:
core/events/character_events.py

Descrição:
Eventos relacionados ao sistema de
personalidade, agentes, comportamento
e interação social do Genesis.

Arquitetura:
Genesis Core

Mark:
III - Matrix
=========================================
"""


from dataclasses import dataclass



@dataclass(
    frozen=True
)
class CharacterEvents:

    """
    Barramento de eventos da camada
    de identidade e personalidade.

    Usado por:

    - AgentManager
    - Jarvis Agent
    - Rafiki Agent
    - MemoryManager
    - VoiceManager
    """



    # ==================================================
    # IDENTIDADE
    # ==================================================


    CHARACTER_CREATED: str = (
        "character.created"
    )


    CHARACTER_LOADED: str = (
        "character.loaded"
    )


    CHARACTER_REMOVED: str = (
        "character.removed"
    )



    # ==================================================
    # ATIVAÇÃO
    # ==================================================


    CHARACTER_ACTIVATED: str = (
        "character.activated"
    )


    CHARACTER_DEACTIVATED: str = (
        "character.deactivated"
    )


    PERSONALITY_CHANGED: str = (
        "character.personality.changed"
    )


    MODE_CHANGED: str = (
        "character.mode.changed"
    )



    # ==================================================
    # CONVERSAÇÃO
    # ==================================================


    GREETING: str = (
        "character.greeting"
    )


    RESPONSE_GENERATED: str = (
        "character.response.generated"
    )


    TONE_CHANGED: str = (
        "character.tone.changed"
    )



    # ==================================================
    # ESTADO INTERNO
    # ==================================================


    MOOD_CHANGED: str = (
        "character.mood.changed"
    )


    EMOTION_UPDATED: str = (
        "character.emotion.updated"
    )


    BEHAVIOR_ADAPTED: str = (
        "character.behavior.adapted"
    )



    # ==================================================
    # MEMÓRIA SOCIAL
    # ==================================================


    MEMORY_CREATED: str = (
        "character.memory.created"
    )


    MEMORY_ACCESSED: str = (
        "character.memory.accessed"
    )


    USER_PREFERENCE_LEARNED: str = (
        "character.user.preference.learned"
    )



    # ==================================================
    # CONSELHO / RAFIKI
    # ==================================================


    ADVICE_REQUESTED: str = (
        "character.advice.requested"
    )


    ADVICE_GENERATED: str = (
        "character.advice.generated"
    )


    LIFE_CONTEXT_UPDATED: str = (
        "character.life.context.updated"
    )



    # ==================================================
    # APRENDIZADO
    # ==================================================


    FEEDBACK_RECEIVED: str = (
        "character.feedback.received"
    )


    LEARNING_STARTED: str = (
        "character.learning.started"
    )


    LEARNING_COMPLETED: str = (
        "character.learning.completed"
    )



    # ==================================================
    # ERROS
    # ==================================================


    CHARACTER_ERROR: str = (
        "character.error"
    )