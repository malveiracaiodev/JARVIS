"""
=========================================
JARVIS CORE

Arquivo:
core/services/logger.py

Descrição:
Sistema central de logs do Genesis Core.

Responsável por:
- Registrar eventos do sistema
- Histórico operacional seguro
- Escrita concorrente em disco
- Comunicação com EventBus
- Diagnóstico do núcleo

Arquitetura:
Genesis Core

Mark:
III - Matrix (Logging Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
import copy
import os
from collections import deque
from datetime import datetime
from pathlib import Path
from core.base.module import Module, ModuleStatus


class Logger(Module):
    """
    Serviço de observabilidade de alta performance (Mark III - Matrix).
    """

    def __init__(self):
        super().__init__("core.logger")
        self.version = "3.1"
        self.event_bus = None
        self.log_folder = Path("logs")
        self.log_file = self.log_folder / "genesis_core.log"
        self.max_history = 1000
        self.history = deque(maxlen=self.max_history)
        self._lock = threading.RLock()

    def initialize(self) -> None:
        """Inicializa o subsistema de log, garantindo que o diretório exista."""
        with self._lock:
            try:
                self.log_folder.mkdir(parents=True, exist_ok=True)
                self.status = ModuleStatus.ONLINE
                self._write("INFO", "[LOGGER] Subsistema de log inicializado com sucesso.")
            except Exception as error:
                self.status = ModuleStatus.ERROR
                print(f"[LOGGER FATAL] Falha ao inicializar o logger: {error}")

    def shutdown(self) -> None:
        """Encerra o subsistema de log com segurança."""
        with self._lock:
            self._write("INFO", "[LOGGER] Encerrando subsistema de log...")
            self.status = ModuleStatus.OFFLINE

    def connect_event_bus(self, event_bus) -> None:
        """Conecta o logger ao barramento de eventos do núcleo."""
        with self._lock:
            self.event_bus = event_bus

    # ==================================================
    # MÉTODOS DE CONVENIÊNCIA (INTERFACE DO LOGGER)
    # ==================================================

    def info(self, message):
        self._write("INFO", message)

    def error(self, message):
        self._write("ERROR", message)

    def warning(self, message):
        self._write("WARNING", message)

    def success(self, message):
        self._write("SUCCESS", message)

    def debug(self, message):
        self._write("DEBUG", message)

    # ==================================================
    # ESCRITA E PERSISTÊNCIA
    # ==================================================

    def _write(self, level, message):
        """Escrita atômica com garantia de persistência física (fsync)."""
        now = datetime.now()
        log_entry = {
            "time": now.isoformat(),
            "level": level,
            "message": str(message)
        }
        text = f"[{now:%Y-%m-%d %H:%M:%S}] [{level}] {message}"

        # Exibição imediata no console
        print(text)

        with self._lock:
            # Mantém histórico em memória
            self.history.append(log_entry)

            # Escrita persistente no disco
            try:
                self.log_folder.mkdir(parents=True, exist_ok=True)
                with open(self.log_file, "a", encoding="utf-8") as file:
                    file.write(text + "\n")
                    file.flush()
                    os.fsync(file.fileno()) 
            except Exception as error:
                print(f"[LOGGER FAILURE] {error}")

    def get_history(self):
        with self._lock:
            return copy.deepcopy(list(self.history))