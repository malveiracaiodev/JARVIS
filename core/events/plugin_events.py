"""
=========================================
JARVIS CORE

Arquivo:
plugin_events.py

Descrição:
Tópicos de eventos para ciclo de vida dos módulos dinâmicos (Plugins).

Arquitetura:
Genesis Core

Mark:
III - Intelligence
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PluginEvents:
    """
    Eventos emitidos por extensões acopladas dinamicamente ao Core.
    """
    LOADED: str = "plugin.loaded"
    UNLOADED: str = "plugin.unloaded"
    ERROR: str = "plugin.error"