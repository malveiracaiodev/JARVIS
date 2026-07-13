"""
=========================================
JARVIS CORE

Arquivo:
agent_manager.py

Descrição:
Gerenciador central de agentes do ecossistema.

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.6)
=========================================
"""

import threading
from core.base.module import Module, ModuleStatus


class AgentManager(Module):
    """
    Módulo de registro, ciclo de vida e roteamento de agentes cognitivos.
    """

    def __init__(self, logger=None):
        super().__init__("core.agent_manager")
        self.version = "2.2"
        self.logger = logger
        self.agents = {}
        self._lock = threading.RLock()

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        with self._lock:
            self.agents.clear()
        self.set_status(ModuleStatus.ONLINE)
        self.success("Agent Manager inicializado em modo concorrente seguro")

    def shutdown(self):
        with self._lock:
            # Desliga cada agente de forma individual e limpa o dicionário
            for agent in self.agents.values():
                try:
                    agent.stop()
                except Exception:
                    pass
            self.agents.clear()
        self.set_status(ModuleStatus.OFFLINE)
        self.info("Agent Manager encerrado com sucesso")

    def register(self, agent):
        if not hasattr(agent, "name"):
            self.error("Falha ao registrar: Objeto não possui atributo 'name'")
            return False
            
        with self._lock:
            key = agent.name.lower()
            self.agents[key] = agent
            self.info(f"Agente registrado com sucesso: {agent.name}")
            return True

    def get(self, name):
        with self._lock:
            return self.agents.get(name.lower())

    def list_agents(self):
        with self._lock:
            return list(self.agents.keys())

    # ==========================================================
    # LOGS REDIRECIONADOS
    # ==========================================================

    def info(self, message):
        if self.logger: self.logger.info(message)

    def success(self, message):
        if self.logger: self.logger.success(message)

    def error(self, message):
        if self.logger: self.logger.error(message)