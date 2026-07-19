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


from core.cognitive.parser import (
    Parser
)


from core.cognitive.planner import (
    Planner
)


from core.cognitive.reasoner import (
    Reasoner
)


from core.cognitive.executor import (
    Executor
)


from core.cognitive.reflection import (
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
    Montador da Pipeline Cognitiva Genesis.

    Fluxo:

        Parser
          |
        Planner
          |
        Reasoner
          |
        Executor
          |
        Reflection

    Thought é o núcleo.
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



        if self.tool_manager is None:


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

                f"Etapa registrada: {self._step_name(step)}"

            )



        pipeline.initialize()



        self.pipeline = pipeline



        self._log(

            "success",

            "Thought Engine construída."

        )



        return pipeline




    # ==================================================
    # NOME DE STEP
    # ==================================================


    def _step_name(
        self,
        step
    ):


        name = getattr(

            step,

            "name",

            None

        )



        if callable(name):

            return name()



        if name:

            return name



        return step.__class__.__name__.lower()




    # ==================================================
    # TOOLS PADRÃO
    # ==================================================


    def _register_default_tools(
        self
    ):


        try:


            existing = self.tool_manager.list_tools()



        except Exception:


            existing = []



        if "system_test" not in existing:


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

            self._step_name(step)

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


            if callable(method):


                method(
                    message
                )


                return



        print(

            f"[PIPELINE:{level.upper()}] {message}"

        )