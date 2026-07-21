"""
=========================================
GENESIS CORE - TOOL LAYER REGISTRY

Arquivo: core/tools/__init__.py
Descrição: Centralização e exportação da camada de ferramentas executáveis.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from core.interfaces.tool_interface import ToolInterface
from core.tools.system_test_tool import SystemTestTool

__all__ = [
    "ToolInterface",
    "SystemTestTool"
]