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


from core.base.module import (
    Module,
    ModuleStatus
)


from core.logger import Logger

from core.config_manager import ConfigManager

from core.event_bus import EventBus

from core.memory_manager import MemoryManager

from core.system_monitor import SystemMonitor


from core.events import SystemEvents





class Kernel(Module):
    """
    Núcleo principal do JARVIS.

    Responsável por:
    - Inicializar módulos
    - Controlar ciclo de vida
    - Gerenciar comunicação
    - Controlar memória
    - Monitorar saúde
    """



    VERSION = "Mark I - Heartbeat"





    def __init__(self):

        super().__init__(
            "Kernel"
        )


        self.start_time = None



        # ======================================================
        # Módulos principais
        # ======================================================


        self.logger = Logger()



        self.config = ConfigManager(
            self.logger
        )



        self.event_bus = EventBus(
            self.logger
        )



        self.memory = MemoryManager(
            self.logger,
            self.event_bus
        )



        self.monitor = SystemMonitor(
            self,
            self.logger,
            self.event_bus
        )



        # Ordem de inicialização

        self.modules = [

            self.logger,

            self.config,

            self.event_bus,

            self.memory,

            self.monitor

        ]





    # ==========================================================
    # BOOT
    # ==========================================================


    def boot(self):

        """
        Inicia o JARVIS.
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
        Inicializa todos os módulos.
        """


        self.set_status(
            ModuleStatus.INITIALIZING
        )



        self.start_time = time.time()



        self._show_banner()



        for module in self.modules:

            module.initialize()



        # Primeiro evento do sistema

        self.event_bus.emit(
            SystemEvents.START
        )



        # Primeira memória do sistema

        self.memory.remember(

            "system.start",

            "JARVIS iniciou o processo de inicialização"

        )



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


        if hasattr(
            self,
            "event_bus"
        ):


            self.event_bus.emit(
                SystemEvents.SHUTDOWN
            )



        if hasattr(
            self,
            "logger"
        ):


            self.logger.warning(
                "Encerrando sistema..."
            )



        for module in reversed(
            self.modules
        ):


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
    # FINALIZAÇÃO DO BOOT
    # ==========================================================


    def _finish_boot(self):

        """
        Finaliza inicialização.
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



        self.event_bus.emit(
            SystemEvents.READY
        )



        self.memory.remember(

            "system.ready",

            "JARVIS está online e operacional"

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

        return self.get_status()





    # ==========================================================
    # BANNER
    # ==========================================================


    def _show_banner(self):

        print(
            "=" * 45
        )


        print(
            "              JARVIS CORE"
        )


        print(
            f"         {self.VERSION}"
        )


        print(
            "=" * 45
        )


        print()