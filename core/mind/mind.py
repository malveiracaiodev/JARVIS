"""
=========================================
JARVIS CORE

Arquivo:
core/mind/mind.py

Descrição:
Controlador principal da inteligência.
Integrador de submódulos cognitivos e roteamento de mensagens.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from core.base.module import Module, ModuleStatus
from core.mind.brain import Brain
from core.mind.memory import Memory
from core.mind.knowledge import Knowledge
from core.mind.reasoning import Reasoning
from core.mind.tools import Tools


class Mind(Module):
    """
    Sistema cognitivo completo do JARVIS Mark III.
    """

    def __init__(self, logger=None, event_bus=None, engine=None):
        super().__init__("core.mind.mind")
        self.version = "Mark III"
        
        self.logger = logger
        self.event_bus = event_bus
        self.engine = engine

        # Instancia os submódulos cognitivos
        self.brain = Brain(logger=self.logger, event_bus=self.event_bus)
        self.memory = Memory()
        self.knowledge = Knowledge()
        self.reasoning = Reasoning()
        self.tools = Tools()

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)

        # Injeta os loggers para os subsistemas de forma segura
        self.memory.logger = self.logger
        self.knowledge.logger = self.logger
        self.reasoning.logger = self.logger
        self.tools.logger = self.logger

        # Inicializa submódulos de forma limpa e blindada
        self.memory.initialize()
        self.knowledge.initialize()
        
        if hasattr(self.reasoning, "initialize"):
            self.reasoning.initialize()

        if hasattr(self.tools, "initialize"):
            self.tools.initialize()

        # Conecta dependências ao cérebro (JARVIS Core)
        self.brain.connect(
            memory=self.memory,
            knowledge=self.knowledge,
            reasoning=self.reasoning,
            tools=self.tools,
            engine=self.engine
        )

        self.brain.initialize()

        self.set_status(ModuleStatus.ONLINE)
        if self.logger:
            self.logger.success("Sistema cognitivo integrado e ONLINE.")

    def start(self):
        self.initialize()

    def shutdown(self):
        self.set_status(ModuleStatus.OFFLINE)

        # Desliga de forma limpa cada subsistema cognitivo
        for submodule_name in ["brain", "memory", "knowledge", "reasoning", "tools"]:
            submodule = getattr(self, submodule_name, None)
            if submodule and hasattr(submodule, "shutdown"):
                submodule.shutdown()

        if self.logger:
            self.logger.info("Sistema cognitivo desativado com segurança.")

    def think(self, message):
        if self.get_status() != ModuleStatus.ONLINE:
            return "Minha mente ainda não foi completamente iniciada pelo Kernel."
        return self.brain.process(message)

    def learn(self, topic, information, source="user", tags=None):
        if hasattr(self.knowledge, "add"):
            return self.knowledge.add(topic=topic, information=information, source=source, tags=tags)

    def remember(self, data):
        if hasattr(self.memory, "store"):
            return self.memory.store(data)

    def recall(self, query):
        if hasattr(self.memory, "retrieve"):
            return self.memory.retrieve(query)

    def forget(self):
        if hasattr(self.memory, "clear"):
            self.memory.clear()

    def search(self, query):
        if hasattr(self.knowledge, "search"):
            return self.knowledge.search(query)

    def status_report(self):
        brain_info = {}
        if hasattr(self.brain, "get_brain_info"):
            brain_info = self.brain.get_brain_info()
            
        return {
            "name": self.name,
            "version": self.version,
            "status": self.get_status().value,
            "brain": brain_info,
            "tools": self.tools.available() if hasattr(self.tools, "available") else [],
            "async_engine_bound": self.engine is not None
        }