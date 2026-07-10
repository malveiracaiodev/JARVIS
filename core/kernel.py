"""
=========================================
JARVIS CORE

Arquivo:
kernel.py

Descrição:
Núcleo principal responsável por inicializar
e controlar todos os componentes do sistema.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


import time


from core.base.module import Module, ModuleStatus

from core.logger import Logger
from core.config_manager import ConfigManager
from core.event_bus import EventBus



class Kernel(Module):
    """
    Núcleo principal do JARVIS.

    Responsável por:
    - Inicializar módulos
    - Controlar ciclo de vida
    - Gerenciar estado do sistema
    """


    VERSION = "Mark I - Heartbeat"



    def __init__(self):
        """
        Inicializa o Kernel.
        """

        super().__init__("Kernel")


        self.start_time = None


        # ======================================================
        # Inicialização dos módulos principais
        # ======================================================


        self.logger = Logger()


        self.config = ConfigManager(
            self.logger
        )


        self.event_bus = EventBus(
            self.logger
        )


        # Ordem importa:
        # Logger -> Config -> Eventos

        self.modules = [

            self.logger,

            self.config,

            self.event_bus

        ]



    # ==========================================================
    # BOOT
    # ==========================================================


    def boot(self):
        """
        Processo principal de inicialização do JARVIS.
        """

        try:

            self.initialize()


        except Exception as error:


            print(
                "\n[CRITICAL] Falha durante inicialização:"
            )


            print(error)


            self.shutdown()



    # ==========================================================
    # INITIALIZE
    # ==========================================================


    def initialize(self):
        """
        Inicializa o Kernel e seus módulos.
        """


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.start_time = time.time()



        self._show_banner()



        for module in self.modules:


            module.initialize()



        self.set_status(
            ModuleStatus.ONLINE
        )


        self._finish_boot()





    # ==========================================================
    # SHUTDOWN
    # ==========================================================


    def shutdown(self):
        """
        Encerra todos os módulos.
        """


        if hasattr(self, "logger"):


            self.logger.warning(
                "Encerrando sistema..."
            )



        for module in reversed(self.modules):


            try:

                module.shutdown()


            except Exception as error:


                print(
                    f"Erro ao desligar {module.name}: {error}"
                )



        self.set_status(
            ModuleStatus.OFFLINE
        )





    # ==========================================================
    # BOOT FINAL
    # ==========================================================


    def _finish_boot(self):
        """
        Finaliza o processo de inicialização.
        """


        elapsed = (
            time.time()
            -
            self.start_time
        )



        self.logger.success(
            "Kernel iniciado"
        )


        self.logger.success(
            "Sistema Online"
        )



        user = self.config.get(
            "user",
            "name"
        )



        if user:


            self.logger.info(
                f"Bem-vindo, {user}."
            )



        self.logger.info(
            f"Tempo de inicialização: {elapsed:.2f}s"
        )



        print(
            "\nHello, Sir."
        )





    # ==========================================================
    # STATUS
    # ==========================================================


    def status(self):
        """
        Retorna o estado atual do Kernel.
        """

        return self.get_status()





    # ==========================================================
    # BANNER
    # ==========================================================


    def _show_banner(self):
        """
        Exibe a tela inicial do JARVIS.
        """


        print("=" * 45)


        print(
            "              JARVIS CORE"
        )


        print(
            f"         {self.VERSION}"
        )


        print("=" * 45)


        print()