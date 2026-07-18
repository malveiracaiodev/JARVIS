"""
=========================================
GENESIS CORE

Arquivo:
core/pipeline/cognitive_pipeline.py

Descrição:
Motor principal da Pipeline Cognitiva
do Genesis Core.

Responsável por:

- Gerenciar etapas cognitivas
- Executar PipelineSteps
- Transportar PipelineContext
- Controlar fluxo cognitivo
- Registrar histórico de processamento

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)


from core.interfaces.pipeline_interface import (
    PipelineInterface
)


from core.models.thought import (
    Thought
)


from core.pipeline.pipeline_context import (
    PipelineContext
)


from core.pipeline.pipeline_step import (
    PipelineStep
)



class CognitivePipeline(
    Module,
    PipelineInterface
):


    """
    Orquestrador da Pipeline Cognitiva.

    Não possui inteligência própria.

    Apenas coordena:

        Parser
          |
        Planner
          |
        Reasoner
          |
        Executor
          |
        Reflection

    O Thought é transportado pelo Context.
    """



    def __init__(
        self,
        name="core.cognitive_pipeline"
    ):


        super().__init__(
            name
        )


        self._name = name


        self.steps_list = []


        self.history = []


        self.errors = []



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def name(
        self
    ):

        return self._name



    # ==================================================
    # CICLO DE VIDA
    # ==================================================


    def initialize(
        self
    ):


        self.set_status(
            ModuleStatus.ONLINE
        )


        return True



    def shutdown(
        self
    ):


        self.steps_list.clear()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        return True



    # ==================================================
    # ETAPAS
    # ==================================================


    def add_step(
        self,
        step
    ):


        if not isinstance(
            step,
            PipelineStep
        ):


            raise TypeError(
                "A etapa precisa herdar PipelineStep."
            )


        self.steps_list.append(
            step
        )



    def remove_step(
        self,
        step_name
    ):


        self.steps_list = [

            step

            for step in self.steps_list

            if step.name != step_name

        ]



    def steps(
        self
    ):


        return self.steps_list



    def list_steps(
        self
    ):


        return [

            step.name

            for step in self.steps_list

        ]



    # ==================================================
    # EXECUÇÃO MARK IV
    # ==================================================


    def process(
        self,
        thought: Thought,
        context: PipelineContext | None = None
    ) -> PipelineContext:



        if context is None:


            context = PipelineContext(

                thought.message

            )


            context.set_thought(
                thought
            )



        if not self.steps_list:


            context.add_error(

                "Pipeline sem etapas registradas."

            )


            thought.failed()


            return context



        for step in self.steps_list:



            started = datetime.now()



            try:



                context.update_step(

                    step.name

                )



                context.add_history(

                    {

                        "step":

                            step.name,


                        "status":

                            "started",


                        "timestamp":

                            started.isoformat()

                    }

                )



                # ======================================
                # MARK IV
                #
                # Cada etapa recebe e devolve
                # o mesmo PipelineContext.
                #
                # O método correto é process().
                #
                # execute() pertence à camada
                # de execução de ações.
                # ======================================


                context = step.process(

                    context

                )



                if not isinstance(

                    context,

                    PipelineContext

                ):


                    raise TypeError(

                        f"A etapa '{step.name}' retornou "

                        f"{type(context).__name__}. "

                        "Esperado PipelineContext."

                    )



                finished = datetime.now()



                duration = (

                    finished - started

                ).total_seconds()



                self.history.append(

                    {

                        "step":

                            step.name,


                        "duration":

                            duration

                    }

                )



                context.add_history(

                    {

                        "step":

                            step.name,


                        "status":

                            "completed",


                        "duration":

                            duration

                    }

                )



            except Exception as error:



                self.errors.append(

                    {

                        "step":

                            step.name,


                        "error":

                            str(error)

                    }

                )



                context.add_error(

                    {

                        "step":

                            step.name,


                        "error":

                            str(error)

                    }

                )



                thought.failed()



                break



        return context



    # ==================================================
    # CONTROLE
    # ==================================================


    def reset(
        self
    ):


        self.history.clear()


        self.errors.clear()


        return True



    # ==================================================
    # STATUS
    # ==================================================


    def status(
        self
    ):


        return {


            "name":

                self._name,


            "status":

                self.get_status().value,


            "steps":

                len(
                    self.steps_list
                ),


            "errors":

                len(
                    self.errors
                )

        }