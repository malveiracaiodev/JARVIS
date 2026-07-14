"""
=========================================
JARVIS CORE

Arquivo:
core/mind/brain.py

Descrição:
Orquestrador cognitivo central do Genesis Core.

Responsável por coordenar a inteligência,
memória, conhecimento e Pipeline Cognitiva.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime
from enum import Enum


from core.base.module import (
    Module,
    ModuleStatus
)


from core.interfaces.brain_interface import (
    BrainInterface
)



class BrainStatus(Enum):

    OFFLINE = "offline"

    INITIALIZING = "initializing"

    ONLINE = "online"

    THINKING = "thinking"

    ERROR = "error"



class Brain(
    Module,
    BrainInterface
):

    """
    Cérebro central do Genesis Core.

    O Brain coordena.

    Não executa ferramentas.
    Não gerencia serviços.
    Não controla infraestrutura.
    """



    def __init__(
        self,
        logger=None
    ):

        super().__init__(
            "core.mind.brain"
        )


        self.version = "Mark III - Cognitive Brain"


        self.logger = logger


        self.pipeline = None

        self.memory = None

        self.knowledge = None

        self.reasoning = None

        self.tools = None

        self.engine = None


        self.brain_status = BrainStatus.OFFLINE


        self.started_at = None



    # ==================================================
    # Logs
    # ==================================================


    def _log(
        self,
        level,
        message
    ):

        if self.logger:

            method = getattr(
                self.logger,
                level,
                None
            )

            if method:

                method(message)

                return


        print(
            f"[BRAIN] {message}"
        )



    # ==================================================
    # Conexões
    # ==================================================


    def connect(
        self,
        pipeline=None,
        memory=None,
        knowledge=None,
        reasoning=None,
        tools=None,
        engine=None
    ):


        if pipeline:

            self.pipeline = pipeline


        if memory:

            self.memory = memory


        if knowledge:

            self.knowledge = knowledge


        if reasoning:

            self.reasoning = reasoning


        if tools:

            self.tools = tools


        if engine:

            self.engine = engine



        self._log(
            "info",
            "Dependências cognitivas conectadas."
        )



    # ==================================================
    # Lifecycle
    # ==================================================


    def initialize(self):

        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.brain_status = BrainStatus.INITIALIZING


        self.started_at = datetime.now()


        self.brain_status = BrainStatus.ONLINE


        self.set_status(
            ModuleStatus.ONLINE
        )


        self._log(
            "success",
            "Brain Cognitivo ONLINE."
        )



    def shutdown(self):

        self.brain_status = BrainStatus.OFFLINE


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self._log(
            "info",
            "Brain desligado."
        )



    # ==================================================
    # Pensamento
    # ==================================================


    def process(
        self,
        input_data
    ):


        self.brain_status = BrainStatus.THINKING



        if not self.pipeline:

            self.brain_status = BrainStatus.ERROR


            return {

                "error":
                "Pipeline Cognitiva não conectada."

            }



        try:


            result = self.pipeline.process(
                input_data
            )


            self.brain_status = BrainStatus.ONLINE


            return result



        except Exception as error:


            self.brain_status = BrainStatus.ERROR


            self._log(
                "error",
                str(error)
            )


            return {

                "error": str(error)

            }



    # ==================================================
    # Informação
    # ==================================================


    def get_brain_info(
        self
    ):

        return {

            "status":
            self.brain_status.value,

            "version":
            self.version,

            "pipeline":
            self.pipeline is not None,

            "memory":
            self.memory is not None,

            "knowledge":
            self.knowledge is not None,

            "tools":
            self.tools is not None

        }