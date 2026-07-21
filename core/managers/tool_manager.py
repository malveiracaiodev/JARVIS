"""
=========================================
GENESIS CORE

Arquivo:
core/managers/tool_manager.py

Descrição:
Gerenciador central das ferramentas executáveis 
do Genesis Core (Mark IV - Neural Lattice).

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from core.base.module import Module, ModuleStatus
from core.interfaces.tool_interface import ToolInterface
from core.runtime.component_state import ComponentState

class ToolManager(Module):
    """
    Núcleo de capacidades executáveis otimizado para o padrão Mark IV.
    """

    def __init__(self, logger=None, registry=None):
        super().__init__("core.tool_manager")
        self.version = "4.0-Lattice"
        self.logger = logger
        self.registry = registry
        self._tools = {}
        self._lock = threading.RLock()

    # ==================================================
    # CICLO DE VIDA
    # ==================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        self.set_status(ModuleStatus.ONLINE)
        self.log_success("Tool Manager Mark IV (Neural Lattice) ONLINE.")

    def shutdown(self):
        self.clear()
        self.set_status(ModuleStatus.OFFLINE)
        self.log_info("Tool Manager encerrado.")

    # ==================================================
    # REGISTRO
    # ==================================================

    def register(self, tool):
        if not isinstance(tool, ToolInterface):
            raise TypeError("Tool precisa implementar ToolInterface.")

        name = tool.name()
        if not name:
            raise ValueError("Tool sem nome.")

        with self._lock:
            if name in self._tools:
                self.log_info(f"Tool já registrada na Lattice: {name}")
                return False

            self._tools[name] = {
                "object": tool,
                "version": getattr(tool, "version", "1.0"),
                "status": ComponentState.ONLINE
            }

        if self.registry:
            try:
                self.registry.register_capability(name, tool)
            except Exception as error:
                self.log_error(f"Erro ao registrar capability no Registry: {error}")

        self.log_info(f"Tool integrada ao Lattice: {name}")
        return True

    def unregister(self, name):
        with self._lock:
            data = self._tools.pop(name, None)

        if data:
            if self.registry:
                try:
                    self.registry.unregister(name)
                except Exception as error:
                    self.log_error(f"Erro ao desregistrar do Registry: {error}")
            self.log_info(f"Tool removida da Lattice: {name}")
            return True
        return False

    def clear(self):
        with self._lock:
            names = list(self._tools.keys())
        for name in names:
            self.unregister(name)

    # ==================================================
    # EXECUÇÃO E BUSCA
    # ==================================================

    def find(self, action):
        with self._lock:
            tools = [data["object"] for data in self._tools.values()]
        for tool in tools:
            try:
                if tool.validate(action):
                    return tool
            except Exception as error:
                self.log_error(f"Erro validando tool {tool.name()}: {error}")
        return None

    def execute(self, action, context=None):
        if not action:
            return {"success": False, "message": "Ação vazia."}

        tool = self.find(action)
        if not tool:
            return {"success": False, "message": "Nenhuma Tool encontrada na Lattice."}

        with self._lock:
            tool_data = self._tools.get(tool.name())
            if tool_data and tool_data["status"] == ComponentState.ISOLATED:
                return {"success": False, "error": f"Tool {tool.name()} está isolada."}

        try:
            result = tool.execute(action, context)
            return {"success": True, "tool": tool.name(), "result": result}
        except Exception as error:
            self.log_error(f"Falha executando tool {tool.name()}: {error}")
            with self._lock:
                if tool.name() in self._tools:
                    self._tools[tool.name()]["status"] = ComponentState.DEGRADED
            return {"success": False, "error": str(error)}

    # ==================================================
    # LOGGING (Helpers)
    # ==================================================

    def log_info(self, msg):
        if self.logger: self.logger.info(msg)

    def log_success(self, msg):
        if self.logger:
            if hasattr(self.logger, "success"): self.logger.success(msg)
            else: self.logger.info(msg)

    def log_error(self, msg):
        if self.logger: self.logger.error(msg)