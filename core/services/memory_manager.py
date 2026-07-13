"""
=========================================
JARVIS CORE

Arquivo:
memory_manager.py

Descrição:
Gerenciador de armazenamento da memória.

Responsável por:
- Persistência de dados atômica e segura
- Carregamento com tratamento de falhas
- Histórico e busca thread-safe
- Eventos de memória

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.1 - Production Ready)

Autor:
Caio Vitor Malveira
=========================================
"""

import json
import shutil
import threading
from pathlib import Path
from datetime import datetime

from core.base.module import (
    Module,
    ModuleStatus
)
from core.events import MemoryEvents


class MemoryManager(Module):
    """
    Serviço responsável pela persistência estável da memória do JARVIS.
    """

    MEMORY_FOLDER = Path("data/memory")
    MEMORY_FILE = MEMORY_FOLDER / "long_term.json"

    def __init__(self, logger=None, event_bus=None):
        super().__init__("core.memory_manager")
        self.version = "2.1"
        self.logger = logger
        self.event_bus = event_bus
        self.memories = []
        self._lock = threading.RLock()  # Proteção contra concorrência de múltiplos módulos

    # ==========================================================
    # Ciclo de vida
    # ==========================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        try:
            self.MEMORY_FOLDER.mkdir(parents=True, exist_ok=True)
            self.load()

            if self.event_bus:
                self.event_bus.subscribe(MemoryEvents.SEARCH, self.search)

            self.set_status(ModuleStatus.ONLINE)
            self.log_success("Memory Manager iniciado com persistência segura")
        except Exception as error:
            self.set_error(str(error))

    def shutdown(self):
        self.save()
        self.set_status(ModuleStatus.OFFLINE)
        self.log_info("Memory Manager encerrado")

    # ==========================================================
    # Memória
    # ==========================================================

    def remember(self, content, memory_type="experience", importance=1):
        with self._lock:
            # Garante ID incremental seguro baseado no conteúdo atual
            next_id = max([m.get("id", 0) for m in self.memories], default=0) + 1
            
            memory = {
                "id": next_id,
                "type": memory_type,
                "content": content,
                "importance": importance,
                "created": datetime.now().isoformat()
            }

            self.memories.append(memory)
            self.emit(MemoryEvents.CREATED, memory)
            self.save()
            return memory

    def last_events(self, limit=10):
        with self._lock:
            return self.memories[-limit:]

    def search(self, text):
        if not text:
            return []
            
        target = text.lower()
        results = []
        
        with self._lock:
            for memory in self.memories:
                content = str(memory.get("content", "")).lower()
                if target in content:
                    results.append(memory)
                    
        return results

    # ==========================================================
    # Persistência
    # ==========================================================

    def load(self):
        with self._lock:
            if not self.MEMORY_FILE.exists():
                self.memories = []
                self.log_info("Base de dados de memória não encontrada. Inicializando estrutura vazia.")
                return

            try:
                with open(self.MEMORY_FILE, "r", encoding="utf-8") as file:
                    self.memories = json.load(file)
                self.log_info(f"Memórias carregadas: {len(self.memories)}")
                self.emit(MemoryEvents.LOADED)
            except (json.JSONDecodeError, TypeError) as decode_error:
                # Recuperação de desastres: se o arquivo JSON quebrar, cria um backup e não trava o boot do JARVIS
                backup_path = self.MEMORY_FOLDER / f"corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                shutil.copy(self.MEMORY_FILE, backup_path)
                self.memories = []
                if self.logger and hasattr(self.logger, "error"):
                    self.logger.error(f"Arquivo de memória corrompido! Backup gerado em {backup_path.name}. Resetando banco.")
                self.emit(MemoryEvents.LOADED)

    def save(self):
        with self._lock:
            temp_file = self.MEMORY_FILE.with_suffix(".tmp")
            try:
                # Escrita atômica: primeiro escreve no arquivo temporário
                with open(temp_file, "w", encoding="utf-8") as file:
                    json.dump(self.memories, file, indent=4, ensure_ascii=False)
                
                # Se deu tudo certo na escrita, substitui o oficial instantaneamente
                if temp_file.exists():
                    temp_file.replace(self.MEMORY_FILE)
                    
                self.emit(MemoryEvents.SAVED)
            except Exception as e:
                if temp_file.exists():
                    temp_file.unlink()
                if self.logger and hasattr(self.logger, "error"):
                    self.logger.error(f"Falha ao salvar memórias no disco: {str(e)}")
                raise e

    # ==========================================================
    # Auxiliares
    # ==========================================================

    def emit(self, event, *args):
        if self.event_bus:
            self.event_bus.emit(event, *args)

    def log_info(self, message):
        if self.logger:
            self.logger.info(message)

    def log_success(self, message):
        if self.logger:
            self.logger.success(message)