"""
=========================================
GENESIS CORE - UNIVERSAL BASE MODULE

Arquivo: core/base/module.py
Descrição: Classe base universal para todos os módulos do ecossistema Genesis.
Mark: IV - Matrix
Autor: Caio Vitor Malveira
=========================================
"""

import threading
import uuid
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional, Union


class ModuleStatus(Enum):
    OFFLINE = 0
    INITIALIZING = 1
    ONLINE = 2
    WARNING = 3
    ERROR = 4
    DISABLED = 5


class Module(ABC):
    """
    Classe base de todos os componentes Genesis (Agents, Services, Managers, etc).
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        version: str = "1.0",
        tags: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None
    ) -> None:
        # Identidade
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.description: str = description
        self.version: str = version

        # Classificação
        self.tags: List[str] = tags or []
        self.capabilities: List[str] = capabilities or []
        self.dependencies: List[str] = dependencies or []

        # Controle
        self.enabled: bool = True
        self.status: ModuleStatus = ModuleStatus.OFFLINE

        # Tempo
        self.created_at: datetime = datetime.now()
        self.started_at: Optional[datetime] = None
        self.stopped_at: Optional[datetime] = None

        # Erros
        self.error_message: Optional[str] = None

        # Métricas
        self.metrics: Dict[str, int] = {
            "starts": 0,
            "stops": 0,
            "errors": 0,
            "events": 0
        }

        # Configuração
        self.config: Dict[str, Any] = {}

        # Locks
        self._state_lock = threading.RLock()

        # Histórico (Thread-safe com limite fixo)
        self.status_history: deque = deque(maxlen=200)
        self.status_history.append({
            "status": self.status.name,
            "time": self.created_at.isoformat()
        })

    # ==========================================================
    # CICLO DE VIDA (CONTRATOS OBRIGATÓRIOS)
    # ==========================================================

    @abstractmethod
    def initialize(self) -> Any:
        """Inicialização executada pelo Kernel."""
        pass

    @abstractmethod
    def shutdown(self) -> Any:
        """Encerramento gracioso."""
        pass

    # ==========================================================
    # GERENCIAMENTO DE ESTADO
    # ==========================================================

    def set_status(self, status: ModuleStatus) -> None:
        if not isinstance(status, ModuleStatus):
            raise ValueError("Status inválido.")

        with self._state_lock:
            self.status = status
            self.status_history.append({
                "status": status.name,
                "time": datetime.now().isoformat()
            })

            if status == ModuleStatus.ONLINE:
                self.started_at = datetime.now()
                self.metrics["starts"] += 1
            elif status == ModuleStatus.OFFLINE:
                self.stopped_at = datetime.now()
                self.metrics["stops"] += 1

    def set_error(self, message: str) -> None:
        with self._state_lock:
            self.error_message = message
            self.metrics["errors"] += 1
            self.set_status(ModuleStatus.ERROR)

    def enable(self) -> None:
        with self._state_lock:
            self.enabled = True

    def disable(self) -> None:
        with self._state_lock:
            self.enabled = False
            self.set_status(ModuleStatus.DISABLED)

    # ==========================================================
    # CONSULTAS OPERACIONAIS
    # ==========================================================

    def get_status(self) -> ModuleStatus:
        with self._state_lock:
            return self.status

    def is_online(self) -> bool:
        return self.get_status() == ModuleStatus.ONLINE

    def is_enabled(self) -> bool:
        with self._state_lock:
            return self.enabled

    def has_error(self) -> bool:
        return self.get_status() == ModuleStatus.ERROR

    # ==========================================================
    # TELEMETRIA E DIAGNÓSTICO
    # ==========================================================

    def uptime(self) -> float:
        with self._state_lock:
            if not self.started_at:
                return 0.0
            return (datetime.now() - self.started_at).total_seconds()

    def health(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.name,
            "enabled": self.enabled,
            "uptime": self.uptime(),
            "errors": self.metrics["errors"]
        }

    def register_event(self) -> None:
        with self._state_lock:
            self.metrics["events"] += 1

    def info(self, message: Optional[str] = None) -> Union[Dict[str, Any], None]:
        """
        Retorna os metadados do módulo ou registra log caso uma mensagem seja passada.
        """
        if message:
            if hasattr(self, "logger") and self.logger:
                self.logger.info(message)
            return

        with self._state_lock:
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "version": self.version,
                "status": self.status.name,
                "enabled": self.enabled,
                "tags": self.tags,
                "capabilities": self.capabilities,
                "dependencies": self.dependencies,
                "created_at": self.created_at.isoformat(),
                "started_at": self.started_at.isoformat() if self.started_at else None,
                "uptime": self.uptime(),
                "metrics": self.metrics,
                "error": self.error_message,
                "history": list(self.status_history)
            }

    def __str__(self) -> str:
        return f"{self.name} [{self.status.name}]"