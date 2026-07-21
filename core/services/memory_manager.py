"""
=========================================
JARVIS CORE

Arquivo:
core/services/memory_manager.py

Descrição:
Gerenciador central da memória do Genesis Core.
Implementa a MemoryInterface para persistência
segura, histórico cognitivo, busca thread-safe,
recuperação contra corrupção e comunicação com EventBus.

Arquitetura:
Genesis Core

Mark:
V - Evolution (Memory Layer)

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
from core.interfaces.memory_interface import MemoryInterface

class MemoryManager(Module, MemoryInterface):
    """
    Gerenciador de memória persistente (Mark V - Evolution).
    Implementa o contrato MemoryInterface com foco em atomicidade,
    recuperação forense e resiliência.
    """

    MEMORY_FOLDER = Path("data/memory")
    MEMORY_FILE = MEMORY_FOLDER / "long_term.json"

    def __init__(self, logger=None, event_bus=None):
        Module.__init__(self, "core.memory_manager")
        self.version = "3.2"
        self.logger = logger
        self.event_bus = event_bus
        self.memories = []
        self._lock = threading.RLock()

    # ==================================================
    # IMPLEMENTAÇÃO DA MEMORY INTERFACE
    # ==================================================

    def store(self, data, memory_type="long_term"):
        """Armazena um dado de forma persistente."""
        with self._lock:
            entry = {
                "id": f"ltm_{int(datetime.now().timestamp())}_{len(self.memories)}",
                "data": data,
                "type": memory_type,
                "timestamp": datetime.now().isoformat()
            }
            self.memories.append(entry)
            self.save()
            return entry["id"]

    def retrieve(self, query, context=None):
        """Recupera memórias persistidas correspondentes à query."""
        with self._lock:
            if not query:
                return self.memories.copy()
            
            results = [
                item for item in self.memories 
                if query.lower() in str(item.get("data", "")).lower()
            ]
            return results

    def search(self, query, limit=10):
        """Busca estruturada nas memórias persistidas."""
        with self._lock:
            matches = self.retrieve(query)
            return matches[-limit:]

    def clear(self):
        """Limpa toda a base persistida."""
        with self._lock:
            count = len(self.memories)
            self.memories.clear()
            self.save()
            return f"MemoryManager limpo. {count} registros removidos."

    def forget(self, memory_id):
        """Remove uma memória específica pelo ID."""
        with self._lock:
            initial_len = len(self.memories)
            self.memories = [item for item in self.memories if item.get("id") != memory_id]
            if len(self.memories) < initial_len:
                self.save()
                return True
            return False

    def status(self):
        """Retorna o estado operacional."""
        with self._lock:
            return {
                "name": self.name(),
                "persisted_items": len(self.memories),
                "status": "operational"
            }

    def name(self):
        return "memory.long_term"

    # ==================================================
    # PERSISTÊNCIA E RESILIÊNCIA (FSYNC & CORRUPTION)
    # ==================================================

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
                if self.event_bus:
                    self.emit(MemoryEvents.SAVED)
                return True
            except Exception as error:
                if temp_file.exists():
                    temp_file.unlink()
                if self.logger:
                    self.log_error(f"Falha crítica na escrita da memória: {error}")
                raise

    def load(self):
        """Carregamento com isolamento de corrupção."""
        with self._lock:
            if not self.MEMORY_FILE.exists():
                self.memories = []
                if self.logger:
                    self.log_info("Memória inexistente. Inicializando estrutura vazia.")
                return

            try:
                with open(self.MEMORY_FILE, "r", encoding="utf-8") as file:
                    self.memories = json.load(file)
                if self.logger:
                    self.log_info(f"Memórias carregadas: {len(self.memories)}")
                if self.event_bus:
                    self.emit(MemoryEvents.LOADED)
            except (json.JSONDecodeError, TypeError, OSError) as e:
                if self.logger:
                    self.log_error(f"Corrupção detectada no arquivo de memória: {e}")
                self._handle_corruption()
                self.memories = []
                if self.event_bus:
                    self.emit(MemoryEvents.LOADED)

    def _handle_corruption(self):
        """Isola o arquivo corrompido para diagnóstico."""
        backup = self.MEMORY_FOLDER / f"corrupted_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            if self.MEMORY_FILE.exists():
                shutil.move(self.MEMORY_FILE, backup)
            if self.logger:
                self.log_error(f"Arquivo corrompido isolado em: {backup}")
        except Exception as e:
            if self.logger:
                self.log_error(f"Falha ao mover arquivo corrompido: {e}")