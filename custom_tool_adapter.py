"""
=========================================
GENESIS CORE

Arquivo:
custom_tool_adapter.py

Descrição:
Adaptador atualizado para satisfazer todos os 
métodos abstratos exigidos pela ToolInterface 
da Neural Lattice (Mark IV).

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

from core.interfaces.tool_interface import ToolInterface
from core.runtime.component_state import ComponentState

class CustomToolAdapter(ToolInterface):
    """
    Adaptador para transformar funções simples do Python em Tools 
    compatíveis com a Neural Lattice (Mark IV).
    """
    def __init__(self, tool_name, func, description=""):
        self._name = tool_name
        self._func = func
        self._description = description
        self.version = "1.0"
        self._status = ComponentState.ONLINE

    def name(self) -> str:
        return self._name

    def description(self) -> str:
        return self._description

    def permissions(self) -> list:
        return ["execute"]

    def status(self):
        return self._status

    def validate(self, action) -> bool:
        if isinstance(action, dict):
            return action.get("tool") == self._name or self._name in action.get("command", "")
        if isinstance(action, str):
            return self._name in action
        return False

    def execute(self, action, context=None):
        if isinstance(action, dict):
            params = action.get("params", action)
        else:
            params = {"input": action}
        
        return self._func(params)