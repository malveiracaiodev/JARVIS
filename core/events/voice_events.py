"""
=========================================
GENESIS CORE

Arquivo:
core/events/voice_events.py

Descrição:
Eventos relacionados ao sistema de voz
do Genesis Core.

Responsável pela comunicação entre:

- VoiceManager
- Speech To Text
- Text To Speech
- Cognitive Pipeline
- Agents
- User Interface

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from dataclasses import dataclass



@dataclass(
    frozen=True
)
class VoiceEvents:

    """
    Barramento de eventos do sistema
    de comunicação por voz.

    Representa todo o ciclo:

    ouvir → interpretar → responder
    """



    # ==================================================
    # WAKE WORD
    # ==================================================


    WAKE_DETECTED: str = (
        "voice.wake.detected"
    )


    WAKE_LOST: str = (
        "voice.wake.lost"
    )



    # ==================================================
    # CAPTURA DE ÁUDIO
    # ==================================================


    LISTEN_START: str = (
        "voice.listen.start"
    )


    LISTEN_ACTIVE: str = (
        "voice.listen.active"
    )


    LISTEN_END: str = (
        "voice.listen.end"
    )


    AUDIO_RECEIVED: str = (
        "voice.audio.received"
    )



    # ==================================================
    # SPEECH TO TEXT
    # ==================================================


    STT_STARTED: str = (
        "voice.stt.started"
    )


    SPEECH_RECEIVED: str = (
        "voice.speech.received"
    )


    TRANSCRIPTION_CREATED: str = (
        "voice.transcription.created"
    )


    STT_COMPLETED: str = (
        "voice.stt.completed"
    )


    STT_ERROR: str = (
        "voice.stt.error"
    )



    # ==================================================
    # PROCESSAMENTO
    # ==================================================


    COMMAND_DETECTED: str = (
        "voice.command.detected"
    )


    INTENT_DETECTED: str = (
        "voice.intent.detected"
    )



    # ==================================================
    # TEXT TO SPEECH
    # ==================================================


    RESPONSE_READY: str = (
        "voice.response.ready"
    )


    TTS_STARTED: str = (
        "voice.tts.started"
    )


    SPEAK_START: str = (
        "voice.speak.start"
    )


    SPEAK_STREAM: str = (
        "voice.speak.stream"
    )


    SPEAK_END: str = (
        "voice.speak.end"
    )


    TTS_COMPLETED: str = (
        "voice.tts.completed"
    )


    TTS_ERROR: str = (
        "voice.tts.error"
    )



    # ==================================================
    # PERSONALIDADE
    # ==================================================


    VOICE_CHANGED: str = (
        "voice.changed"
    )


    CHARACTER_VOICE_SELECTED: str = (
        "voice.character.selected"
    )



    # ==================================================
    # CONTROLE
    # ==================================================


    INTERRUPTED: str = (
        "voice.interrupted"
    )


    MUTED: str = (
        "voice.muted"
    )


    UNMUTED: str = (
        "voice.unmuted"
    )



    # ==================================================
    # ERROS
    # ==================================================


    DEVICE_ERROR: str = (
        "voice.device.error"
    )


    ERROR: str = (
        "voice.error"
    )