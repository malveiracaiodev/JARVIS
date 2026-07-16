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



    def __init__(
        self
    ):

        self._name = "system_test"



    # ==============================================
    # METADADOS DA TOOL
    # ==============================================


    def name(
        self
    ):

        return self._name



    @property
    def description(
        self
    ):

        return (
            "Ferramenta interna para "
            "diagnóstico do Genesis Core."
        )



    @property
    def permissions(
        self
    ):

        return [

            "system.test"

        ]



    @property
    def status(
        self
    ):

        return "online"



    # ==============================================
    # VALIDAÇÃO
    # ==============================================


    def validate(
        self,
        action
    ):


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



        return any(

            word in text

            for word in keywords

        )



    # ==============================================
    # EXECUÇÃO
    # ==============================================


    def execute(
        self,
        action,
        context=None
    ):


        return {

            "message":
                "Sistema cognitivo operacional.",


            "tool":
                self.name(),


            "action":
                action,


            "status":
                "success"

        }