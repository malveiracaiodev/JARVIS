"""
=========================================
GENESIS CORE

Arquivo:
core/runtime/component_state.py

Descrição:
Estados oficiais dos componentes da
Genesis Matrix.

Todos os módulos registrados no
BootManager utilizam este catálogo
como padrão de ciclo de vida.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from enum import Enum


class ComponentState(Enum):
    """
    Estados oficiais do ciclo de vida
    dos componentes do Genesis Core.
    """

    CREATED = "created"
    REGISTERED = "registered"

    BOOTING = "booting"

    ONLINE = "online"

    FAILED = "failed"

    SHUTDOWN = "shutdown"

    OFFLINE = "offline"

    RESTARTING = "restarting"

    UNKNOWN = "unknown"

    def is_online(self) -> bool:
        """
        Indica se o componente está operacional.
        """
        return self == ComponentState.ONLINE

    def is_active(self) -> bool:
        """
        Indica se o componente está em atividade.
        """
        return self in (
            ComponentState.BOOTING,
            ComponentState.ONLINE,
            ComponentState.RESTARTING,
        )

    def is_finished(self) -> bool:
        """
        Indica se o ciclo do componente foi encerrado.
        """
        return self in (
            ComponentState.OFFLINE,
            ComponentState.SHUTDOWN,
            ComponentState.FAILED,
        )

    def __str__(self) -> str:
        return self.value