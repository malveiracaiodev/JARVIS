"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/planner.py

Descrição:
Planejador Cognitivo do Genesis Core.

Responsável por transformar intenções
em estruturas planejáveis.

Não decide.
Não executa.
Não controla ferramentas.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


import uuid

from datetime import datetime


from core.interfaces.planner_interface import (
    PlannerInterface
)


from core.pipeline.pipeline_step import (
    PipelineStep
)



class Planner(
    PipelineStep,
    PlannerInterface
):

    """
    Criador de planos cognitivos.

    O Planner prepara caminhos.

    O Reasoner escolhe o melhor.
    """



    def __init__(
        self,
        logger=None
    ):

        super().__init__(
            "planner"
        )


        self.logger = logger


        self.plans_created = 0

        self.errors = 0



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def name(
        self
    ):

        return "planner"



    # ==================================================
    # STATUS
    # ==================================================


    def status(
        self
    ):

        return {

            "name":
                self.name(),


            "plans_created":
                self.plans_created,


            "errors":
                self.errors

        }



    # ==================================================
    # PIPELINE
    # ==================================================


    def process(
        self,
        context
    ):


        try:


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


            context.data[
                "plan"
            ] = plan



            self.plans_created += 1



        except Exception as error:


            self.errors += 1


            context.data[
                "plan"
            ] = {

                "error":
                    str(error)

            }


            self.log_error(
                str(error)
            )



        return context



    # ==================================================
    # CRIAÇÃO
    # ==================================================


    def create_plan(
        self,
        intention
    ):


        if not intention:


            return {

                "id":
                    str(uuid.uuid4()),


                "goal":
                    None,


                "steps":
                    [],


                "status":
                    "empty"

            }



        return {


            "id":
                str(uuid.uuid4()),


            "created":
                datetime.now()
                .isoformat(),


            "goal":
                intention,


            "priority":
                "normal",


            "status":
                "draft",


            "steps":

            [

                {

                    "order":
                        1,


                    "action":
                        "analyze",


                    "description":
                        "Analisar objetivo e contexto."

                },


                {

                    "order":
                        2,


                    "action":
                        "prepare",


                    "description":
                        "Preparar recursos necessários."

                },


                {

                    "order":
                        3,


                    "action":
                        "execute",


                    "description":
                        "Executar estratégia definida."

                },


                {

                    "order":
                        4,


                    "action":
                        "verify",


                    "description":
                        "Avaliar resultado obtido."

                }

            ]

        }



    # ==================================================
    # DECOMPOSIÇÃO
    # ==================================================


    def decompose(
        self,
        goal
    ):


        if not goal:

            return []



        return [

            {

                "step":
                    1,


                "action":
                    "analyze",


                "goal":
                    goal

            },

            {

                "step":
                    2,


                "action":
                    "execute",


                "goal":
                    goal

            }

        ]



    # ==================================================
    # CANCELAMENTO
    # ==================================================


    def cancel_plan(
        self,
        plan_id
    ):


        return {

            "id":
                plan_id,


            "status":
                "cancelled"

        }



    # ==================================================
    # VALIDAÇÃO
    # ==================================================


    def validate_plan(
        self,
        plan
    ):


        if not isinstance(
            plan,
            dict
        ):

            return False



        required = [

            "id",

            "goal",

            "steps"

        ]



        for field in required:

            if field not in plan:

                return False



        return len(
            plan["steps"]
        ) > 0



    # ==================================================
    # OTIMIZAÇÃO
    # ==================================================


    def optimize_plan(
        self,
        plan
    ):


        if not plan:

            return plan



        plan["optimized"] = True


        return plan



    # ==================================================
    # LOG
    # ==================================================


    def log_error(
        self,
        message
    ):


        if self.logger:

            self.logger.error(
                message
            )



    # ==================================================
    # DIAGNÓSTICO
    # ==================================================


    def info(
        self
    ):

        return {

            "name":
                self.name(),


            "plans_created":
                self.plans_created,


            "errors":
                self.errors

        }