"""
=========================================
GENESIS CORE

Arquivo:
core/mind/mind.py

Descrição:
Controlador superior da inteligência.

Responsável por integrar:
- Brain
- Pipeline Cognitiva
- Estado cognitivo
- Agentes

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from core.base.module import (
    Module,
    ModuleStatus
)


from core.mind.brain import (
    Brain
)



class Mind(Module):

    """
    Camada superior cognitiva.

    O Mind coordena.

    O Brain processa.

    A Pipeline executa o fluxo cognitivo.

    O Mind não possui inteligência própria.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None,
        engine=None,
        pipeline=None
    ):


        super().__init__(
            "core.mind.mind"
        )


        self.version = (
            "Genesis Core Mark III"
        )


        self.logger = logger

        self.event_bus = event_bus

        self.engine = engine

        self.pipeline = pipeline



        self.brain = Brain(
            logger=self.logger,
            event_bus=self.event_bus
        )



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
            f"[MIND] {message}"
        )



    # ==================================================
    # CICLO DE VIDA
    # ==================================================


    def initialize(
        self
    ):


        self.set_status(
            ModuleStatus.INITIALIZING
        )



        self.brain.connect(
            pipeline=self.pipeline
        )



        self.brain.initialize()



        self.set_status(
            ModuleStatus.ONLINE
        )



        self._log(
            "success",
            "Mind Cognitivo ONLINE."
        )



        return True



    def start(
        self
    ):

        return self.initialize()



    def shutdown(
        self
    ):


        self.brain.shutdown()



        self.set_status(
            ModuleStatus.OFFLINE
        )



        self._log(
            "info",
            "Mind desligado."
        )



        return True



    # ==================================================
    # COGNIÇÃO
    # ==================================================


    def think(
        self,
        message
    ):


        if self.get_status() != ModuleStatus.ONLINE:


            return {

                "error":
                "Mind offline."

            }



        return self.brain.process(
            message
        )



    # ==================================================
    # MEMÓRIA
    # ==================================================


    def remember(
        self,
        data,
        memory_type="general",
        importance=1
    ):


        return self.brain.remember(
            data,
            memory_type,
            importance
        )



    def recall(
        self,
        query
    ):


        return self.brain.recall(
            query
        )



    def forget(
        self
    ):


        return self.brain.state.memory.clear()



    # ==================================================
    # CONHECIMENTO
    # ==================================================


    def learn(
        self,
        topic,
        information,
        source="user",
        tags=None
    ):


        return self.brain.learn(
            topic,
            information,
            source,
            tags
        )



    def search(
        self,
        query
    ):


        return self.brain.search(
            query
        )



    # ==================================================
    # ESTADO
    # ==================================================


    def get_state(
        self
    ):


        return self.brain.state.snapshot()



    def reset(
        self
    ):


        return self.brain.reset()



    # ==================================================
    # DIAGNÓSTICO
    # ==================================================


    def status_report(
        self
    ):


        return {


            "name":
            self.name,


            "version":
            self.version,


            "status":
            self.get_status()
            .value,


            "brain":
            self.brain.get_brain_info(),


            "pipeline":
            self.pipeline is not None

        }