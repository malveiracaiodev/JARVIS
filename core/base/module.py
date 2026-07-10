"""
=========================================
JARVIS CORE

Arquivo:
module.py

Descrição:
Classe base para todos os módulos
do JARVIS.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime



class ModuleStatus(Enum):
    """
    Estados possíveis de um módulo.
    """

    OFFLINE = 0
    INITIALIZING = 1
    ONLINE = 2
    ERROR = 3





class Module(ABC):
    """
    Classe base de todos os módulos do JARVIS.

    Todos os componentes do sistema
    devem herdar desta classe.
    """



    def __init__(self, name: str):

        self.name = name


        self.status = ModuleStatus.OFFLINE


        self.created_at = datetime.now()


        self.started_at = None


        self.error_message = None


        self.status_history = [

            {
                "status":
                    self.status.name,

                "time":
                    self.created_at.isoformat()
            }

        ]




    # ==========================================================
    # Interface obrigatória
    # ==========================================================


    @abstractmethod
    def initialize(self):

        pass




    @abstractmethod
    def shutdown(self):

        pass





    # ==========================================================
    # Controle de estado
    # ==========================================================


    def get_status(self):

        return self.status





    def set_status(
        self,
        status: ModuleStatus
    ):
        """
        Atualiza estado do módulo.
        """


        if not isinstance(
            status,
            ModuleStatus
        ):

            raise ValueError(
                "Status inválido."
            )



        self.status = status



        self.status_history.append(

            {

                "status":
                    status.name,

                "time":
                    datetime.now()
                    .isoformat()

            }

        )



        if status == ModuleStatus.ONLINE:

            self.started_at = datetime.now()





    def set_error(
        self,
        message: str
    ):
        """
        Coloca módulo em erro.
        """


        self.error_message = message


        self.set_status(
            ModuleStatus.ERROR
        )





    # ==========================================================
    # Diagnóstico
    # ==========================================================


    def is_online(self):

        return (
            self.status
            ==
            ModuleStatus.ONLINE
        )





    def is_offline(self):

        return (
            self.status
            ==
            ModuleStatus.OFFLINE
        )





    def has_error(self):

        return (
            self.status
            ==
            ModuleStatus.ERROR
        )





    def uptime(self):
        """
        Retorna tempo online.
        """


        if not self.started_at:

            return 0



        return (
            datetime.now()
            -
            self.started_at
        ).total_seconds()





    def info(self):
        """
        Informações completas do módulo.
        """


        return {


            "name":
                self.name,


            "status":
                self.status.name,


            "created_at":
                self.created_at.isoformat(),


            "started_at":
                (
                    self.started_at.isoformat()
                    if self.started_at
                    else None
                ),


            "uptime":
                self.uptime(),


            "error":
                self.error_message


        }





    def __str__(self):

        return (
            f"{self.name} "
            f"({self.status.name})"
        )