"""
=========================================
JARVIS CORE

Arquivo:
tool_manager.py

Descrição:
Gerenciador central de ferramentas
do Genesis Core.

Responsável por registrar,
localizar e controlar capacidades
executáveis do sistema.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from core.base.module import Module, ModuleStatus



class ToolManager(
    Module
):
    """
    Gerenciador de ferramentas.

    Controla capacidades disponíveis
    para o Executor Cognitivo.
    """



    def __init__(
        self,
        logger=None
    ):

        super().__init__(
            "core.tool_manager"
        )


        self.logger = logger

        self.tools = {}



    # ==================================================

    def initialize(
        self
    ):

        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.success(
            "Tool Manager ativado."
        )



    # ==================================================

    def shutdown(
        self
    ):

        self.tools.clear()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.info(
            "Tool Manager encerrado."
        )



    # ==================================================
    # Registro
    # ==================================================


    def register(
        self,
        tool
    ):
        """
        Registra ferramenta.
        """


        name = tool.name()


        self.tools[name] = tool


        self.info(
            f"Ferramenta registrada: {name}"
        )



    # ==================================================

    def unregister(
        self,
        name
    ):

        self.tools.pop(
            name,
            None
        )



    # ==================================================
    # Busca
    # ==================================================


    def find(
        self,
        action
    ):
        """
        Retorna ferramenta compatível.
        """


        for tool in self.tools.values():


            try:

                if tool.validate(
                    action
                ):

                    return tool


            except Exception:

                continue



        return None



    # ==================================================

    def get_all(
        self
    ):

        return dict(
            self.tools
        )



    # ==================================================

    def list_tools(
        self
    ):

        return list(
            self.tools.keys()
        )



    # ==================================================

    def info(
        self,
        msg
    ):

        if self.logger:

            self.logger.info(
                msg
            )



    def success(
        self,
        msg
    ):

        if self.logger:

            self.logger.success(
                msg
            )



    def error(
        self,
        msg
    ):

        if self.logger:

            self.logger.error(
                msg
            )