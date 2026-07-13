"""
=========================================
JARVIS CORE

Arquivo:
core/mind/knowledge.py

Descrição:
Biblioteca estruturada de fatos, axiomas e documentos locais para a inteligência.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import json
import threading
from pathlib import Path
from datetime import datetime
from core.base.module import Module, ModuleStatus


class Knowledge(Module):
    """
    Biblioteca de Conhecimento Semântico estática do Core.
    """

    def __init__(self):
        super().__init__("core.mind.knowledge")
        self.version = "3.0"
        self.folder = Path("data")
        self.file = self.folder / "knowledge.json"
        self.database = []
        self._lock = threading.RLock()
        self.load()

    def initialize(self):
        with self._lock:
            self.set_status(ModuleStatus.INITIALIZING)
            self.load()
            self.set_status(ModuleStatus.ONLINE)
            self._log_safe("success", "Base de conhecimento semântica sincronizada.")

    def shutdown(self):
        with self._lock:
            self.save()
            self.set_status(ModuleStatus.OFFLINE)
            self._log_safe("info", "Base de conhecimento descarregada com sucesso.")

    def _log_safe(self, level, message):
        """Evita colisões com assinaturas rígidas da classe base Module."""
        if hasattr(self, "logger") and self.logger:
            log_method = getattr(self.logger, level, None)
            if log_method and callable(log_method):
                log_method(f"[{self.name}] {message}")
                return
        
        # Fallback de log herdado da classe base
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
                    self.database = []
                    self.save()
                    return
                with open(self.file, "r", encoding="utf-8") as file:
                    self.database = json.load(file)
            except Exception as error:
                self.database = []
                self._log_safe("error", f"Falha de leitura na base de conhecimento: {error}")

    def save(self):
        with self._lock:
            try:
                self.folder.mkdir(exist_ok=True)
                with open(self.file, "w", encoding="utf-8") as file:
                    json.dump(self.database, file, indent=4, ensure_ascii=False)
            except Exception as error:
                self._log_safe("error", f"Falha de escrita na base de conhecimento: {error}")

    def add(self, topic, information, source="internal", tags=None):
        with self._lock:
            entry = {
                "id": len(self.database) + 1,
                "topic": topic,
                "information": information,
                "source": source,
                "tags": tags or [],
                "created_at": datetime.now().isoformat()
            }
            self.database.append(entry)
            self.save()
            return entry

    def search(self, query):
        query_clean = query.lower().strip()
        results = []
        with self._lock:
            for item in self.database:
                searchable_text = f"{item.get('topic', '')} {item.get('information', '')} {' '.join(item.get('tags', []))}".lower()
                if query_clean in searchable_text:
                    results.append(item)
        return results

    def get_topic(self, topic):
        target_topic = topic.lower().strip()
        with self._lock:
            for item in self.database:
                if item.get("topic", "").lower().strip() == target_topic:
                    return item
        return None

    def remove(self, topic):
        target_topic = topic.lower().strip()
        with self._lock:
            before = len(self.database)
            self.database = [item for item in self.database if item.get("topic", "").lower().strip() != target_topic]
            if len(self.database) != before:
                self.save()
                return True
            return False

    def import_text(self, path):
        file_path = Path(path)
        if not file_path.exists():
            self._log_safe("error", f"Tentativa de importação inválida: {path} inexistente.")
            return False
        try:
            text = file_path.read_text(encoding="utf-8")
            self.add(topic=file_path.stem, information=text, source=str(file_path))
            return True
        except Exception as error:
            self._log_safe("error", f"Erro ao processar importação de documento: {error}")
            return False

    def total_entries(self):
        with self._lock:
            return len(self.database)

    def status(self):
        with self._lock:
            return {
                "name": self.name,
                "version": self.version,
                "entries": len(self.database),
                "file": str(self.file)
            }