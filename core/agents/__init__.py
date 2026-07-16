"""
=========================================
JARVIS CORE

Pacote:
core.agents

Descrição:
Exposição centralizada dos agentes
inteligentes do Genesis Core.

Os agentes representam personalidades
ou entidades capazes de interagir com
o usuário utilizando a infraestrutura
cognitiva do sistema.

Arquitetura:

             Genesis Core

                  │
            Agent Manager
                  │
        ┌─────────┴─────────┐
        │                   │
     JARVIS             RAFIKI
        │                   │
        └─────────┬─────────┘
                  │
                Brain
                  │
        Cognitive Pipeline

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


# ==================================================
# AGENTES BASE
# ==================================================

from .agent import Agent


# ==================================================
# GERENCIADOR
# ==================================================

from .agent_manager import AgentManager


# ==================================================
# EXPORTAÇÃO PÚBLICA
# ==================================================

__all__ = [

    "Agent",

    "AgentManager",

]