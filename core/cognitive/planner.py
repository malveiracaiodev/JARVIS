"""
=========================================
JARVIS CORE

Arquivo:
core/cognitive/planner.py

Descrição:
Implementação do Planner Cognitivo
do Genesis Core.

Responsável por transformar entradas
estruturadas em planos cognitivos.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from core.interfaces.planner_interface import PlannerInterface

from core.pipeline.pipeline_step import PipelineStep



class Planner(
    PipelineStep,
    PlannerInterface
):
    """
    Planejador cognitivo.

    Responsável por transformar uma
    intenção em um plano estruturado.

    Não executa ações.
    """



    def __init__(
        self
    ):

        super().__init__(
            "planner"
        )



    # ==================================================
    # PipelineStep
    # ==================================================


    def process(
        self,
        context
    ):
        """
        Executa planejamento dentro
        da Pipeline Cognitiva.
        """



        parsed = context.data.get(
            "parsed",
            {}
        )



        intention = parsed.get(
            "content"
        )



        context.intention = intention



        plan = self.create_plan(
            intention
        )



        context.plan = plan


        context.data["plan"] = plan



        return context



    # ==================================================
    # PlannerInterface
    # ==================================================


    def create_plan(
        self,
        intention
    ):
        """
        Cria um plano baseado
        na intenção recebida.
        """



        if not intention:


            return {

                "goal": None,

                "steps": []

            }



        return {

            "goal":
            intention,


            "steps":

            [

                {

                    "action":
                    "analyze",


                    "description":
                    "Analisar objetivo recebido."

                },


                {

                    "action":
                    "prepare",


                    "description":
                    "Preparar recursos necessários."

                },


                {

                    "action":
                    "execute",


                    "description":
                    "Executar objetivo."

                },


                {

                    "action":
                    "verify",


                    "description":
                    "Verificar resultado."

                }

            ]

        }



    # ==================================================


    def validate_plan(
        self,
        plan
    ):
        """
        Verifica se o plano
        possui estrutura válida.
        """


        if not isinstance(
            plan,
            dict
        ):

            return False



        if "steps" not in plan:

            return False



        if not plan["steps"]:

            return False



        return True



    # ==================================================


    def optimize_plan(
        self,
        plan
    ):
        """
        Otimiza plano existente.

        Futuramente:

        - IA
        - prioridades
        - custos
        - contexto
        """


        return plan