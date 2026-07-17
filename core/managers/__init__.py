"""
=========================================
GENESIS CORE

Pacote:
managers

Descrição:
Camada de gerenciamento estrutural
do Genesis Core.

Responsável por:

- Registro global de componentes
- Controle de serviços
- Gerenciamento de plugins
- Orquestração de ferramentas
- Integração entre módulos do sistema

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from .registry import Registry

from .service_manager import ServiceManager

from .plugin_manager import PluginManager

from .tool_manager import ToolManager



__version__ = "3.5"



__all__ = [

    "Registry",

    "ServiceManager",

    "PluginManager",

    "ToolManager"

]