"""
=========================================
GENESIS CORE

Arquivo:
core/pipeline/pipeline_initializer.py

Descrição:
Construtor da Pipeline Cognitiva.

Responsável por:

- Registrar ferramentas iniciais
- Construir fluxo Thought Engine
- Conectar Executor ao ToolManager
- Preparar módulos cognitivos

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


from core.cognitive import (
    Executor,
    Parser,
    Planner,
    Reasoner,
    Reflection
)


from core.pipeline.cognitive_pipeline import (
    CognitivePipeline
)


from core.tools import (
    SystemTestTool
)



class PipelineInitializer:
    """
    Montador da inteligência cognitiva Genesis.

    Cria a cadeia:

        Parser
          |
        Planner
          |
        Reasoner
          |
        Executor
          |
        Reflection

    O Thought é o núcleo do fluxo.
    """



    def __init__(
        self,
        logger=None,
        tool_manager=None
    ):


        self.logger = logger

        self.tool_manager = tool_manager

        self.pipeline = None

        self.steps = []



    # ==================================================
    # CONSTRUÇÃO
    # ==================================================


    def build(
        self
    ):


        if self.pipeline:


            self._log(
                "info",
                "Pipeline já inicializada."
            )


            return self.pipeline



        if not self.tool_manager:


            raise RuntimeError(

                "Pipeline Cognitiva requer ToolManager."

            )



        self._log(

            "info",

            "Construindo Thought Engine."

        )



        self._register_default_tools()



        pipeline = CognitivePipeline()



        self.steps = [


            Parser(
                logger=self.logger
            ),



            Planner(
                logger=self.logger
            ),



            Reasoner(
                logger=self.logger
            ),



            Executor(

                tool_manager=self.tool_manager,

                logger=self.logger

            ),



            Reflection(

                logger=self.logger

            )

        ]



        for step in self.steps:


            pipeline.add_step(
                step
            )


            self._log(

                "info",

                f"Etapa registrada: {step.name}"

            )



        pipeline.initialize()



        self.pipeline = pipeline



        self._log(

            "success",

            "Thought Engine construída."

        )



        return pipeline



    # ==================================================
    # REGISTRO DE TOOLS
    # ==================================================


    def _register_default_tools(
        self
    ):


        if "system_test" not in self.tool_manager.list_tools():


            self.tool_manager.register(

                SystemTestTool()

            )


            self._log(

                "info",

                "Ferramenta registrada: system_test"

            )



    # ==================================================
    # CONSULTA
    # ==================================================


    def get_pipeline(
        self
    ):


        return self.pipeline



    def get_steps(
        self
    ):


        return [

            step.name

            for step in self.steps

        ]



    # ==================================================
    # RESET
    # ==================================================


    def reset(
        self
    ):


        if self.pipeline:


            self.pipeline.shutdown()



        self.pipeline = None

        self.steps.clear()



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


            if method:


                method(
                    message
                )

                return



        print(

            f"[PIPELINE:{level.upper()}] {message}"

        )