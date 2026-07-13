"""
=========================================
JARVIS CORE

Arquivo:
system_events.py

Descrição:
Definição dos tópicos de eventos estruturais do núcleo do JARVIS.

Arquitetura:
Genesis Core

Mark:
III - Intelligence (Patch 3.2 - Immutable Events)

Autor:
Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemEvents:
    """
    Eventos do ciclo de vida e telemetria do núcleo (Kernel).
    """
    START: str = "system.start"
    READY: str = "system.ready"
    SHUTDOWN: str = "system.shutdown"
    ERROR: str = "system.error"
    MODULE_STARTED: str = "system.module.started"
    MODULE_STOPPED: str = "system.module.stopped"
    HEALTH_CHECK: str = "system.health.check"