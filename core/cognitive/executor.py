"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/executor.py

Descrição:
Executor Cognitivo do Genesis Core.

Transforma decisões cognitivas em
operações executáveis através do
ToolManager.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.interfaces.executor_interface import (
    ExecutorInterface
)


from core.pipeline.pipeline_step import (
    PipelineStep
)



class Executor(
    PipelineStep,
    ExecutorInterface
):


    def __init__(
        self,
        tool_manager=None,
        logger=None
    ):


        super().__init__(
            "executor"
        )


        self.tool_manager = tool_manager

        self.logger = logger


        self.executions = 0

        self.failures = 0



    # ======================================================
    # IDENTIDADE
    # ======================================================


    def name(
        self
    ):

        return "executor"



    # ======================================================
    # STATUS
    # ======================================================


    def status(
        self
    ):

        return {

            "name":
                self.name(),

            "executions":
                self.executions,

            "failures":
                self.failures,

            "tool_manager":
                self.tool_manager is not None

        }



    # ======================================================
    # PIPELINE
    # ======================================================


    def process(
        self,
        context
    ):


        reasoning = context.data.get(
            "reasoning",
            {}
        )


        decision = reasoning.get(
            "decision",
            {}
        )



        # ==================================================
        # CONVERSÃO DE DECISÃO COGNITIVA
        # PARA AÇÃO EXECUTÁVEL
        # ==================================================

        if isinstance(
            decision,
            dict
        ) and "plan" in decision:


            plan = decision.get(
                "plan",
                {}
            )


            action = {

                "goal":
                    plan.get(
                        "goal",
                        ""
                    ),

                "plan":
                    plan,

                "strategy":
                    decision.get(
                        "strategy",
                        "execute_plan"
                    )

            }



        else:


            action = (

                decision

                or

                context.data.get(
                    "plan",
                    {}
                )

            )



        result = self.execute_action(
            action,
            context
        )


        context.data[
            "execution"
        ] = result



        return context



    # ======================================================
    # EXECUÇÃO DE AÇÃO
    # ======================================================


    def execute_action(
        self,
        action,
        context=None
    ):


        if not action:


            return self.failure(
                "Nenhuma ação fornecida."
            )



        if self.tool_manager is None:


            return self.failure(
                "ToolManager indisponível."
            )



        try:


            tool = self.tool_manager.find(
                action
            )



            if tool is None:


                return self.failure(
                    "Nenhuma ferramenta compatível encontrada."
                )



            self.executions += 1



            result = tool.execute(
                action
            )



            return {

                "success":
                    True,


                "tool":
                    tool.name(),


                "result":
                    result,


                "timestamp":
                    datetime.now()
                    .isoformat()

            }



        except Exception as error:


            self.failures += 1


            self.log_error(
                str(error)
            )


            return self.failure(
                str(error)
            )



    # ======================================================
    # VALIDAÇÃO
    # ======================================================


    def validate(
        self,
        action
    ):


        if not action:

            return False



        if self.tool_manager is None:

            return False



        return (

            self.tool_manager.find(
                action
            )

            is not None

        )



    # ======================================================
    # ROLLBACK
    # ======================================================


    def rollback(
        self,
        action
    ):


        return {

            "success":
                False,


            "message":
                "Rollback ainda não implementado.",


            "action":
                action

        }



    # ======================================================
    # ERRO
    # ======================================================


    def failure(
        self,
        message
    ):


        return {

            "success":
                False,


            "message":
                message,


            "timestamp":
                datetime.now()
                .isoformat()

        }



    def log_error(
        self,
        message
    ):


        if self.logger:

            self.logger.error(
                message
            )



    # ======================================================
    # DIAGNÓSTICO
    # ======================================================


    def info(
        self
    ):

        return self.status()