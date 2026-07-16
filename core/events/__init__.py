"""
=========================================
GENESIS CORE

Arquivo:
core/events/__init__.py

Descrição:
Pacote central de barramento de eventos
do Genesis Core.

Responsável por expor todos os contratos
de comunicação assíncrona entre módulos.

Arquitetura:

Kernel
  |
EventBus
  |
Events Catalog


Eventos disponíveis:

- Sistema
- Usuário
- Voz
- Inteligência Artificial
- Plugins
- Personagens
- Memória
- Tarefas


Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


# ==================================================
# SISTEMA
# ==================================================

from .system_events import SystemEvents



# ==================================================
# USUÁRIO
# ==================================================

from .user_events import UserEvents



# ==================================================
# VOZ
# ==================================================

from .voice_events import VoiceEvents



# ==================================================
# INTELIGÊNCIA ARTIFICIAL
# ==================================================

from .ai_events import AIEvents



# ==================================================
# PLUGINS
# ==================================================

from .plugin_events import PluginEvents



# ==================================================
# PERSONAGENS / AGENTES
# ==================================================

from .character_events import CharacterEvents



# ==================================================
# MEMÓRIA
# ==================================================

from .memory_events import MemoryEvents



# ==================================================
# TAREFAS
# ==================================================

from .task_events import TaskEvents



# ==================================================
# API PÚBLICA DO PACOTE
# ==================================================

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