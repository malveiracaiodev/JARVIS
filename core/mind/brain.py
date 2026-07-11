"""
=========================================
JARVIS CORE

Arquivo:
brain.py

Descrição:
Núcleo de inteligência do sistema.

Responsável por:
- Coordenar pensamento
- Integrar memória
- Consultar conhecimento
- Utilizar ferramentas
- Executar raciocínio

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from enum import Enum


class BrainStatus(Enum):
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    ONLINE = "online"
    THINKING = "thinking"
    ERROR = "error"


class Brain:
    """
    Cérebro central do JARVIS.

    O Brain não possui inteligência própria.

    Ele apenas coordena todos os sistemas
    cognitivos do Mind.
    """

    def __init__(self):

        self.name = "JARVIS Brain"

        self.version = "Mark II"

        self.status = BrainStatus.OFFLINE

        self.memory = None

        self.knowledge = None

        self.reasoning = None

        self.tools = None

        self.logger = None

        self.started_at = None

    # ==========================================================
    # Conexões
    # ==========================================================

    def connect(
        self,
        memory=None,
        knowledge=None,
        reasoning=None,
        tools=None,
        logger=None
    ):

        if memory is not None:
            self.memory = memory
            self._log("[BRAIN] Memory conectado")

        if knowledge is not None:
            self.knowledge = knowledge
            self._log("[BRAIN] Knowledge conectado")

        if reasoning is not None:
            self.reasoning = reasoning
            self._log("[BRAIN] Reasoning conectado")

        if tools is not None:
            self.tools = tools
            self._log("[BRAIN] Tools conectado")

        if logger is not None:
            self.logger = logger

    # ==========================================================
    # Ciclo de vida
    # ==========================================================

    def initialize(self):

        self.status = BrainStatus.INITIALIZING

        self.started_at = datetime.now()

        self.status = BrainStatus.ONLINE

        self._log("[BRAIN] Inteligência iniciada")

    def start(self):
        self.initialize()

    def shutdown(self):

        self.status = BrainStatus.OFFLINE

        self._log("[BRAIN] Inteligência encerrada")

    # ==========================================================
    # Processamento
    # ==========================================================

    def process(
        self,
        input_text
    ):

        self.status = BrainStatus.THINKING

        context = {
            "memory": None,
            "knowledge": None,
            "tools": None
        }

        # -----------------------------
        # Memória
        # -----------------------------

        if self.memory:

            try:

                context["memory"] = self.memory.retrieve(
                    input_text
                )

            except Exception as error:

                self._log(
                    f"[BRAIN] Erro Memory: {error}"
                )

        # -----------------------------
        # Conhecimento
        # -----------------------------

        if self.knowledge:

            try:

                if hasattr(self.knowledge, "search"):

                    context["knowledge"] = (
                        self.knowledge.search(
                            input_text
                        )
                    )

            except Exception as error:

                self._log(
                    f"[BRAIN] Erro Knowledge: {error}"
                )

        # -----------------------------
        # Ferramentas
        # -----------------------------

        if self.tools:

            try:

                if hasattr(self.tools, "available"):

                    context["tools"] = (
                        self.tools.available()
                    )

            except Exception as error:

                self._log(
                    f"[BRAIN] Erro Tools: {error}"
                )

        # -----------------------------
        # Raciocínio
        # -----------------------------

        if self.reasoning:

            try:

                result = self.reasoning.analyze(
                    input_text,
                    context
                )

            except Exception as error:

                self.status = BrainStatus.ERROR

                return (
                    f"Erro durante o raciocínio: {error}"
                )

        else:

            result = (
                "Processando informação: "
                + input_text
            )

        # -----------------------------
        # Armazenamento
        # -----------------------------

        if self.memory:

            try:

                self.memory.store({

                    "input": input_text,

                    "response": result,

                    "context": context,

                    "timestamp": datetime.now().isoformat()

                })

            except Exception as error:

                self._log(
                    f"[BRAIN] Falha ao armazenar memória: {error}"
                )

        self.status = BrainStatus.ONLINE

        return result

    # ==========================================================
    # Diagnóstico
    # ==========================================================

    def info(self):

        return {

            "name": self.name,

            "version": self.version,

            "status": self.status.value,

            "started_at": (
                self.started_at.isoformat()
                if self.started_at
                else None
            ),

            "memory": self.memory is not None,

            "knowledge": self.knowledge is not None,

            "reasoning": self.reasoning is not None,

            "tools": self.tools is not None

        }

    # ==========================================================
    # Logger interno
    # ==========================================================

    def _log(
        self,
        message
    ):

        if self.logger:

            self.logger.info(message)

        else:

            print(message)