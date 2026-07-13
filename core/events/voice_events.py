"""
=========================================
JARVIS CORE

Arquivo:
voice_events.py

Descrição:
Tópicos de eventos do pipeline de captura e síntese de áudio (STT/TTS).

Arquitetura:
Genesis Core

Mark:
III - Intelligence
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceEvents:
    """
    Eventos de controle do ecossistema de voz.
    """
    LISTEN_START: str = "voice.listen.start"
    SPEECH_RECEIVED: str = "voice.speech.received"
    SPEAK_START: str = "voice.speak.start"
    SPEAK_END: str = "voice.speak.end"