"""
=========================================
GENESIS CORE - CENTRAL EVENT CATALOG

Arquivo: core/events/__init__.py
Descrição: Pacote central de barramento de eventos do Genesis Core.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from core.events.system_events import SystemEvents
from core.events.user_events import UserEvents
from core.events.voice_events import VoiceEvents
from core.events.ai_events import AIEvents
from core.events.plugin_events import PluginEvents
from core.events.character_events import CharacterEvents
from core.events.memory_events import MemoryEvents
from core.events.task_events import TaskEvents

__all__ = [
    "SystemEvents",
    "UserEvents",
    "VoiceEvents",
    "AIEvents",
    "PluginEvents",
    "CharacterEvents",
    "MemoryEvents",
    "TaskEvents",
]