"""
=========================================
JARVIS CORE

Arquivo:
core/cognitive/executor.py

Descrição:
Implementação do Executor Cognitivo
do Genesis Core.

Responsável por transformar decisões
em operações executáveis.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from core.interfaces.executor_interface import ExecutorInterface

from core.pipeline.pipeline_step import PipelineStep



class Executor(
    PipelineStep,
    ExecutorInterface
):
    """
    Executor cognitivo.

    Responsabilidades:

    - Receber decisões
    - Encontrar ferramentas compatíveis
    - Executar operações

    Não possui ferramentas próprias.

    Utiliza ferramentas externas.
    """



    def __init__(
        self
    ):

        super().__init__(
            "executor"
        )


        self.tools = []



    # ==================================================
    # Gerenciamento de ferramentas
    # ==================================================


    def register_tool(
        self,
        tool
    ):
        """
        Registra uma ferramenta externa.
        """


        self.tools.append(
            tool
        )



    # ==================================================
    # PipelineStep
    # ==================================================


    def process(
        self,
        context
    ):
        """
        Executa decisão cognitiva
        dentro da Pipeline.
        """


        reasoning = context.data.get(
            "reasoning",
            {}
        )


        action = reasoning.get(
            "decision"
        )


        if not action:

            action = context.data.get(
                "plan"
            )



        result = self.execute_action(
            action
        )


        context.data["execution"] = result


        return context



    # ==================================================
    # Execução
    # ==================================================


    def execute_action(
        self,
        action
    ):
        """
        Executa uma ação usando
        ferramentas registradas.
        """


        if not action:

            return {

                "success": False,

                "message":
                "Nenhuma ação fornecida."

            }



        for tool in self.tools:


            try:

                if tool.validate(
                    action
                ):


                    result = tool.execute(
                        action
                    )


                    return {

                        "success": True,

                        "tool":
                        tool.name(),

                        "result":
                        result

                    }


            except Exception as error:


                return {

                    "success": False,

                    "error":
                    str(error)

                }



        return {

            "success": False,

            "message":
            "Nenhuma ferramenta compatível encontrada."

        }



    # ==================================================
    # ExecutorInterface
    # ==================================================


    def validate(
        self,
        action
    ):
        """
        Verifica se existe capacidade
        de execução.
        """


        if not action:

            return False



        for tool in self.tools:


            try:

                if tool.validate(
                    action
                ):

                    return True


            except Exception:

                continue



        return False



    # ==================================================


    def rollback(
        self,
        action
    ):
        """
        Sistema inicial de reversão.

        Futuramente:

        - desfazer ações
        - restaurar estados
        - recuperar falhas
        """


        return {

            "success": False,

            "message":
            "Rollback não implementado."

        }