"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/executor.py

Descrição:
Executor Cognitivo do Genesis Core.

Transforma decisões produzidas pelo Reasoner
em operações através do ToolManager.

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


from core.pipeline.pipeline_context import (
    PipelineContext
)



class Executor(
    PipelineStep,
    ExecutorInterface
):


    """
    Executor da Pipeline Cognitiva.

    Apenas executa ações.

    Não decide.
    Não interpreta.
    Não planeja.
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


    def get_name(
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

                "executor",


            "executions":

                self.executions,


            "failures":

                self.failures,


            "tool_manager":

                self.tool_manager is not None

        }



    # ==================================================
    # PIPELINE
    # ==================================================


    def process(
        self,
        context: PipelineContext
    ):


        thought = context.get_thought()


        if thought is None:


            context.add_error(
                "Executor recebeu Context sem Thought."
            )


            return context



        try:


            decision = thought.decision



            if decision is None:


                decision = context.get(
                    "decision"
                )



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


            thought.set_metadata(
                "execution",
                result
            )



            context.set(
                "result",
                result
            )



            context.add_history({

                "step":
                    "executor",

                "success":
                    result.get(
                        "success",
                        False
                    ),

                "timestamp":
                    datetime.now().isoformat()

            })



        except Exception as error:


            self.failures += 1


            result = self.failure(
                str(error)
            )


            thought.set_result(
                result
            )


            context.set(
                "result",
                result
            )


            context.add_error(
                str(error)
            )


            self.log_error(
                str(error)
            )



        return context



    # ==================================================
    # AÇÃO
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

                        if isinstance(
                            thought.plan,
                            dict
                        )

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
    # EXECUÇÃO
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


            if hasattr(
                self.tool_manager,
                "execute"
            ):


                result = self.tool_manager.execute(
                    action
                )


                self.executions += 1



                if isinstance(
                    result,
                    dict
                ):


                    success = result.get(
                        "success",
                        True
                    )


                else:

                    success = True



                return {


                    "success":

                        success,


                    "result":

                        result,


                    "timestamp":

                        datetime.now()
                        .isoformat()

                }



            return self.failure(
                "ToolManager sem execute()."
            )



        except Exception as error:


            self.failures += 1


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


        return self.tool_manager is not None



    def rollback(
        self,
        action
    ):


        return {

            "success":

                False,

            "message":

                "Rollback não implementado.",

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
    # INFO
    # ==================================================


    def info(
        self
    ):

        return self.status()