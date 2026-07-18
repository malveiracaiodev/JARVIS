"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/executor.py

Descrição:
Executor Cognitivo do Genesis Core.

Transforma decisões armazenadas no Thought
em operações executáveis através do ToolManager.

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

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


    """
    Camada executora do ciclo cognitivo.

    Responsabilidades:

    - receber Thought;
    - extrair decisão;
    - localizar ferramenta;
    - executar operação;
    - salvar resultado no Thought.

    Não decide.
    Não planeja.
    Não interpreta.

    Apenas executa.
    """



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



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def name(
        self
    ):

        return "executor"



    # ==================================================
    # STATUS
    # ==================================================


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



    # ==================================================
    # PIPELINE MARK IV
    # ==================================================


    def process(
        self,
        context
    ):


        try:


            thought = context.thought



            if thought is None:


                context.add_error(
                    "Nenhum Thought disponível para execução."
                )


                return context



            decision = thought.decision



            action = self.build_action(
                decision,
                thought
            )



            result = self.execute_action(
                action,
                context
            )



            thought.set_result(
                result
            )



            if result.get(
                "success",
                False
            ):


                thought.set_status(
                    "executed"
                )


            else:


                thought.failed()



        except Exception as error:


            self.failures += 1


            self.log_error(
                str(error)
            )


            if context.thought:


                context.thought.set_result(

                    self.failure(
                        str(error)
                    )

                )


                context.thought.failed()



        return context



    # ==================================================
    # CONVERSÃO
    # ==================================================


    def build_action(
        self,
        decision,
        thought
    ):


        if not decision:


            return None



        if isinstance(
            decision,
            dict
        ):


            return {


                "goal":

                    (
                        thought.plan.get(
                            "goal"
                        )

                        if thought.plan

                        else None
                    ),



                "strategy":

                    decision.get(
                        "strategy",
                        "execute_plan"
                    ),



                "plan":

                    thought.plan,



                "decision":

                    decision

            }



        return decision



    # ==================================================
    # EXECUÇÃO REAL
    # ==================================================


    def execute_action(
        self,
        action,
        context=None
    ):


        if not action:


            return self.failure(
                "Nenhuma ação disponível."
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



    # ==================================================
    # INTERFACE
    # ==================================================


    def execute(
        self,
        action,
        context=None
    ):


        return self.execute_action(
            action,
            context
        )



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



    # ==================================================
    # FALHA
    # ==================================================


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


        return self.status()