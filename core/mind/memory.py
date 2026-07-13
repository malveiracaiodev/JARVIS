"""
=========================================
JARVIS CORE

Arquivo:
core/mind/memory.py

Descrição:
Sistema de memória de curto/longo prazo persistente e thread-safe.

Arquitetura:
Genesis Core

Mark:
III - Matrix (Cognitive Support Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

import json
import threading
from pathlib import Path
from datetime import datetime
from core.base.module import Module, ModuleStatus


class Memory(Module):
    """
    Submódulo de gerenciamento e persistência de memórias episódicas e contextuais.
    """

    def __init__(self):
        super().__init__("core.mind.memory")
        self.version = "3.0"
        self.folder = Path("data")
        self.file = self.folder / "memory.json"
        self.entries = []
        self._lock = threading.RLock()
        self.load()

    def initialize(self):
        with self._lock:
            self.set_status(ModuleStatus.INITIALIZING)
            self.load()
            self.set_status(ModuleStatus.ONLINE)
            self._log_safe("success", "Subsistema de memória episódica ONLINE.")

    def shutdown(self):
        with self._lock:
            self.save()
            self.set_status(ModuleStatus.OFFLINE)
            self._log_safe("info", "Subsistema de memória descarregado.")

    def _log_safe(self, level, message):
        """Roteamento seguro de logging para compatibilidade de classes pai."""
        if hasattr(self, "logger") and self.logger:
            log_method = getattr(self.logger, level, None)
            if log_method and callable(log_method):
                log_method(f"[{self.name}] {message}")
                return
        
        log_fallback = getattr(super(), level, None)
        if log_fallback and callable(log_fallback):
            try:
                log_fallback(message)
            except TypeError:
                print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{level.upper()}] [{self.name}] {message}")

    def load(self):
        with self._lock:
            try:
                self.folder.mkdir(exist_ok=True)
                if not self.file.exists():
                    self.entries = []
                    self.save()
                    return

                with open(self.file, "r", encoding="utf-8") as archive:
                    data = json.load(archive)
                
                self.entries = [self._normalize(item) for item in data]
            except Exception as error:
                self.entries = []
                self._log_safe("error", f"Erro ao ler banco de memórias: {error}")

    def save(self):
        with self._lock:
            try:
                self.folder.mkdir(exist_ok=True)
                with open(self.file, "w", encoding="utf-8") as archive:
                    json.dump(self.entries, archive, indent=4, ensure_ascii=False)
            except Exception as error:
                self._log_safe("error", f"Erro ao persistir memórias em disco: {error}")

    def _normalize(self, item):
        if not isinstance(item, dict):
            return {"id": len(self.entries) + 1, "data": item, "created_at": datetime.now().isoformat()}
        
        target_data = item.get("data", item)
        created_at = item.get("created_at", item.get("created", item.get("timestamp", datetime.now().isoformat())))
        return {
            "id": item.get("id", len(self.entries) + 1),
            "data": target_data,
            "created_at": created_at
        }

    def store(self, data):
        with self._lock:
            entry = {
                "id": len(self.entries) + 1,
                "data": data,
                "created_at": datetime.now().isoformat()
            }
            self.entries.append(entry)
            self.save()
            return entry

    def retrieve(self, query):
        query_clean = query.lower().strip()
        results = []
        with self._lock:
            for item in self.entries:
                text_snapshot = json.dumps(item["data"], ensure_ascii=False).lower()
                if query_clean in text_snapshot:
                    results.append(item)
        return results

    def last(self, limit=10):
        with self._lock:
            return list(self.entries[-limit:])

    def get(self, memory_id):
        with self._lock:
            for item in self.entries:
                if item["id"] == memory_id:
                    return item
        return None

    def remove(self, memory_id):
        with self._lock:
            before = len(self.entries)
            self.entries = [item for item in self.entries if item["id"] != memory_id]
            if len(self.entries) != before:
                self.save()
                return True
            return False

    def clear(self):
        with self._lock:
            self.entries = []
            self.save()

    def status(self):
        with self._lock:
            return {
                "name": self.name,
                "version": self.version,
                "memories": len(self.entries),
                "file": str(self.file)
            }