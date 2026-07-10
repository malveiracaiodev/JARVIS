"""
=========================================
JARVIS CORE

Arquivo:
system_monitor.py

Descrição:
Monitor de saúde do sistema.

Responsável por acompanhar o estado
dos módulos do JARVIS.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


from core.base.module import (
    Module,
    ModuleStatus
)


from core.events import SystemEvents





class SystemMonitor(Module):
    """
    Monitora o estado interno do JARVIS.
    """



    def __init__(
        self,
        kernel,
        logger,
        event_bus
    ):

        super().__init__(
            "System Monitor"
        )


        self.kernel = kernel

        self.logger = logger

        self.event_bus = event_bus

        self.health = 0





    # ==========================================================
    # Inicialização
    # ==========================================================


    def initialize(self):
        """
        Inicializa o monitor.
        """


        self.set_status(
            ModuleStatus.INITIALIZING
        )



        self.event_bus.subscribe(
            SystemEvents.READY,
            self.system_ready
        )



        self.set_status(
            ModuleStatus.ONLINE
        )



        self.logger.success(
            "System Monitor iniciado"
        )





    # ==========================================================
    # Encerramento
    # ==========================================================


    def shutdown(self):
        """
        Encerra o monitor.
        """


        self.event_bus.unsubscribe(
            SystemEvents.READY,
            self.system_ready
        )


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.logger.info(
            "System Monitor encerrado"
        )





    # ==========================================================
    # Eventos
    # ==========================================================


    def system_ready(self):
        """
        Recebe sinal de sistema pronto.
        """


        self.logger.info(
            "System Monitor recebeu SYSTEM READY"
        )


        self.check_health()





    # ==========================================================
    # Diagnóstico
    # ==========================================================


    def check_health(self):
        """
        Verifica saúde dos módulos.
        """


        online = 0


        total = len(
            self.kernel.modules
        )



        for module in self.kernel.modules:


            if module.is_online():

                online += 1



        self.health = int(

            (
                online
                /
                total

            )
            *
            100

        )



        self.logger.info(
            f"Saúde do sistema: {self.health}%"
        )



        return self.health