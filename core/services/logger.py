"""
=========================================
JARVIS CORE

Arquivo:
logger.py

Descrição:
Sistema central de logs do JARVIS.

Responsável por:
- Registrar eventos do sistema com segurança concorrente
- Escrita assíncrona/segura em disco
- Histórico operacional de performance otimizada
- Comunicação integrada com EventBus

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.2 - High Performance)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from collections import deque
from datetime import datetime
from pathlib import Path

from core.base.module import (
    Module,
    ModuleStatus
)


class Logger(Module):
    """
    Serviço central de logs thread-safe para o ecossistema JARVIS.
    """

    def __init__(self):
        super().__init__("core.logger")
        self.version = "2.2"
        self.event_bus = None
        
        self.log_folder = Path("logs")
        self.log_file = self.log_folder / "jarvis.log"
        
        # deque com maxlen remove o item mais antigo automaticamente sem reindexar a memória
        self.max_history = 500
        self.history = deque(maxlen=self.max_history)
        
        # Trava para impedir concorrência de I/O em arquivos por múltiplas threads
        self._lock = threading.Lock()

    # =====================================================
    # Dependências
    # =====================================================

    def connect_event_bus(self, event_bus):
        self.event_bus = event_bus

    # =====================================================
    # Ciclo de vida
    # =====================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        try:
            self.log_folder.mkdir(parents=True, exist_ok=True)
            self._write("BOOT", "Sistema de logs inicializado")
            
            self.set_status(ModuleStatus.ONLINE)
            self.success("Logger ONLINE")
            self.emit("LOGGER_STARTED")
        except Exception as error:
            self.set_error(str(error))

    def shutdown(self):
        self.info("Logger encerrando")
        self.emit("LOGGER_STOPPED")
        self.set_status(ModuleStatus.OFFLINE)

    # =====================================================
    # Eventos
    # =====================================================

    def emit(self, event, *args, **kwargs):
        if self.event_bus:
            try:
                self.event_bus.emit(event, *args, **kwargs)
            except Exception:
                pass  # Evita que uma falha no barramento de eventos derrube o Logger

    # =====================================================
    # API pública de Log
    # =====================================================

    def debug(self, message):
        self._write("DEBUG", message)

    def info(self, message):
        self._write("INFO", message)

    def success(self, message):
        self._write(" OK ", message)

    def warning(self, message):
        self._write("WARN", message)

    def error(self, message):
        self._write("FAIL", message)

    # =====================================================
    # Escrita
    # =====================================================

    def _write(self, level, message):
        now = datetime.now()
        text = f"[{now:%Y-%m-%d %H:%M:%S}] [{level}] {message}"

        # Print imediato no console (operação atômica em nível de interpretador para sys.stdout)
        print(text)

        with self._lock:
            # Armazenamento rápido na estrutura circular
            self.history.append({
                "time": now.isoformat(),
                "level": level,
                "message": message
            })

            try:
                # Opcional: Garante diretório existente caso seja removido em runtime
                self.log_folder.mkdir(parents=True, exist_ok=True)
                
                with open(self.log_file, "a", encoding="utf-8") as file:
                    file.write(text + "\n")
            except Exception as error:
                print(f"[LOGGER CRITICAL ERROR] Falha ao gravar log em disco: {error}")

    # =====================================================
    # Diagnóstico
    # =====================================================

    def get_history(self):
        with self._lock:
            return list(self.history)