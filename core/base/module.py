"""
=========================================
JARVIS CORE

Arquivo:
module.py

Descrição:
Classe base para todos os módulos
do JARVIS.

Mark:
II - Evolution Stable

Autor:
Caio Vitor Malveira
=========================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid



class ModuleStatus(Enum):

    OFFLINE = 0

    INITIALIZING = 1

    ONLINE = 2

    WARNING = 3

    ERROR = 4





class Module(ABC):

    """
    Classe base de todos os módulos.
    """



    def __init__(self, name):

        self.id = str(
            uuid.uuid4()
        )

        self.name = name

        self.version = "1.0"


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



    # ==================================================
    # Interface
    # ==================================================


    @abstractmethod
    def initialize(self):

        pass



    @abstractmethod
    def shutdown(self):

        pass



    # ==================================================
    # Estado
    # ==================================================


    def set_status(
        self,
        status
    ):


        if not isinstance(
            status,
            ModuleStatus
        ):

            raise ValueError(
                "Status inválido"
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
        message
    ):


        self.error_message = message


        self.set_status(
            ModuleStatus.ERROR
        )



    def restart(self):

        self.shutdown()

        self.initialize()



    # ==================================================
    # Diagnóstico
    # ==================================================


    def get_status(self):

        return self.status



    def is_online(self):

        return (
            self.status ==
            ModuleStatus.ONLINE
        )



    def is_offline(self):

        return (
            self.status ==
            ModuleStatus.OFFLINE
        )



    def has_error(self):

        return (
            self.status ==
            ModuleStatus.ERROR
        )



    def uptime(self):


        if not self.started_at:

            return 0


        return (

            datetime.now()

            -
            self.started_at

        ).total_seconds()



    def info(self):


        return {

            "id":
                self.id,

            "name":
                self.name,

            "version":
                self.version,

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
            f"[{self.status.name}]"
        )