"""
Gerenciador de agentes.
"""

from core.base.module import Module, ModuleStatus


class AgentManager(Module):

    def __init__(self, logger):

        super().__init__("Agent Manager")

        self.logger = logger

        self.agents = {}

    def initialize(self):

        self.set_status(ModuleStatus.ONLINE)

        self.logger.success("Agent Manager iniciado")

    def shutdown(self):

        self.agents.clear()

        self.set_status(ModuleStatus.OFFLINE)

        self.logger.info("Agent Manager encerrado")

    def register(self, agent):

        self.agents[agent.name.lower()] = agent

    def get(self, name):

        return self.agents.get(name.lower())

    def list_agents(self):

        return list(self.agents.keys())