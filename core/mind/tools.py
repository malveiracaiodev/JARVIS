"""
=========================================
GENESIS CORE - SYSTEM TOOLS REGISTRY

Arquivo: core/mind/tools.py
Descrição: Orquestrador de capacidades e chamadas dinâmicas.
Mark: IV - Thought Engine
=========================================
"""

import json
import threading
import urllib.request
import urllib.parse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Callable
from core.base.module import Module, ModuleStatus

class Tools(Module):
    """
    Gerenciador thread-safe e dinâmico de ferramentas nativas e estendidas.
    """

    def __init__(self):
        super().__init__("core.mind.tools")
        self.version = "Mark IV"
        self.tools: Dict[str, Callable] = {}
        self._lock = threading.RLock()

    def initialize(self) -> bool:
        self.set_status(ModuleStatus.INITIALIZING)
        with self._lock:
            self.register("web_search", self._tool_web_search)
            self.register("create_persona", self._tool_create_persona)
            self.register("create_plugin", self._tool_create_plugin)
        self.set_status(ModuleStatus.ONLINE)
        self._log_safe("success", "Gerenciador de ferramentas e capacidades ativado.")
        return True

    def shutdown(self) -> bool:
        with self._lock:
            self.tools.clear()
        self.set_status(ModuleStatus.OFFLINE)
        return True

    def _log_safe(self, level: str, message: str) -> None:
        if hasattr(self, "logger") and self.logger:
            log_method = getattr(self.logger, level, None)
            if log_method and callable(log_method):
                log_method(f"[{self.name}] {message}")
                return
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{level.upper()}] {message}")

    def register(self, name: str, function: Callable) -> None:
        with self._lock:
            self.tools[name.lower().strip()] = function
            self._log_safe("info", f"Capacidade unificada: '{name}'")

    def execute(self, name: str, *args, **kwargs) -> Any:
        name_key = name.lower().strip()
        with self._lock:
            tool = self.tools.get(name_key)
        if not tool:
            return f"Erro: Capacidade operacional '{name}' indisponível."
        try:
            return tool(*args, **kwargs)
        except Exception as error:
            self._log_safe("error", f"Falha na execução de '{name}': {error}")
            return f"Falha na execução de '{name}': {str(error)}"

    def available(self) -> List[str]:
        with self._lock:
            return list(self.tools.keys())

    def remove(self, name: str) -> bool:
        name_key = name.lower().strip()
        with self._lock:
            if name_key in self.tools:
                del self.tools[name_key]
                return True
        return False

    def _tool_web_search(self, query: str) -> str:
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
            snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
            results = [f"[{i+1}] {re.sub(r'<[^>]*>', '', s).strip()}" for i, s in enumerate(snippets[:3])]
            return "\n".join(results) if results else "Sem dados diretos na busca."
        except Exception as e:
            return f"Erro de busca: {str(e)}"

    def _tool_create_persona(self, name: str, behavior: str, goal: str) -> str:
        try:
            folder = Path("personas")
            folder.mkdir(exist_ok=True)
            p_data = {"name": name, "behavior": behavior, "goal": goal, "created_at": datetime.now().isoformat()}
            with open(folder / f"{name.lower().strip()}.json", "w", encoding="utf-8") as f:
                json.dump(p_data, f, indent=4, ensure_ascii=False)
            return f"Sucesso: Persona '{name}' injetada e guardada em disco."
        except Exception as e:
            return f"Erro ao gerar persona: {str(e)}"

    def _tool_create_plugin(self, plugin_name: str, code: str) -> str:
        try:
            folder = Path("plugins")
            folder.mkdir(exist_ok=True)
            f_name = f"{plugin_name.lower().strip().replace(' ', '_')}.py"
            with open(folder / f_name, "w", encoding="utf-8") as f:
                f.write(code)
            return f"Sucesso: Extensão de capacidade '{plugin_name}' compilada."
        except Exception as e:
            return f"Erro ao criar funcionalidade: {str(e)}"