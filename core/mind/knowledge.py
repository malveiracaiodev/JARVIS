"""
=========================================
GENESIS CORE - KNOWLEDGE DATABASE

Arquivo: core/mind/knowledge.py
Descrição: Biblioteca estruturada de conhecimento semântico.
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

class Knowledge(Module):
    """
    Memória semântica estática e de fatos persistentes do Genesis Core.
    """

    def __init__(self):
        super().__init__("core.mind.knowledge")
        self.version = "Mark IV"
        self.folder = Path("data")
        self.file = self.folder / "knowledge.json"
        self.database: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        self.load()

    def initialize(self) -> bool:
        with self._lock:
            self.set_status(ModuleStatus.INITIALIZING)
            self.load()
            self.set_status(ModuleStatus.ONLINE)
            self._log_safe("success", "Knowledge Engine ONLINE.")
        return True

    def shutdown(self) -> bool:
        with self._lock:
            self.save()
            self.set_status(ModuleStatus.OFFLINE)
            self._log_safe("info", "Knowledge Engine desativada.")
        return True

    def _log_safe(self, level: str, message: str) -> None:
        if hasattr(self, "logger") and self.logger:
            method = getattr(self.logger, level, None)
            if callable(method):
                method(f"[{self.name}] {message}")
                return
        print(f"[KNOWLEDGE] [{level.upper()}] {message}")

    def load(self) -> None:
        with self._lock:
            try:
                self.folder.mkdir(exist_ok=True)
                if not self.file.exists():
                    self.database = []
                    self.save()
                    return
                with open(self.file, "r", encoding="utf-8") as file:
                    self.database = json.load(file)
            except Exception as error:
                self.database = []
                self._log_safe("error", f"Falha no carregamento: {error}")

    def save(self) -> None:
        with self._lock:
            try:
                self.folder.mkdir(exist_ok=True)
                with open(self.file, "w", encoding="utf-8") as file:
                    json.dump(self.database, file, indent=4, ensure_ascii=False)
            except Exception as error:
                self._log_safe("error", f"Falha na gravação: {error}")

    def add(self, topic: str, information: str, source: str = "internal", tags: Optional[List[str]] = None) -> Dict[str, Any]:
        with self._lock:
            entry = {
                "id": str(uuid.uuid4()),
                "topic": topic.strip(),
                "information": information,
                "source": source,
                "tags": tags or [],
                "created_at": datetime.now().isoformat()
            }
            self.database.append(entry)
            self.save()
            return entry

    def search(self, query: str, context: Optional[Any] = None) -> List[Dict[str, Any]]:
        query_clean = query.lower().strip()
        results = []
        with self._lock:
            for item in self.database:
                searchable_text = f"{item.get('topic','')} {item.get('information','')} {' '.join(item.get('tags',[]))}".lower()
                if query_clean in searchable_text:
                    results.append(item)
        return results

    def get_topic(self, topic: str) -> Optional[Dict[str, Any]]:
        target = topic.lower().strip()
        with self._lock:
            for item in self.database:
                if item["topic"].lower().strip() == target:
                    return item
        return None

    def remove(self, topic: str) -> bool:
        target = topic.lower().strip()
        with self._lock:
            old_size = len(self.database)
            self.database = [i for i in self.database if i["topic"].lower().strip() != target]
            if len(self.database) != old_size:
                self.save()
                return True
        return False

    def import_text(self, path: str) -> bool:
        file_path = Path(path)
        if not file_path.exists():
            return False
        try:
            self.add(
                topic=file_path.stem,
                information=file_path.read_text(encoding="utf-8"),
                source=str(file_path)
            )
            return True
        except Exception as error:
            self._log_safe("error", f"Falha na importação de arquivo: {error}")
            return False

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {"entries": len(self.database), "version": self.version}

    def total_entries(self) -> int:
        return len(self.database)

    def status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "entries": len(self.database),
            "file": str(self.file)
        }