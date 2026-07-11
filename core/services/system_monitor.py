"""
=========================================
JARVIS CORE

Arquivo:
system_monitor.py

Descrição:
Monitor de saúde do sistema.

Responsável por:
- Verificar módulos
- Calcular saúde operacional
- Detectar falhas

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime



from core.base.module import (
    Module,
    ModuleStatus
)



from core.events import SystemEvents






class SystemMonitor(Module):


    """
    Monitora a saúde interna
    do JARVIS.
    """



    def __init__(
        self,
        kernel=None,
        logger=None,
        event_bus=None
    ):


        super().__init__(
            "core.system_monitor"
        )


        self.version = "2.0"


        self.kernel = kernel


        self.logger = logger


        self.event_bus = event_bus



        self.health = 0


        self.history = []








    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )



        if self.event_bus:


            self.event_bus.subscribe(
                SystemEvents.READY,
                self.system_ready
            )



        self.set_status(
            ModuleStatus.ONLINE
        )



        self.log_success(
            "System Monitor iniciado"
        )







    def shutdown(self):


        if self.event_bus:


            self.event_bus.unsubscribe(
                SystemEvents.READY,
                self.system_ready
            )



        self.set_status(
            ModuleStatus.OFFLINE
        )



        self.log_info(
            "System Monitor encerrado"
        )







    # ==========================================================
    # Eventos
    # ==========================================================


    def system_ready(
        self,
        *args,
        **kwargs
    ):


        self.log_info(
            "Sistema pronto. Iniciando diagnóstico."
        )


        self.check_health()







    # ==========================================================
    # Diagnóstico
    # ==========================================================


    def check_health(self):


        if not self.kernel:


            return 0



        modules = self.kernel.modules



        total = len(
            modules
        )



        if total == 0:


            self.health = 0


            return 0





        online = 0



        for module in modules:


            if module.is_online():


                online += 1





        self.health = int(

            (
                online /
                total
            )
            *
            100

        )



        report = {


            "health":
            self.health,


            "online":
            online,


            "total":
            total,


            "time":
            datetime.now().isoformat()

        }



        self.history.append(
            report
        )



        self.log_info(
            f"Saúde do sistema: {self.health}%"
        )



        self.emit(
            SystemEvents.HEALTH_CHECK,
            report
        )



        return self.health








    def get_health(self):


        return self.health






    def get_history(self):


        return self.history







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