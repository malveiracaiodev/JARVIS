"""
=========================================
JARVIS CORE

Arquivo:
logger.py

Descrição:
Sistema de logs do JARVIS.

Responsável por registrar mensagens,
avisos, erros e informações do sistema.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


from pathlib import Path
from datetime import datetime


from core.base.module import Module, ModuleStatus



class Logger(Module):
    """
    Sistema central de registros do JARVIS.
    """



    LOG_FOLDER = Path("logs")

    LOG_FILE = (
        LOG_FOLDER /
        "jarvis.log"
    )



    def __init__(self):

        super().__init__(
            "Logger"
        )




    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):
        """
        Inicializa o sistema de logs.
        """

        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:

            self.LOG_FOLDER.mkdir(
                exist_ok=True
            )


            self._write(
                "BOOT",
                "Inicializando sistema de logs"
            )


            self.set_status(
                ModuleStatus.ONLINE
            )


            self.success(
                "Logger iniciado"
            )



        except Exception as error:


            self.set_error(
                str(error)
            )


            print(
                f"Falha no Logger: {error}"
            )





    def shutdown(self):
        """
        Encerra o Logger.
        """


        self.info(
            "Logger encerrado"
        )


        self.set_status(
            ModuleStatus.OFFLINE
        )





    # ==========================================================
    # Logs públicos
    # ==========================================================


    def debug(self, message: str):
        """
        Mensagens de diagnóstico.
        """

        self._write(
            "DEBUG",
            message
        )



    def info(self, message: str):
        """
        Informação normal.
        """

        self._write(
            "INFO",
            message
        )



    def success(self, message: str):
        """
        Operação concluída.
        """

        self._write(
            " OK ",
            message
        )



    def warning(self, message: str):
        """
        Avisos.
        """

        self._write(
            "WARN",
            message
        )



    def error(self, message: str):
        """
        Erros.
        """

        self._write(
            "FAIL",
            message
        )





    # ==========================================================
    # Escrita interna
    # ==========================================================


    def _write(
        self,
        level: str,
        message: str
    ):
        """
        Escreve no console e arquivo.
        """

        try:


            now = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            text = (
                f"[{now}] "
                f"[{level}] "
                f"{message}"
            )


            print(text)



            self.LOG_FOLDER.mkdir(
                exist_ok=True
            )



            with self.LOG_FILE.open(
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    text + "\n"
                )



        except Exception as error:


            print(
                "[LOGGER FAILURE]",
                error
            )