"""
=========================================
JARVIS CORE

Arquivo:
core/pipeline/pipeline_initializer.py

Descrição:
Inicializador da Pipeline Cognitiva
do Genesis Core.

Responsável por construir e registrar
as etapas cognitivas do sistema.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from core.pipeline.cognitive_pipeline import CognitivePipeline


from core.cognitive import (

    Parser,

    Planner,

    Reasoner,

    Executor,

    Reflection

)


from core.tools import SystemTestTool



class PipelineInitializer:
    """
    Construtor da arquitetura cognitiva.

    Monta:

    Parser
       |
    Planner
       |
    Reasoner
       |
    Executor
       |
    Reflection
    """



    def __init__(
        self,
        logger=None
    ):

        self.logger = logger

        self.pipeline = None



    # ==================================================

    def build(
        self
    ):
        """
        Cria e configura a pipeline.
        """



        if self.pipeline:

            self._log(
                "info",
                "Pipeline já inicializada."
            )

            return self.pipeline



        self._log(
            "info",
            "Construindo Pipeline Cognitiva."
        )



        pipeline = CognitivePipeline()



        # ==============================================
        # Criando etapas cognitivas
        # ==============================================


        parser = Parser()

        planner = Planner()

        reasoner = Reasoner()

        executor = Executor()

        reflection = Reflection()



        # ==============================================
        # Registrando ferramentas
        # ==============================================


        executor.register_tool(
            SystemTestTool()
        )


        self._log(
            "info",
            "Ferramenta registrada: system_test"
        )



        # ==============================================
        # Montando pipeline
        # ==============================================


        steps = [

            parser,

            planner,

            reasoner,

            executor,

            reflection

        ]



        for step in steps:


            pipeline.add_step(
                step
            )


            self._log(
                "info",
                f"Etapa registrada: {step.name}"
            )



        self.pipeline = pipeline



        self._log(
            "success",
            "Pipeline Cognitiva construída."
        )



        return pipeline



    # ==================================================

    def get_pipeline(
        self
    ):
        """
        Retorna pipeline atual.
        """


        return self.pipeline



    # ==================================================

    def reset(
        self
    ):
        """
        Remove pipeline atual.
        """


        self.pipeline = None



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

                method(
                    message
                )

                return



        print(
            f"[PIPELINE:{level.upper()}] {message}"
        )