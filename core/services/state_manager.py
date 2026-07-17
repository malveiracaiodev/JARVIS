"""
=========================================
JARVIS CORE

Arquivo:
core/services/state_manager.py

Descrição:
Gerenciador do estado global do Genesis Core.

Responsável por:
- Controlar estado operacional
- Registrar transições
- Monitorar ciclo de vida
- Emitir eventos de sistema
- Fornecer diagnóstico global

Arquitetura:
Genesis Core

Mark:
III - Matrix (State Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import copy
import threading


from enum import Enum
from datetime import datetime
from collections import deque



from core.base.module import (
    Module,
    ModuleStatus
)



class SystemState(Enum):

    BOOTING = "BOOTING"

    INITIALIZING = "INITIALIZING"

    ONLINE = "ONLINE"

    IDLE = "IDLE"

    PROCESSING = "PROCESSING"

    BUSY = "BUSY"

    LEARNING = "LEARNING"

    WARNING = "WARNING"

    ERROR = "ERROR"

    SHUTDOWN = "SHUTDOWN"





class StateManager(Module):
    """
    Controlador do estado global
    do Genesis Core.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None,
        max_history=200
    ):


        super().__init__(
            "core.state_manager"
        )


        self.version = "3.0"


        self.logger = logger

        self.event_bus = event_bus



        self.state = (
            SystemState.BOOTING
        )


        self.last_change = (
            datetime.now()
        )


        self.history = deque(
            maxlen=max_history
        )


        self._lock = threading.RLock()





    # ======================================================
    # CICLO DE VIDA
    # ======================================================


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
            "State Manager Mark III ONLINE."
        )




    def shutdown(self):


        self.change_state(
            SystemState.SHUTDOWN
        )


        with self._lock:

            self.history.clear()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "State Manager encerrado."
        )





    # ======================================================
    # CONTROLE DE ESTADO
    # ======================================================


    def change_state(
        self,
        new_state
    ):


        if not isinstance(
            new_state,
            SystemState
        ):

            raise ValueError(
                "Estado inválido."
            )



        with self._lock:



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
                (
                    "Estado alterado: "
                    f"{old_state.value} -> "
                    f"{new_state.value}"
                )
            )



            self.emit(
                "SYSTEM_STATE_CHANGED",
                record
            )





    def set_state(
        self,
        state
    ):

        self.change_state(
            state
        )





    # ======================================================
    # CONSULTA
    # ======================================================


    def get_state(self):


        with self._lock:

            return self.state





    def is_state(
        self,
        state
    ):


        with self._lock:

            return self.state == state





    def get_history(self):


        with self._lock:


            return copy.deepcopy(
                list(self.history)
            )





    def status_report(self):


        with self._lock:


            return {


                "system_state":
                    self.state.value,


                "last_change":
                    (
                        self.last_change.isoformat()
                        if self.last_change
                        else None
                    ),


                "history_size":
                    len(self.history),


                "module_status":
                    self.status.value
                    if hasattr(
                        self.status,
                        "value"
                    )
                    else str(self.status)

            }







    # ======================================================
    # EVENTOS
    # ======================================================


    def emit(
        self,
        event,
        data=None
    ):


        if self.event_bus:


            try:

                self.event_bus.emit(
                    event,
                    data
                )


            except Exception:

                pass





    # ======================================================
    # LOG
    # ======================================================


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





    def log_error(
        self,
        message
    ):


        if self.logger:

            self.logger.error(
                message
            )