"""
=========================================
JARVIS CORE

Arquivo:
core/services/logger.py

Descrição:
Sistema central de logs do Genesis Core.

Responsável por:
- Registrar eventos do sistema
- Histórico operacional seguro
- Escrita concorrente em disco
- Comunicação com EventBus
- Diagnóstico do núcleo

Arquitetura:
Genesis Core

Mark:
III - Matrix (Logging Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import copy
import threading

from collections import deque
from datetime import datetime
from pathlib import Path


from core.base.module import (
    Module,
    ModuleStatus
)



class Logger(Module):
    """
    Serviço central de logs do Genesis Core.

    Atua como camada de observabilidade
    de todos os módulos do sistema.
    """



    def __init__(self):

        super().__init__(
            "core.logger"
        )


        self.version = "3.0"


        self.event_bus = None


        self.log_folder = Path(
            "logs"
        )


        self.log_file = (
            self.log_folder /
            "genesis_core.log"
        )


        self.max_history = 1000


        self.history = deque(
            maxlen=self.max_history
        )


        self._lock = threading.RLock()



    # =====================================================
    # DEPENDÊNCIAS
    # =====================================================


    def connect_event_bus(
        self,
        event_bus
    ):

        self.event_bus = event_bus



    def set_event_bus(
        self,
        event_bus
    ):

        self.connect_event_bus(
            event_bus
        )



    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def initialize(self):

        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:

            self.log_folder.mkdir(
                parents=True,
                exist_ok=True
            )


            self._write(
                "BOOT",
                "Sistema de logs Genesis Core inicializado."
            )


            self.set_status(
                ModuleStatus.ONLINE
            )


            self.success(
                "Logger ONLINE"
            )


            self.emit(
                "LOGGER_STARTED"
            )


        except Exception as error:


            self.set_error(
                str(error)
            )


            self.error(
                f"Falha inicializando Logger: {error}"
            )



    def shutdown(self):

        self.info(
            "Logger encerrando."
        )


        self.emit(
            "LOGGER_STOPPED"
        )


        self.set_status(
            ModuleStatus.OFFLINE
        )



    # =====================================================
    # EVENTOS
    # =====================================================


    def emit(
        self,
        event,
        *args,
        **kwargs
    ):


        if self.event_bus:

            try:

                self.event_bus.emit(
                    event,
                    *args,
                    **kwargs
                )


            except Exception:

                pass



    # =====================================================
    # API PÚBLICA
    # =====================================================


    def debug(
        self,
        message
    ):

        self._write(
            "DEBUG",
            message
        )



    def info(
        self,
        message
    ):

        self._write(
            "INFO",
            message
        )



    def success(
        self,
        message
    ):

        self._write(
            "SUCCESS",
            message
        )



    def warning(
        self,
        message
    ):

        self._write(
            "WARNING",
            message
        )



    def error(
        self,
        message
    ):

        self._write(
            "ERROR",
            message
        )



    # =====================================================
    # ESCRITA
    # =====================================================


    def _write(
        self,
        level,
        message
    ):


        now = datetime.now()


        text = (
            f"[{now:%Y-%m-%d %H:%M:%S}] "
            f"[{level}] "
            f"{message}"
        )


        print(
            text
        )



        with self._lock:


            self.history.append(

                {

                    "time":
                        now.isoformat(),

                    "level":
                        level,

                    "message":
                        str(message)

                }

            )



            try:


                self.log_folder.mkdir(
                    parents=True,
                    exist_ok=True
                )


                with open(
                    self.log_file,
                    "a",
                    encoding="utf-8"
                ) as file:


                    file.write(
                        text + "\n"
                    )


                    file.flush()



            except Exception as error:


                print(
                    "[LOGGER FAILURE] "
                    f"{error}"
                )



    # =====================================================
    # DIAGNÓSTICO
    # =====================================================


    def get_history(self):

        with self._lock:

            return copy.deepcopy(
                list(self.history)
            )