"""
=========================================
GENESIS CORE

Arquivo:
core/managers/tool_manager.py

Descrição:
Gerenciador central das ferramentas
executáveis do Genesis Core.

Responsável por:
- Registrar Tools
- Validar capacidades
- Executar ações
- Integrar capacidades ao Registry

Arquitetura:
Genesis Core

Mark:
III - Matrix (Tool Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import threading


from core.base.module import (
    Module,
    ModuleStatus
)


from core.interfaces.tool_interface import (
    ToolInterface
)





class ToolManager(Module):

    """
    Núcleo de capacidades executáveis.
    """



    def __init__(
        self,
        logger=None,
        registry=None
    ):


        super().__init__(
            "core.tool_manager"
        )


        self.version = "3.5"


        self.logger = logger

        self.registry = registry



        self._tools = {}

        self._lock = threading.RLock()





    # ==================================================
    # CICLO DE VIDA
    # ==================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log_success(
            "Tool Manager Mark III ONLINE."
        )





    def shutdown(self):


        self.clear()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Tool Manager encerrado."
        )





    # ==================================================
    # REGISTRO
    # ==================================================


    def register(
        self,
        tool
    ):


        if not isinstance(
            tool,
            ToolInterface
        ):


            raise TypeError(
                "Tool precisa implementar ToolInterface."
            )



        name = tool.name()



        if not name:

            raise ValueError(
                "Tool sem nome."
            )



        with self._lock:


            if name in self._tools:


                self.log_info(
                    f"Tool já registrada: {name}"
                )


                return False



            self._tools[name] = {


                "object":
                    tool,


                "version":
                    getattr(
                        tool,
                        "version",
                        "1.0"
                    ),


                "status":
                    "online"

            }



        if self.registry:


            self.registry.register_capability(
                name,
                tool
            )



        self.log_info(
            f"Tool registrada: {name}"
        )


        return True





    def unregister(
        self,
        name
    ):


        with self._lock:


            data = self._tools.pop(
                name,
                None
            )



        if data:


            if self.registry:


                self.registry.unregister(
                    name
                )


            self.log_info(
                f"Tool removida: {name}"
            )


            return True



        return False





    def clear(self):


        with self._lock:


            names = list(
                self._tools.keys()
            )


        for name in names:

            self.unregister(
                name
            )





    # ==================================================
    # CONSULTA
    # ==================================================


    def get(
        self,
        name
    ):


        with self._lock:


            data = self._tools.get(
                name
            )


            return (
                data["object"]
                if data
                else None
            )





    def get_all(self):


        with self._lock:


            return {

                name:
                data["object"]

                for name, data

                in self._tools.items()

            }





    def list_tools(self):


        with self._lock:


            return list(
                self._tools.keys()
            )





    # ==================================================
    # BUSCA
    # ==================================================


    def find(
        self,
        action
    ):


        with self._lock:


            tools = [

                data["object"]

                for data

                in self._tools.values()

            ]



        for tool in tools:


            try:


                if tool.validate(
                    action
                ):


                    return tool



            except Exception as error:


                self.log_error(
                    f"Erro validando {tool.name()}: {error}"
                )



        return None





    def has(
        self,
        action
    ):


        return self.find(
            action
        ) is not None





    # ==================================================
    # EXECUÇÃO
    # ==================================================


    def execute(
        self,
        action,
        context=None
    ):


        if not action:


            return {

                "success":
                    False,

                "message":
                    "Ação vazia."

            }



        tool = self.find(
            action
        )



        if not tool:


            return {

                "success":
                    False,

                "message":
                    "Nenhuma Tool encontrada."

            }




        try:


            result = tool.execute(
                action,
                context
            )



            return {


                "success":
                    True,


                "tool":
                    tool.name(),


                "result":
                    result

            }



        except Exception as error:


            self.log_error(
                f"Falha executando {tool.name()}: {error}"
            )


            return {


                "success":
                    False,


                "error":
                    str(error)

            }





    # ==================================================
    # LOG
    # ==================================================


    def log_info(
        self,
        msg
    ):

        if self.logger:

            self.logger.info(msg)





    def log_success(
        self,
        msg
    ):

        if self.logger:

            self.logger.success(msg)





    def log_error(
        self,
        msg
    ):

        if self.logger:

            self.logger.error(msg)