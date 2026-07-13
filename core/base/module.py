"""
=========================================
JARVIS CORE

Arquivo:
module.py

Descrição:
Classe base abstrata, estável e thread-safe para todos os 
módulos e subsistemas do JARVIS.

Mark:
II - Evolution Stable (Patch 2.5 - Concurrency Hardened)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
import uuid
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from enum import Enum


class ModuleStatus(Enum):
    OFFLINE = 0
    INITIALIZING = 1
    ONLINE = 2
    WARNING = 3
    ERROR = 4


class Module(ABC):
    """
    Classe base de ciclo de vida e estado para todos os módulos do sistema.
    """

    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.version = "1.0"
        self.status = ModuleStatus.OFFLINE
        self.created_at = datetime.now()
        self.started_at = None
        self.error_message = None

        # Lock reentrante para sincronização de estado concorrente
        self._state_lock = threading.RLock()

        # Evita vazamento de memória usando histórico circular restrito a 100 registros
        self.status_history = deque(maxlen=100)
        self.status_history.append({
            "status": self.status.name,
            "time": self.created_at.isoformat()
        })

    # ==================================================
    # Interface Abstrata
    # ==================================================

    @abstractmethod
    def initialize(self):
        """Método executado durante a inicialização do módulo pelo Kernel."""
        pass

    @abstractmethod
    def shutdown(self):
        """Método executado para finalização graciosa do módulo pelo Kernel."""
        pass

    # ==================================================
    # Gerenciamento de Estado Operacional
    # ==================================================

    def set_status(self, status):
        if not isinstance(status, ModuleStatus):
            raise ValueError("Status inválido atribuído ao módulo.")

        with self._state_lock:
            self.status = status
            self.status_history.append({
                "status": status.name,
                "time": datetime.now().isoformat()
            })

            if status == ModuleStatus.ONLINE:
                self.started_at = datetime.now()

    def set_error(self, message):
        with self._state_lock:
            self.error_message = message
            self.set_status(ModuleStatus.ERROR)

    def restart(self):
        with self._state_lock:
            self.shutdown()
            self.initialize()

    # ==================================================
    # Métodos de Diagnóstico e Telemetria
    # ==================================================

    def get_status(self):
        with self._state_lock:
            return self.status

    def is_online(self):
        with self._state_lock:
            return self.status == ModuleStatus.ONLINE

    def is_offline(self):
        with self._state_lock:
            return self.status == ModuleStatus.OFFLINE

    def has_error(self):
        with self._state_lock:
            return self.status == ModuleStatus.ERROR

    def uptime(self):
        with self._state_lock:
            if not self.started_at:
                return 0.0
            return (datetime.now() - self.started_at).total_seconds()

    def info(self):
        with self._state_lock:
            return {
                "id": self.id,
                "name": self.name,
                "version": self.version,
                "status": self.status.name,
                "created_at": self.created_at.isoformat(),
                "started_at": self.started_at.isoformat() if self.started_at else None,
                "uptime": self.uptime(),
                "error": self.error_message,
                "history": list(self.status_history)
            }

    def __str__(self):
        with self._state_lock:
            return f"{self.name} [{self.status.name}]"