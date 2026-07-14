"""
=========================================
JARVIS CORE

Arquivo:
core/tools/system_test_tool.py

Descrição:
Primeira ferramenta de teste
do Executor Cognitivo.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from core.interfaces.tool_interface import ToolInterface



class SystemTestTool(
    ToolInterface
):
    """
    Ferramenta inicial de diagnóstico.

    Usada para validar:

    Pipeline
    Reasoner
    Executor
    Reflection
    """



    def name(
        self
    ):
        return "system_test"



    # ==============================================


    def validate(
        self,
        action
    ):
        """
        Verifica se é uma ação
        de teste do sistema.
        """


        if not action:

            return False



        if not isinstance(
            action,
            dict
        ):

            return False



        goal = action.get(
            "goal",
            ""
        )



        keywords = [

            "teste",

            "testar",

            "sistema",

            "cognitivo"

        ]



        text = str(
            goal
        ).lower()



        for word in keywords:

            if word in text:

                return True



        return False



    # ==============================================


    def execute(
        self,
        action
    ):
        """
        Executa diagnóstico.
        """


        return {

            "message":
            "Sistema cognitivo operacional.",


            "action":
            action,


            "status":
            "online"

        }