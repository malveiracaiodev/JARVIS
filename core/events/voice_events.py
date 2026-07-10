"""
=========================================
JARVIS CORE

Arquivo:
voice_events.py

Descrição:
Eventos do sistema de voz.

Mark:
I - Heartbeat
=========================================
"""


class VoiceEvents:
    """
    Eventos relacionados à voz.
    """


    LISTEN_START = (
        "voice.listen.start"
    )


    SPEECH_RECEIVED = (
        "voice.speech.received"
    )


    SPEAK_START = (
        "voice.speak.start"
    )


    SPEAK_END = (
        "voice.speak.end"
    )