"""
=========================================
GENESIS CORE

Arquivo:
core/mind/brain.py

Descrição:
Orquestrador cognitivo central do Genesis Core.

Responsável por coordenar:
- Estado cognitivo
- Pipeline Cognitiva
- Memória de trabalho
- Histórico de processamento

Não executa ferramentas.
Não controla infraestrutura.
Não decide ações.

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


from core.mind.brain_state import (
    BrainState
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
    Núcleo cognitivo do Genesis Core.

    O Brain coordena:

    - Estado mental
    - Pipeline cognitiva
    - Histórico
    - Memória
    - Conhecimento

    O Brain não executa ações externas.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None
    ):


        super().__init__(
            "core.mind.brain"
        )


        self.version = (
            "Genesis Core Mark III"
        )


        self.logger = logger

        self.event_bus = event_bus



        # Estado cognitivo central

        self.state = BrainState(
            logger=self.logger
        )



        # Pipeline Cognitiva

        self.pipeline = None



        # Estado interno do Brain

        self._brain_status = (
            BrainStatus.OFFLINE
        )



        self.started_at = None

        self.cycles = 0

        self.errors = 0



    # ==================================================
    # ESTADO COGNITIVO
    # ==================================================

    def get_brain_status(
        self
    ):

        return self._brain_status



    # ==================================================
    # LOG
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


            if callable(method):

                method(
                    message
                )

                return



        print(
            f"[BRAIN] {message}"
        )



    # ==================================================
    # CONEXÕES
    # ==================================================

    def connect(
        self,
        pipeline=None,
        reasoner=None
    ):


        if pipeline:

            self.pipeline = pipeline



        self._log(
            "info",
            "Componentes cognitivos conectados."
        )



    # ==================================================
    # CICLO DE VIDA
    # ==================================================

    def initialize(
        self
    ):


        self._brain_status = (
            BrainStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.INITIALIZING
        )



        self.state.initialize()



        self.started_at = datetime.now()



        self._brain_status = (
            BrainStatus.ONLINE
        )


        self.set_status(
            ModuleStatus.ONLINE
        )



        self._log(
            "success",
            "Brain Cognitivo ONLINE."
        )



        return True



    def shutdown(
        self
    ):


        self.state.shutdown()



        self._brain_status = (
            BrainStatus.OFFLINE
        )


        self.set_status(
            ModuleStatus.OFFLINE
        )



        self._log(
            "info",
            "Brain desligado."
        )



        return True



    # ==================================================
    # PROCESSAMENTO COGNITIVO
    # ==================================================

    def process(
        self,
        input_data
    ):


        if not self.pipeline:


            self.errors += 1


            self._brain_status = (
                BrainStatus.ERROR
            )



            return {

                "error":
                "Pipeline Cognitiva não conectada."

            }



        try:


            self._brain_status = (
                BrainStatus.THINKING
            )



            self.state.context.set_last_message(
                input_data
            )



            result = self.pipeline.process(
                input_data
            )



            self.cycles += 1



            self.state.add_history(
                {

                    "timestamp":
                    datetime.now()
                    .isoformat(),


                    "input":
                    input_data,


                    "result":
                    result

                }
            )



            self._brain_status = (
                BrainStatus.ONLINE
            )



            return result



        except Exception as error:


            self.errors += 1


            self._brain_status = (
                BrainStatus.ERROR
            )



            self._log(
                "error",
                str(error)
            )



            return {

                "error":
                str(error)

            }



    # ==================================================
    # MEMÓRIA
    # ==================================================

    def remember(
        self,
        data,
        memory_type="general",
        importance=1
    ):


        return self.state.memory.store(
            data,
            memory_type,
            importance
        )



    def recall(
        self,
        query
    ):


        return self.state.memory.retrieve(
            query
        )



    # ==================================================
    # CONHECIMENTO
    # ==================================================

    def learn(
        self,
        topic,
        information,
        source="internal",
        tags=None
    ):


        return self.state.knowledge.add(
            topic,
            information,
            source,
            tags
        )



    def search(
        self,
        query
    ):


        return self.state.knowledge.search(
            query
        )



    # ==================================================
    # RESET
    # ==================================================

    def reset(
        self
    ):


        if self.get_status() != ModuleStatus.ONLINE:

            return False



        self.state.context.clear_temporary()



        return True



    # ==================================================
    # INFORMAÇÕES
    # ==================================================

    def get_brain_info(
        self
    ):


        return {


            "name":
            self.name,


            "version":
            self.version,


            "status":
            self._brain_status.value,


            "module_status":
            self.get_status().value,


            "pipeline":
            self.pipeline is not None,


            "cycles":
            self.cycles,


            "errors":
            self.errors,


            "state":
            self.state.snapshot()

        }