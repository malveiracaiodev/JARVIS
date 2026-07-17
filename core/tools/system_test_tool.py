"""
=========================================
JARVIS CORE

Arquivo:
core/tools/system_test_tool.py

Descrição:
Ferramenta de diagnóstico interno
do Executor Cognitivo.

Responsável por:
- Validar pipeline cognitiva
- Testar execução de ferramentas
- Confirmar comunicação entre módulos

Arquitetura:
Genesis Core

Mark:
III - Matrix (Tool Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.interfaces.tool_interface import (
    ToolInterface
)





class SystemTestTool(
    ToolInterface
):

    """
    Ferramenta interna de diagnóstico.

    Utilizada para validar:

    - Parser
    - Planner
    - Reasoner
    - Executor
    - Reflection
    """



    def __init__(self):

        self._name = (
            "system_test"
        )


        self._version = (
            "1.0"
        )



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def id(self):

        return self._name



    def name(self):

        return self._name





    @property
    def description(self):

        return (
            "Ferramenta interna de diagnóstico "
            "do Genesis Core."
        )





    @property
    def version(self):

        return self._version





    @property
    def permissions(self):

        return [

            "system.test"

        ]





    @property
    def status(self):

        return "ONLINE"





    # ==================================================
    # METADATA
    # ==================================================


    def metadata(self):

        return {

            "name":
                self.name(),

            "description":
                self.description,

            "version":
                self.version,

            "permissions":
                self.permissions,

            "status":
                self.status

        }





    # ==================================================
    # VALIDAÇÃO
    # ==================================================


    def validate(
        self,
        action
    ):


        if not isinstance(
            action,
            dict
        ):

            return False



        goal = str(

            action.get(
                "goal",
                ""
            )

        ).lower()



        keywords = [

            "teste",

            "testar",

            "sistema",

            "cognitivo",

            "diagnostico"

        ]



        return any(

            word in goal

            for word in keywords

        )





    def can_execute(
        self,
        action
    ):

        return self.validate(
            action
        )





    # ==================================================
    # EXECUÇÃO
    # ==================================================


    def execute(
        self,
        action,
        context=None
    ):


        return {


            "success":
                True,


            "message":
                "Sistema cognitivo operacional.",


            "tool":
                self.name(),


            "action":
                action,


            "context_received":
                context is not None,


            "executed_at":
                datetime.now()
                .isoformat(),


            "status":
                "SUCCESS"

        }