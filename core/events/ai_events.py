"""
=========================================
JARVIS CORE

Arquivo:
ai_events.py

Descrição:
Eventos da inteligência artificial.

Mark:
I - Heartbeat
=========================================
"""


class AIEvents:
    """
    Eventos da IA.
    """


    REQUEST = (
        "ai.request"
    )


    RESPONSE = (
        "ai.response"
    )


    MODEL_LOADED = (
        "ai.model.loaded"
    )


    MEMORY_REQUIRED = (
        "ai.memory.required"
    )