"""
=========================================
JARVIS CORE

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

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.base.module import Module

from core.interfaces.pipeline_interface import PipelineInterface

from core.pipeline.pipeline_context import PipelineContext

from core.pipeline.pipeline_step import PipelineStep



class CognitivePipeline(
    Module,
    PipelineInterface
):
    """
    Orquestrador da Pipeline Cognitiva.

    A pipeline não pensa.

    Ela apenas transporta o contexto
    entre etapas cognitivas.
    """



    def __init__(
        self,
        name: str = "core.cognitive_pipeline"
    ):

        super().__init__(
            name
        )


        self.steps = []



    # ==================================================
    # Ciclo de vida do Module
    # ==================================================


    def initialize(
        self
    ):
        """
        Inicializa a Pipeline Cognitiva.
        """


        return True



    # ==================================================


    def shutdown(
        self
    ):
        """
        Finaliza a Pipeline Cognitiva.
        """


        self.steps.clear()


        return True



    # ==================================================
    # Gerenciamento
    # ==================================================


    def add_step(
        self,
        step
    ):
        """
        Adiciona uma etapa cognitiva.
        """


        if not isinstance(
            step,
            PipelineStep
        ):

            raise TypeError(
                "A etapa precisa herdar PipelineStep."
            )


        self.steps.append(
            step
        )



    # ==================================================


    def remove_step(
        self,
        step_name: str
    ):
        """
        Remove uma etapa pelo nome.
        """


        self.steps = [

            step

            for step in self.steps

            if step.name != step_name

        ]



    # ==================================================
    # Execução Cognitiva
    # ==================================================


    def process(
        self,
        message
    ):
        """
        Executa ciclo cognitivo completo.
        """


        context = PipelineContext(
            message
        )



        if not self.steps:

            context.add_error(
                "Nenhuma etapa cognitiva registrada."
            )

            return context



        for step in self.steps:


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


                        "time":
                        started.isoformat()

                    }
                )



                context = step.execute(
                    context
                )



                finished = datetime.now()



                context.add_history(
                    {

                        "step":
                        step.name,


                        "status":
                        "completed",


                        "duration":
                        str(
                            finished - started
                        )

                    }
                )



            except Exception as error:


                context.add_error(
                    {

                        "step":
                        step.name,


                        "error":
                        str(error)

                    }
                )


                context.add_history(
                    {

                        "step":
                        step.name,


                        "status":
                        "failed"

                    }
                )


                break



        return context



    # ==================================================
    # Controle
    # ==================================================


    def clear_steps(
        self
    ):
        """
        Remove todas as etapas.
        """


        self.steps.clear()



    # ==================================================


    def list_steps(
        self
    ):
        """
        Lista etapas carregadas.
        """


        return [

            step.name

            for step in self.steps

        ]