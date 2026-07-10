"""
=========================================
JARVIS CORE

Arquivo:
plugin_events.py

Descrição:
Eventos de plugins.

Mark:
I - Heartbeat
=========================================
"""


class PluginEvents:
    """
    Eventos de plugins.
    """


    LOADED = (
        "plugin.loaded"
    )


    UNLOADED = (
        "plugin.unloaded"
    )


    ERROR = (
        "plugin.error"
    )