"""
=========================================
JARVIS CORE

Arquivo:
logger.py

Descrição:
Sistema central de logs do JARVIS.

Responsável por:
- Registrar eventos do sistema
- Registrar avisos e erros
- Histórico operacional
- Comunicação com EventBus

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from pathlib import Path
from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)




class Logger(Module):


    """
    Serviço central de logs.
    """



    def __init__(self):


        super().__init__(
            "Logger"
        )


        self.version = "2.1"


        self.event_bus = None



        self.log_folder = Path(
            "logs"
        )


        self.log_file = (

            self.log_folder /
            "jarvis.log"

        )


        self.history = []


        self.max_history = 500





    # =====================================================
    # Dependências
    # =====================================================


    def connect_event_bus(
        self,
        event_bus
    ):


        self.event_bus = event_bus





    # =====================================================
    # Ciclo de vida
    # =====================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:


            self.log_folder.mkdir(
                exist_ok=True
            )


            self._write(

                "BOOT",

                "Sistema de logs inicializado"

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





    def shutdown(self):


        self.info(
            "Logger encerrando"
        )


        self.emit(
            "LOGGER_STOPPED"
        )


        self.set_status(
            ModuleStatus.OFFLINE
        )





    # =====================================================
    # Eventos
    # =====================================================


    def emit(
        self,
        event
    ):


        if self.event_bus:


            try:

                self.event_bus.emit(
                    event
                )


            except Exception:

                pass





    # =====================================================
    # API pública
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
            " OK ",
            message
        )




    def warning(
        self,
        message
    ):

        self._write(
            "WARN",
            message
        )




    def error(
        self,
        message
    ):

        self._write(
            "FAIL",
            message
        )





    # =====================================================
    # Escrita
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



        print(text)



        self.history.append(

            {

                "time":
                now.isoformat(),

                "level":
                level,

                "message":
                message

            }

        )



        if len(self.history) > self.max_history:

            self.history.pop(0)




        try:


            self.log_folder.mkdir(
                exist_ok=True
            )


            with self.log_file.open(

                "a",

                encoding="utf-8"

            ) as file:


                file.write(
                    text + "\n"
                )



        except Exception as error:


            print(
                "[LOGGER ERROR]",
                error
            )





    # =====================================================
    # Diagnóstico
    # =====================================================


    def get_history(self):

        return self.history