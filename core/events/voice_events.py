"""
=========================================
GENESIS CORE - VOICE STREAMING EVENTS

Arquivo: core/events/voice_events.py
Descrição: Eventos do ecossistema de voz e processamento acústico.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceEvents:
    """
    Barramento de eventos do sistema de comunicação por voz (Ouvir -> Interpretar -> Responder).
    """

    # Wake Word
    WAKE_DETECTED: str = "voice.wake.detected"
    WAKE_LOST: str = "voice.wake.lost"

    # Captura de Áudio
    LISTEN_START: str = "voice.listen.start"
    LISTEN_ACTIVE: str = "voice.listen.active"
    LISTEN_END: str = "voice.listen.end"
    AUDIO_RECEIVED: str = "voice.audio.received"

    # Speech To Text
    STT_STARTED: str = "voice.stt.started"
    SPEECH_RECEIVED: str = "voice.speech.received"
    TRANSCRIPTION_CREATED: str = "voice.transcription.created"
    STT_COMPLETED: str = "voice.stt.completed"
    STT_ERROR: str = "voice.stt.error"

    # Processamento
    COMMAND_DETECTED: str = "voice.command.detected"
    INTENT_DETECTED: str = "voice.intent.detected"

    # Text To Speech
    RESPONSE_READY: str = "voice.response.ready"
    TTS_STARTED: str = "voice.tts.started"
    SPEAK_START: str = "voice.speak.start"
    SPEAK_STREAM: str = "voice.speak.stream"
    SPEAK_END: str = "voice.speak.end"
    TTS_COMPLETED: str = "voice.tts.completed"
    TTS_ERROR: str = "voice.tts.error"

    # Personalidade
    VOICE_CHANGED: str = "voice.changed"
    CHARACTER_VOICE_SELECTED: str = "voice.character.selected"

    # Controle
    INTERRUPTED: str = "voice.interrupted"
    MUTED: str = "voice.muted"
    UNMUTED: str = "voice.unmuted"

    # Erros
    DEVICE_ERROR: str = "voice.device.error"
    ERROR: str = "voice.error"