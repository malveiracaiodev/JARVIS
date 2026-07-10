"""
=========================================
JARVIS CORE

Arquivo:
system_events.py

Descrição:
Eventos relacionados ao sistema.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""



class SystemEvents:
    """
    Eventos do núcleo do JARVIS.
    """



    START = (
        "system.start"
    )



    READY = (
        "system.ready"
    )



    SHUTDOWN = (
        "system.shutdown"
    )



    ERROR = (
        "system.error"
    )



    MODULE_STARTED = (
        "system.module.started"
    )



    MODULE_STOPPED = (
        "system.module.stopped"
    )



    HEALTH_CHECK = (
        "system.health.check"
    )