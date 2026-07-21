"""
=========================================
GENESIS CORE

Pacote:
managers

Descrição:
Camada de gerenciamento estrutural
do Genesis Core (Mark IV - Neural Lattice).

Responsável por:

- Registro global de componentes (Registry)
- Controle de serviços (ServiceManager)
- Gerenciamento de plugins (PluginManager)
- Orquestração de ferramentas (ToolManager)
- Integração de estados entre módulos na Lattice

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

from .registry import Registry
from .service_manager import ServiceManager
from .plugin_manager import PluginManager
from .tool_manager import ToolManager

__version__ = "4.0-Lattice"

__all__ = [
    "Registry",
    "ServiceManager",
    "PluginManager",
    "ToolManager"
]