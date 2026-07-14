"""
=========================================
JARVIS CORE

Pacote:
managers

Descrição:
Gerenciadores centrais do Genesis Core.

Responsáveis por controlar registros,
serviços, plugins e ferramentas do sistema.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from .registry import Registry

from .service_manager import ServiceManager

from .plugin_manager import PluginManager

from .tool_manager import ToolManager



__all__ = [

    "Registry",

    "ServiceManager",

    "PluginManager",

    "ToolManager"

]