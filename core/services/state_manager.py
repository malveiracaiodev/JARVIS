"""
=========================================
JARVIS CORE

Arquivo:
core/services/state_manager.py

Descrição:
Gerenciador do estado global do Genesis Core.

Responsável por:
- Controlar estado operacional
- Registrar transições
- Monitorar ciclo de vida
- Emitir eventos de sistema
- Fornecer diagnóstico global

Arquitetura:
Genesis Core

Mark:
III - Matrix (State Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

import copy
import threading
from enum import Enum
from datetime import datetime
from collections import deque
from core.base.module import Module, ModuleStatus

class SystemState(Enum):
    BOOTING = "BOOTING"
    INITIALIZING = "INITIALIZING"
    ONLINE = "ONLINE"
    IDLE = "IDLE"
    PROCESSING = "PROCESSING"
    BUSY = "BUSY"
    LEARNING = "LEARNING"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SHUTDOWN = "SHUTDOWN"

class StateManager(Module):
    """
    Controlador de Estado Mark III.
    Gerenciamento atômico e rastreabilidade forense de transições.
    """

    def __init__(self, logger=None, event_bus=None, max_history=200):
        super().__init__("core.state_manager")
        self.version = "3.1"
        self.logger = logger
        self.event_bus = event_bus
        self.state = SystemState.BOOTING
        self.last_change = datetime.now()
        self.history = deque(maxlen=max_history)
        self._lock = threading.RLock()

    # ======================================================
    # CONTROLE DE ESTADO ATÔMICO
    # ======================================================

    def change_state(self, new_state: SystemState):
        """Altera o estado com garantia de consistência (Matrix Layer)."""
        if not isinstance(new_state, SystemState):
            raise ValueError(f"Estado {new_state} inválido para o sistema.")

        with self._lock:
            if self.state == new_state:
                return

            old_state = self.state
            self.state = new_state
            self.last_change = datetime.now()

            record = {
                "from": old_state.value,
                "to": new_state.value,
                "time": self.last_change.isoformat()
            }

            self.history.append(record)
            
            # Notificação de mudança crítica
            self.emit("SYSTEM_STATE_CHANGED", record)
            self.log_info(f"Transição: {old_state.value} -> {new_state.value}")

    def get_snapshot(self):
        """Retorna uma leitura segura do estado atual e histórico recente."""
        with self._lock:
            return {
                "current": self.state.value,
                "last_change": self.last_change.isoformat(),
                "history_tail": list(self.history)[-5:] # Diagnóstico rápido
            }

    # ... [Manter initialize, shutdown e métodos auxiliares de Log/Event] ...