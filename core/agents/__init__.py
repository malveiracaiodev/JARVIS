"""
=========================================
GENESIS CORE

Arquivo:
core/agents/__init__.py

Descrição:
Inicializador e ponto de exportação do pacote
core.agents do Genesis Core (Mark IV).
=========================================
"""

from typing import List, Optional

# ==================================================
# CLASSE BASE DE AGENTES
# ==================================================
from .agent import Agent

# ==================================================
# AGENTE RAIZ GENESIS
# ==================================================
try:
    from .genesis_agent import GenesisAgent
except ImportError:
    GenesisAgent = None  # type: ignore

# ==================================================
# GERENCIADOR
# ==================================================
from .agent_manager import AgentManager

# ==================================================
# EXPORTAÇÃO PÚBLICA
# ==================================================
__all__: List[str] = [
    "Agent",
    "GenesisAgent",
    "AgentManager",
]