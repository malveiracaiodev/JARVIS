"""
=========================================
GENESIS CORE

Arquivo:
core/pipeline/cognitive_pipeline.py

Descrição:
Motor principal da Pipeline Cognitiva.

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine
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



    def reset(
        self
    ):

        self.steps_list.clear()

        self.history.clear()

        self.errors.clear()

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
                "PipelineStep inválido."
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
    # PROCESSAMENTO
    # ==================================================


    def process(
        self,
        thought: Thought,
        context=None
    ):


        if thought is None:

            raise ValueError(
                "Thought não pode ser None."
            )


        if context is None:

            context = PipelineContext(
                thought
            )


        context.start()


        self.history.append({

            "event":
                "pipeline_started",

            "thought":
                thought.id,

            "timestamp":
                datetime.now().isoformat()

        })



        for step in self.steps_list:


            try:


                context.update_step(
                    step.name
                )


                context = step.process(
                    context
                )


                if context.has_errors():

                    break



            except Exception as error:


                context.add_error(
                    str(error)
                )

                self.errors.append(
                    str(error)
                )

                break



        if context.has_errors():


            context.fail()



        else:


            context.complete()



        self.history.append({

            "event":
                "pipeline_finished",

            "thought":
                thought.id,

            "errors":
                len(context.errors),

            "timestamp":
                datetime.now().isoformat()

        })


        return context



    # ==================================================
    # HISTÓRICO
    # ==================================================


    def get_history(
        self
    ):

        return self.history



    def get_errors(
        self
    ):

        return self.errors



    def clear_history(
        self
    ):

        self.history.clear()



    def clear_errors(
        self
    ):

        self.errors.clear()



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

                str(
                    self.status()
                ),


            "steps":

                self.list_steps(),


            "history":

                len(
                    self.history
                ),


            "errors":

                len(
                    self.errors
                )

        }