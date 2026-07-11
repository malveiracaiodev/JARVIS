"""
=========================================
JARVIS CORE

Arquivo:
mind.py

Descrição:
Controlador principal da inteligência.

Responsável por:
- Integrar módulos cognitivos
- Gerenciar pensamento
- Coordenar o Brain
- Expor API cognitiva ao sistema

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from core.mind.brain import Brain
from core.mind.memory import Memory
from core.mind.knowledge import Knowledge
from core.mind.reasoning import Reasoning
from core.mind.tools import Tools


class Mind:
    """
    Sistema cognitivo completo do JARVIS.

    O Mind monta todos os módulos
    cognitivos e entrega uma interface
    única para os agentes.
    """

    def __init__(self):

        self.name = "Mind"

        self.version = "Mark II"

        self.status = "created"

        self.brain = Brain()

        self.memory = Memory()

        self.knowledge = Knowledge()

        self.reasoning = Reasoning()

        self.tools = Tools()

    # ==========================================================
    # Ciclo de vida
    # ==========================================================

    def initialize(self):

        self.memory.initialize()

        self.knowledge.initialize()

        if hasattr(self.reasoning, "initialize"):
            self.reasoning.initialize()

        if hasattr(self.tools, "initialize"):
            self.tools.initialize()

        self.brain.connect(

            memory=self.memory,

            knowledge=self.knowledge,

            reasoning=self.reasoning,

            tools=self.tools

        )

        self.brain.initialize()

        self.status = "online"

        print("[MIND] Sistema cognitivo ONLINE")

    def start(self):
        self.initialize()

    def shutdown(self):

        self.brain.shutdown()

        self.memory.shutdown()

        self.knowledge.shutdown()

        if hasattr(self.reasoning, "shutdown"):
            self.reasoning.shutdown()

        if hasattr(self.tools, "shutdown"):
            self.tools.shutdown()

        self.status = "offline"

        print("[MIND] Sistema cognitivo OFFLINE")

    # ==========================================================
    # Cognição
    # ==========================================================

    def think(
        self,
        message
    ):

        if self.status != "online":

            return "Minha mente ainda não foi iniciada."

        return self.brain.process(message)

    # ==========================================================
    # Aprendizado
    # ==========================================================

    def learn(
        self,
        topic,
        information,
        source="user",
        tags=None
    ):

        return self.knowledge.add(

            topic=topic,

            information=information,

            source=source,

            tags=tags

        )

    # ==========================================================
    # Memória
    # ==========================================================

    def remember(
        self,
        data
    ):

        return self.memory.store(data)

    def recall(
        self,
        query
    ):

        return self.memory.retrieve(query)

    def forget(
        self
    ):

        self.memory.clear()

    # ==========================================================
    # Conhecimento
    # ==========================================================

    def search(
        self,
        query
    ):

        return self.knowledge.search(query)

    # ==========================================================
    # Diagnóstico
    # ==========================================================

    def status_report(self):

        return {

            "name": self.name,

            "version": self.version,

            "status": self.status,

            "brain": self.brain.info(),

            "memory": self.memory.status(),

            "knowledge": self.knowledge.status(),

            "reasoning": (

                len(self.reasoning.history)

                if hasattr(self.reasoning, "history")

                else 0

            ),

            "tools": (

                self.tools.available()

                if hasattr(self.tools, "available")

                else []

            )

        }