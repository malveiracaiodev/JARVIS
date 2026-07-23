"""
=========================================
GENESIS CORE

Pacote:
core.managers

Descrição:
Camada de gerenciamento central do
Genesis Core.

Responsável por:

- Registro global de componentes
- Controle de serviços
- Gerenciamento de plugins
- Orquestração de ferramentas
- Controle da inteligência artificial
- Integração entre módulos da Neural Lattice

Arquitetura:

Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from .registry import Registry

from .service_manager import ServiceManager

from .plugin_manager import PluginManager

from .tool_manager import ToolManager

from .ai_manager import AIManager



__version__ = "5.0-Evolution"



__all__ = [

    "Registry",

    "ServiceManager",

    "PluginManager",

    "ToolManager",

    "AIManager"

]