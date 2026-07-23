"""
=========================================
GENESIS CORE

Pacote:
core.agents

Descrição:
Camada responsável pelo ecossistema
de agentes cognitivos do Genesis Core.

Responsável por:

- Classe base Agent
- Agentes cognitivos Genesis
- Criação dinâmica de agentes
- Gerenciamento do ciclo de vida

Arquitetura:

Kernel
   |
   ▼
AgentManager
   |
   ▼
AgentFactory
   |
   ▼
GenesisAgent
   |
   ▼
Persona


Mark:
V - Evolution
=========================================
"""


# ==================================================
# BASE
# ==================================================

from .agent import Agent



# ==================================================
# AGENTE COGNITIVO GENESIS
# ==================================================

from .genesis_agent import GenesisAgent



# ==================================================
# FACTORY
# ==================================================

from .agent_factory import AgentFactory



# ==================================================
# GERENCIAMENTO
# ==================================================

from .agent_manager import AgentManager



# ==================================================
# API PÚBLICA
# ==================================================

__all__ = [

    "Agent",

    "GenesisAgent",

    "AgentFactory",

    "AgentManager"

]