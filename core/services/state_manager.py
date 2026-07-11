"""
=========================================
JARVIS CORE

Arquivo:
state_manager.py

Descrição:
Gerenciador do estado global do sistema.

Responsável por:
- Controlar ciclo operacional
- Registrar mudanças
- Emitir eventos de sistema

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from enum import Enum
from datetime import datetime



from core.base.module import (
    Module,
    ModuleStatus
)





class SystemState(Enum):


    BOOTING = "BOOTING"

    INITIALIZING = "INITIALIZING"

    ONLINE = "ONLINE"

    IDLE = "IDLE"

    BUSY = "BUSY"

    WARNING = "WARNING"

    ERROR = "ERROR"

    SHUTDOWN = "SHUTDOWN"







class StateManager(Module):


    """
    Controla o estado global
    do JARVIS.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None
    ):


        super().__init__(
            "core.state_manager"
        )


        self.version = "2.0"


        self.logger = logger


        self.event_bus = event_bus



        self.state = SystemState.BOOTING


        self.last_change = datetime.now()


        self.history = []







    # ==========================================================
    # CICLO DE VIDA
    # ==========================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.change_state(
            SystemState.INITIALIZING
        )



        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log_success(
            "State Manager iniciado"
        )






    def shutdown(self):


        self.change_state(
            SystemState.SHUTDOWN
        )


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "State Manager encerrado"
        )







    # ==========================================================
    # CONTROLE
    # ==========================================================


    def change_state(
        self,
        new_state
    ):


        if not isinstance(
            new_state,
            SystemState
        ):


            raise ValueError(
                "Estado inválido"
            )



        if self.state == new_state:

            return



        old_state = self.state



        self.state = new_state


        now = datetime.now()



        self.last_change = now



        record = {


            "from":
            old_state.value,


            "to":
            new_state.value,


            "time":
            now.isoformat()

        }



        self.history.append(
            record
        )



        self.log_info(
            f"Estado: {old_state.value} -> {new_state.value}"
        )



        self.emit(
            "SYSTEM_STATE_CHANGED",
            record
        )








    # ==========================================================
    # CONSULTA
    # ==========================================================


    def get_state(self):


        return self.state






    def is_state(
        self,
        state
    ):


        return self.state == state






    def get_history(self):


        return self.history







    def status_report(self):


        return {


            "system_state":
            self.state.value,


            "last_change":

            self.last_change.isoformat()
            if self.last_change
            else None,


            "changes":
            len(self.history)

        }








    # ==========================================================
    # Auxiliares
    # ==========================================================


    def emit(
        self,
        event,
        data
    ):


        if self.event_bus:


            self.event_bus.emit(
                event,
                data
            )



    def log_info(
        self,
        message
    ):


        if self.logger:

            self.logger.info(
                message
            )



    def log_success(
        self,
        message
    ):


        if self.logger:

            self.logger.success(
                message
            )