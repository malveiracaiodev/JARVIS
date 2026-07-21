"""
=========================================
JARVIS CORE

Arquivo:
core/services/memory_manager.py

Descrição:
Gerenciador central da memória do Genesis Core.

Responsável por:
- Persistência segura de memórias
- Histórico cognitivo
- Busca thread-safe
- Recuperação contra corrupção
- Comunicação com EventBus

Arquitetura:
Genesis Core

Mark:
III - Matrix (Memory Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

import copy
import json
import os
import shutil
import threading
from datetime import datetime
from pathlib import Path
from core.base.module import Module, ModuleStatus
from core.events import MemoryEvents

class MemoryManager(Module):
    """
    Gerenciador de memória persistente (Mark III - Matrix).
    Foco em atomicidade, recuperação forense e resiliência.
    """

    MEMORY_FOLDER = Path("data/memory")
    MEMORY_FILE = MEMORY_FOLDER / "long_term.json"

    def __init__(self, logger=None, event_bus=None):
        super().__init__("core.memory_manager")
        self.version = "3.1"
        self.logger = logger
        self.event_bus = event_bus
        self.memories = []
        self._lock = threading.RLock()

    # ... [Mantenha os métodos initialize e shutdown inalterados] ...

    def save(self):
        """Salva memórias com garantia de persistência física (fsync)."""
        with self._lock:
            self.MEMORY_FOLDER.mkdir(parents=True, exist_ok=True)
            temp_file = self.MEMORY_FILE.with_suffix(".tmp")
            
            try:
                with open(temp_file, "w", encoding="utf-8") as file:
                    json.dump(self.memories, file, indent=4, ensure_ascii=False)
                    file.flush()
                    # Garante que o SO descarregou os dados no disco físico
                    os.fsync(file.fileno())
                
                # Substituição atômica no sistema de arquivos
                temp_file.replace(self.MEMORY_FILE)
                self.emit(MemoryEvents.SAVED)
            except Exception as error:
                if temp_file.exists():
                    temp_file.unlink()
                self.log_error(f"Falha crítica na escrita da memória: {error}")
                raise

    def load(self):
        """Carregamento com isolamento de corrupção."""
        with self._lock:
            if not self.MEMORY_FILE.exists():
                self.memories = []
                self.log_info("Memória inexistente. Inicializando estrutura vazia.")
                return

            try:
                with open(self.MEMORY_FILE, "r", encoding="utf-8") as file:
                    self.memories = json.load(file)
                self.log_info(f"Memórias carregadas: {len(self.memories)}")
                self.emit(MemoryEvents.LOADED)
            except (json.JSONDecodeError, TypeError, OSError) as e:
                self.log_error(f"Corrupção detectada no arquivo de memória: {e}")
                self._handle_corruption()
                self.memories = []
                self.emit(MemoryEvents.LOADED)

    def _handle_corruption(self):
        """Isola o arquivo corrompido para diagnóstico."""
        backup = self.MEMORY_FOLDER / f"corrupted_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            shutil.move(self.MEMORY_FILE, backup)
            self.log_error(f"Arquivo corrompido isolado em: {backup}")
        except Exception as e:
            self.log_error(f"Falha ao mover arquivo corrompido: {e}")

    # ... [Mantenha remember, last_events e search inalterados] ...