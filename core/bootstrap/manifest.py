"""
=========================================
GENESIS CORE

Arquivo:
core/bootstrap/manifest.py

Descrição:
Mapa estrutural de inicialização do Genesis.

Responsável por:

- Definir componentes
- Ordem de boot
- Dependências
- Categorias
- Prioridades
- Construção do ecossistema

Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from typing import Any, Dict, List


# ======================================================
# SERVIÇOS
# ======================================================

from core.services.logger import Logger
from core.services.config_manager import ConfigManager
from core.services.event_bus import EventBus
from core.services.diagnostics import Diagnostics
from core.services.ai_service import AIService


# ======================================================
# GERENCIADORES
# ======================================================

from core.managers.registry import Registry
from core.agents.agent_manager import AgentManager



# ======================================================
# BOOT MANIFEST
# ======================================================

BOOT_COMPONENTS: List[Dict[str, Any]] = [


    # ==================================================
    # FUNDAMENTAÇÃO DO SISTEMA
    # ==================================================

    {
        "name": "logger",
        "category": "service",
        "class": Logger,
        "priority": 0,
        "enabled": True,
        "required": True,
        "constructor": []
    },


    {
        "name": "config",
        "category": "service",
        "class": ConfigManager,
        "priority": 10,
        "enabled": True,
        "required": True,
        "constructor": [
            "logger"
        ]
    },


    {
        "name": "event_bus",
        "category": "service",
        "class": EventBus,
        "priority": 20,
        "enabled": True,
        "required": True,
        "constructor": [
            "logger"
        ]
    },



    # ==================================================
    # REGISTRO GLOBAL
    # ==================================================

    {
        "name": "registry",
        "category": "manager",
        "class": Registry,
        "priority": 30,
        "enabled": True,
        "required": True,
        "constructor": [
            "logger"
        ]
    },



    # ==================================================
    # SISTEMA
    # ==================================================

    {
        "name": "diagnostics",
        "category": "system",
        "class": Diagnostics,
        "priority": 40,
        "enabled": True,
        "required": True,
        "constructor": [
            "logger"
        ]
    },



    # ==================================================
    # INTELIGÊNCIA ARTIFICIAL
    # ==================================================

    {
        "name": "ai_service",
        "category": "service",
        "class": AIService,
        "priority": 45,
        "enabled": True,
        "required": True,
        "constructor": []
    },



    # ==================================================
    # AGENTES COGNITIVOS
    # ==================================================

    {
        "name": "agent_manager",
        "category": "manager",
        "class": AgentManager,
        "priority": 50,
        "enabled": True,
        "required": True,
        "constructor": [
            "logger",
            "event_bus"
        ]
    }

]



# ======================================================
# API
# ======================================================

def get_boot_components() -> List[Dict[str, Any]]:
    """
    Retorna componentes ativos
    ordenados pela prioridade.
    """

    return sorted(
        [
            component
            for component in BOOT_COMPONENTS
            if component.get(
                "enabled",
                True
            )
        ],
        key=lambda component:
            component["priority"]
    )