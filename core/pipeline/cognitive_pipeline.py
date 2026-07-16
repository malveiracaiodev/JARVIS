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
- Registrar histórico de processamento

Arquitetura:
Genesis Core

Mark:
III - Matrix

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
    # EXECUÇÃO
    # ==================================================


    def process(
        self,
        input_data,
        context=None
    ):


        if context is None:

            context = PipelineContext(
                input_data
            )



        if not self.steps_list:

            context.add_error(
                "Pipeline sem etapas registradas."
            )

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



                # ==========================================
                # EXECUTA ETAPA
                # ==========================================

                context = step.execute(
                    context
                )



                # ==========================================
                # VALIDA CONTRATO
                # ==========================================

                if not isinstance(
                    context,
                    PipelineContext
                ):

                    raise TypeError(
                        f"A etapa '{step.name}' "
                        f"retornou "
                        f"{type(context).__name__}. "
                        "Esperado PipelineContext."
                    )



                finished = datetime.now()



                self.history.append(
                    {

                        "step":
                            step.name,


                        "duration":
                            str(
                                finished - started
                            )

                    }
                )



                context.add_history(
                    {

                        "step":
                            step.name,


                        "status":
                            "completed"

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



                # Proteção contra erro em cascata

                if isinstance(
                    context,
                    PipelineContext
                ):

                    context.add_error(
                        {

                            "step":
                                step.name,


                            "error":
                                str(error)

                        }
                    )


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