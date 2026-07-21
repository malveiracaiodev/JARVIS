"""
=========================================
GENESIS CORE

Arquivo:
core/runtime/component_state.py

Descrição:
Estados oficiais dos componentes da
Genesis Matrix (Mark IV - Neural Lattice).

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

from enum import Enum


class ComponentState(Enum):
    """
    Estados oficiais do ciclo de vida dos componentes
    e nós neurais do Genesis Core (Mark IV).
    """

    CREATED = "created"
    REGISTERED = "registered"
    BOOTING = "booting"
    ONLINE = "online"
    DEGRADED = "degraded"      # Novo: Operando sob limitações de recursos ou latência
    ISOLATED = "isolated"      # Novo: Sandbox/Processo isolado devido a anomalia
    FAILED = "failed"
    SHUTDOWN = "shutdown"
    OFFLINE = "offline"
    RESTARTING = "restarting"
    UNKNOWN = "unknown"

    def is_online(self) -> bool:
        """
        Indica se o componente está operacional ou funcionalmente ativo.
        """
        return self in (
            ComponentState.ONLINE,
            ComponentState.DEGRADED,
        )

    def is_active(self) -> bool:
        """
        Indica se o componente está em atividade ou sob gestão do lattice.
        """
        return self in (
            ComponentState.BOOTING,
            ComponentState.ONLINE,
            ComponentState.DEGRADED,
            ComponentState.ISOLATED,
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

    def is_isolated(self) -> bool:
        """
        Indica se o componente foi isolado para proteção do Core.
        """
        return self == ComponentState.ISOLATED

    def __str__(self) -> str:
        return self.value