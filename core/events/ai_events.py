"""
=========================================
GENESIS CORE

Arquivo:
core/events/ai_events.py

Descrição:
Eventos relacionados ao ciclo de vida
dos sistemas de inteligência artificial.

Utilizado pelo EventBus para comunicação
entre módulos cognitivos.

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
class AIEvents:

    """
    Barramento de eventos da inteligência.

    Nenhum módulo deve chamar outro
    diretamente quando existir um evento.
    """



    # ==================================================
    # REQUISIÇÕES
    # ==================================================


    REQUEST: str = (
        "ai.request"
    )


    RESPONSE: str = (
        "ai.response"
    )


    STREAM_START: str = (
        "ai.stream.start"
    )


    STREAM_UPDATE: str = (
        "ai.stream.update"
    )


    STREAM_END: str = (
        "ai.stream.end"
    )



    # ==================================================
    # MODELOS
    # ==================================================


    MODEL_LOADING: str = (
        "ai.model.loading"
    )


    MODEL_LOADED: str = (
        "ai.model.loaded"
    )


    MODEL_UNLOADED: str = (
        "ai.model.unloaded"
    )


    MODEL_ERROR: str = (
        "ai.model.error"
    )



    # ==================================================
    # COGNIÇÃO
    # ==================================================


    THINK_STARTED: str = (
        "ai.think.started"
    )


    THINK_COMPLETED: str = (
        "ai.think.completed"
    )


    REASONING_STARTED: str = (
        "ai.reasoning.started"
    )


    REASONING_COMPLETED: str = (
        "ai.reasoning.completed"
    )



    # ==================================================
    # MEMÓRIA
    # ==================================================


    MEMORY_REQUIRED: str = (
        "ai.memory.required"
    )


    MEMORY_FOUND: str = (
        "ai.memory.found"
    )


    MEMORY_STORED: str = (
        "ai.memory.stored"
    )



    # ==================================================
    # APRENDIZADO
    # ==================================================


    LEARNING_STARTED: str = (
        "ai.learning.started"
    )


    LEARNING_COMPLETED: str = (
        "ai.learning.completed"
    )


    REFLECTION_CREATED: str = (
        "ai.reflection.created"
    )



    # ==================================================
    # AGENTES
    # ==================================================


    AGENT_SELECTED: str = (
        "ai.agent.selected"
    )


    PERSONALITY_CHANGED: str = (
        "ai.personality.changed"
    )



    # ==================================================
    # ERROS
    # ==================================================


    ERROR: str = (
        "ai.error"
    )


    TIMEOUT: str = (
        "ai.timeout"
    )