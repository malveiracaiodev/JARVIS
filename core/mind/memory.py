"""
=========================================
GENESIS CORE - EPISODIC MEMORY

Arquivo: core/mind/memory.py
Descrição: Sistema de memória episódica persistente e de longo prazo.
Mark: IV - Thought Engine
=========================================
"""

import json
import threading
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.base.module import Module, ModuleStatus

class Memory(Module):
    """
    Abstração de armazenamento de logs de experiências e interações históricas.
    """

    def __init__(self):
        super().__init__("core.mind.memory")
        self.version = "Mark IV"
        self.folder = Path("data")
        self.file = self.folder / "memory.json"
        self.entries: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        self.load()

    def initialize(self) -> bool:
        with self._lock:
            self.set_status(ModuleStatus.INITIALIZING)
            self.load()
            self.set_status(ModuleStatus.ONLINE)
            self._log_safe("success", "Memory System ONLINE.")
        return True

    def shutdown(self) -> bool:
        with self._lock:
            self.save()
            self.set_status(ModuleStatus.OFFLINE)
            self._log_safe("info", "Memory System descarregado.")
        return True

    def _log_safe(self, level: str, message: str) -> None:
        if getattr(self, "logger", None):
            method = getattr(self.logger, level, None)
            if callable(method):
                method(f"[{self.name}] {message}")
                return
        print(f"[MEMORY] [{level.upper()}] {message}")

    def load(self) -> None:
        with self._lock:
            try:
                self.folder.mkdir(exist_ok=True)
                if not self.file.exists():
                    self.entries = []
                    self.save()
                    return
                with open(self.file, "r", encoding="utf-8") as archive:
                    self.entries = json.load(archive)
            except Exception as error:
                self.entries = []
                self._log_safe("error", f"Erro ao ler registros: {error}")

    def save(self) -> None:
        with self._lock:
            try:
                with open(self.file, "w", encoding="utf-8") as archive:
                    json.dump(self.entries, archive, indent=4, ensure_ascii=False)
            except Exception as error:
                self._log_safe("error", f"Erro ao gravar registros: {error}")

    def store(self, data: Any, memory_type: str = "general", importance: int = 1) -> Dict[str, Any]:
        with self._lock:
            entry = {
                "id": str(uuid.uuid4()),
                "type": memory_type,
                "data": data,
                "importance": importance,
                "created_at": datetime.now().isoformat()
            }
            self.entries.append(entry)
            self.save()
            return entry

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        query_clean = query.lower().strip()
        result = []
        with self._lock:
            for item in self.entries:
                text = json.dumps(item["data"], ensure_ascii=False).lower()
                if query_clean in text:
                    result.append(item)
        return result

    def last(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            return self.entries[-limit:]

    def get(self, memory_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            for item in self.entries:
                if item["id"] == memory_id:
                    return item
        return None

    def remove(self, memory_id: str) -> bool:
        with self._lock:
            old_size = len(self.entries)
            self.entries = [i for i in self.entries if i["id"] != memory_id]
            if len(self.entries) != old_size:
                self.save()
                return True
        return False

    def clear(self) -> None:
        with self._lock:
            self.entries.clear()
            self.save()

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"total": len(self.entries), "version": self.version}

    def status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "memories": len(self.entries),
            "file": str(self.file)
        }