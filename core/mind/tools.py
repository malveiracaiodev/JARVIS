"""
=========================================
JARVIS CORE

Arquivo:
tools.py

Descrição:
Orquestrador de execução de capacidades e chamadas de funções dinâmicas do sistema.

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
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime
from core.base.module import Module, ModuleStatus


class Tools(Module):
    """
    Gerenciador thread-safe e dinâmico de ferramentas do JARVIS.
    """

    def __init__(self):
        super().__init__("core.mind.tools")
        self.version = "3.1"
        self.tools = {}
        self._lock = threading.RLock()

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        
        # Registrar ferramentas internas do sistema para autocriação e pesquisa
        self.register("web_search", self._tool_web_search)
        self.register("create_persona", self._tool_create_persona)
        self.register("create_plugin", self._tool_create_plugin)

        self.set_status(ModuleStatus.ONLINE)
        self._log_safe("success", "Gerenciador de ferramentas e automodificação ativo.")

    def shutdown(self):
        with self._lock:
            self.tools.clear()
        self.set_status(ModuleStatus.OFFLINE)
        self._log_safe("info", "Registro de capacidades descarregado.")

    def _log_safe(self, level, message):
        """Garante entrega de log de inicialização e parada sem colisões de atributos."""
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

    def register(self, name, function):
        name_key = name.lower().strip()
        with self._lock:
            self.tools[name_key] = function
            self._log_safe("info", f"Capacidade do sistema mapeada: '{name}'")

    def execute(self, name, *args, **kwargs):
        name_key = name.lower().strip()
        with self._lock:
            tool = self.tools.get(name_key)

        if not tool:
            return f"Erro: Ferramenta operacional '{name}' não encontrada ou inativa."

        try:
            return tool(*args, **kwargs)
        except Exception as error:
            self._log_safe("error", f"Exceção interna executando capacidade '{name}': {error}")
            return f"Falha de execução na ferramenta '{name}': {str(error)}"

    def available(self):
        with self._lock:
            return list(self.tools.keys())

    def remove(self, name):
        name_key = name.lower().strip()
        with self._lock:
            if name_key in self.tools:
                del self.tools[name_key]
                self._log_safe("info", f"Capacidade '{name}' removida.")
                return True
            return False

    # ==========================================================
    # Ferramentas Nativas
    # ==========================================================

    def _tool_web_search(self, query: str) -> str:
        self._log_safe("info", f"Pesquisando na Web por: '{query}'")
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
            
            import re
            snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
            results = []
            for i, snippet in enumerate(snippets[:3]):
                clean_text = re.sub(r'<[^>]*>', '', snippet).strip()
                results.append(f"[{i+1}] {clean_text}")
                
            if not results:
                return "A busca web não obteve dados legíveis diretos."
                
            return "\n".join(results)
            
        except Exception as e:
            self._log_safe("error", f"Erro ao pesquisar na web: {e}")
            return f"Não foi possível pesquisar na web: {str(e)}"

    def _tool_create_persona(self, name: str, behavior: str, goal: str) -> str:
        self._log_safe("info", f"Salvando nova persona em disco: {name}")
        try:
            folder = Path("personas")
            folder.mkdir(exist_ok=True)
            
            persona_data = {
                "name": name,
                "behavior": behavior,
                "goal": goal,
                "created_at": datetime.now().isoformat()
            }
            
            file_path = folder / f"{name.lower().strip()}.json"
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(persona_data, file, indent=4, ensure_ascii=False)
                
            return f"Sucesso: Personalidade '{name}' registrada e guardada."
        except Exception as e:
            self._log_safe("error", f"Erro ao criar personalidade: {e}")
            return f"Erro ao gerar nova persona: {str(e)}"

    def _tool_create_plugin(self, plugin_name: str, code: str) -> str:
        self._log_safe("info", f"Instalando plugin fisicamente: {plugin_name}")
        try:
            folder = Path("plugins")
            folder.mkdir(exist_ok=True)
            
            file_name = f"{plugin_name.lower().strip().replace(' ', '_')}.py"
            file_path = folder / file_name
            
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(code)
                
            return f"Sucesso: Plugin '{plugin_name}' instalado com sucesso."
        except Exception as e:
            self._log_safe("error", f"Erro ao salvar plugin: {e}")
            return f"Erro ao criar funcionalidade: {str(e)}"