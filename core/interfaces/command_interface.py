"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/command_interface.py

Descrição:
Interface de entrada textual do Genesis Core.

Responsável por receber comandos humanos
e encaminhar estímulos para a Matrix Cognitiva.

Não executa regras de negócio.

Fluxo:

Usuário
 ↓
CommandInterface
 ↓
Brain
 ↓
CognitivePipeline
 ↓
Executor


Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


import threading
import unicodedata


from core.base.module import (
    Module,
    ModuleStatus
)



class CommandInterface(Module):
    """
    Interface CLI assíncrona do Genesis Core.

    Atua apenas como camada de entrada.
    """



    def __init__(
        self,
        kernel
    ):
        super().__init__(
            "core.command_interface"
        )

        self.version = "3.3"

        self.kernel = kernel

        self.logger = getattr(
            kernel,
            "logger",
            None
        )

        self.running = False

        self._cli_thread = None

        self._lock = threading.RLock()



    # ==================================================
    # NORMALIZAÇÃO
    # ==================================================

    def _normalize(
        self,
        text
    ):

        if not text:
            return ""

        text = unicodedata.normalize(
            "NFD",
            text
        )

        text = "".join(
            ch
            for ch in text
            if unicodedata.category(ch) != "Mn"
        )

        return text.lower().strip()



    # ==================================================
    # CICLO DE VIDA
    # ==================================================

    def initialize(self):

        with self._lock:

            if self.is_online():
                return


            self.set_status(
                ModuleStatus.INITIALIZING
            )


            self.set_status(
                ModuleStatus.ONLINE
            )


            self.success(
                "Command Interface online."
            )



    def shutdown(self):

        with self._lock:

            self.running = False


            self.set_status(
                ModuleStatus.OFFLINE
            )


            self.info(
                "Command Interface encerrada."
            )



    # ==================================================
    # START
    # ==================================================

    def start_interface(
        self
    ):

        self.initialize()


        if self.running:
            return


        self.running = True


        self._cli_thread = threading.Thread(
            target=self._loop,
            name="GenesisCLI",
            daemon=True
        )


        self._cli_thread.start()



    # ==================================================
    # LOOP PRINCIPAL
    # ==================================================

    def _loop(
        self
    ):

        print("\n")
        print("=" * 45)
        print(" JARVIS GENESIS CORE - CLI")
        print(" Interface cognitiva ativa")
        print("=" * 45)


        while self.running:

            try:

                text = input(
                    "\nSenhor > "
                )


                text = text.strip()


                if not text:
                    continue


                command = self._normalize(
                    text
                )


                if command in (
                    "sair",
                    "exit"
                ):

                    self.exit()

                    break



                elif command in (
                    "status",
                    "diagnostico"
                ):

                    self.status()

                    continue



                elif command in (
                    "ajuda",
                    "help"
                ):

                    self.help()

                    continue



                else:

                    self.send_to_brain(
                        text
                    )


            except (
                KeyboardInterrupt,
                EOFError
            ):

                self.exit()

                break


            except Exception as error:

                self.error(
                    str(error)
                )



    # ==================================================
    # ENCAMINHAMENTO COGNITIVO
    # ==================================================

    def send_to_brain(
        self,
        text
    ):

        brain = getattr(
            self.kernel,
            "brain",
            None
        )


        if brain:

            result = brain.process(
                {
                    "source": "cli",
                    "input": text
                }
            )


            print(
                f"\nJARVIS > {result}"
            )


        else:

            print(
                "\n[!] Brain offline."
            )



    # ==================================================
    # COMANDOS BÁSICOS
    # ==================================================

    def help(self):

        print(
            """
Comandos:

 ajuda
 status
 sair

Qualquer outro texto será enviado
para a Matrix Cognitiva.
"""
        )



    def status(self):

        if hasattr(
            self.kernel,
            "diagnostics"
        ):

            self.kernel.diagnostics.display()

        else:

            print(
                "Diagnóstico indisponível."
            )



    def exit(self):

        print(
            "\nEncerrando Genesis Core..."
        )

        self.shutdown()


        if hasattr(
            self.kernel,
            "shutdown"
        ):

            threading.Thread(
                target=self.kernel.shutdown,
                daemon=True
            ).start()



    # ==================================================
    # LOG
    # ==================================================

    def info(
        self,
        message
    ):

        if self.logger:
            self.logger.info(message)



    def success(
        self,
        message
    ):

        if self.logger:
            self.logger.success(message)



    def error(
        self,
        message
    ):

        if self.logger:
            self.logger.error(message)