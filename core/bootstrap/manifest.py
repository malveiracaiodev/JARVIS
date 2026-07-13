"""
=========================================
JARVIS GENESIS CORE

Arquivo:
manifest.py

Descrição:
Manifesto estrutural de componentes e serviços do JARVIS.
Define prioridades de boot e mapeamento de dependências.

Arquitetura:
Genesis Core

Mark:
III - Intelligence (Patch 3.1)

Autor:
Caio Vitor Malveira
=========================================
"""

# ==========================================================
# IMPORTS DAS ESPECIALIZAÇÕES DO CORE
# ==========================================================
from core.base.module import Module
# Nota: Adapte os caminhos reais de importação conforme sua árvore física de diretórios
from core.services.diagnostics import Diagnostics
from core.services.event_bus import EventBus
from core.services.config_manager import ConfigManager
from core.agents.agent_manager import AgentManager

# Simulação de placeholders para gerenciadores secundários se necessários
class Registry: pass
class Logger: pass
class Engine: pass
class Mind: pass

# ==========================================================
# COMPONENTES DO BOOT
# ==========================================================
BOOT_COMPONENTS = [
    {
        "name": "registry",
        "category": "module",
        "class": Registry,
        "priority": 0,
        "enabled": False, # Placeholder desligado por padrão até sua implementação
        "required": False,
        "constructor": [],
    },
    {
        "name": "logger",
        "category": "service",
        "class": Logger,
        "priority": 10,
        "enabled": False, # Exemplo desativado até escrita do logger unificado
        "required": False,
        "constructor": [],
    },
    {
        "name": "event_bus",
        "category": "service",
        "class": EventBus,
        "priority": 20,
        "enabled": True,
        "required": True,
        "constructor": ["logger"], # Será passado como kwargs se aceito, ou ignorado via fallback
    },
    {
        "name": "config",
        "category": "service",
        "class": ConfigManager,
        "priority": 30,
        "enabled": True,
        "required": True,
        "constructor": ["logger"],
    },
    {
        "name": "diagnostics",
        "category": "module",
        "class": Diagnostics,
        "priority": 35,
        "enabled": True,
        "required": True,
        "constructor": ["logger"],
    },
    {
        "name": "agent_manager",
        "category": "service",
        "class": AgentManager,
        "priority": 40,
        "enabled": True,
        "required": True,
        "constructor": ["logger"],
    }
]

# ==========================================================
# API
# ==========================================================
def get_boot_components():
    """Retorna os componentes estruturados e ordenados por prioridade estrita."""
    return sorted(
        [c for c in BOOT_COMPONENTS if c.get("enabled", True)],
        key=lambda component: component["priority"]
    )