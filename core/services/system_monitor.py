"""
=========================================
JARVIS CORE

Arquivo:
core/services/system_monitor.py

Descrição:
Monitor de saúde do Genesis Core.

Responsável por:
- Diagnóstico de módulos
- Telemetria de hardware
- Avaliação operacional
- Histórico de saúde do sistema

Arquitetura:
Genesis Core

Mark:
III - Matrix (Monitoring Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import copy
import threading


from datetime import datetime
from collections import deque


try:
    import psutil

except ImportError:
    psutil = None



from core.base.module import (
    Module,
    ModuleStatus
)


from core.events import SystemEvents





class SystemMonitor(Module):
    """
    Monitora saúde interna do Genesis Core.
    """



    def __init__(
        self,
        kernel=None,
        logger=None,
        event_bus=None,
        max_history=200
    ):


        super().__init__(
            "core.system_monitor"
        )


        self.version = "3.0"


        self.kernel = kernel

        self.logger = logger

        self.event_bus = event_bus



        self.health = 100



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


        try:


            if self.event_bus:


                self.event_bus.subscribe(
                    SystemEvents.READY,
                    self.system_ready
                )



            self.set_status(
                ModuleStatus.ONLINE
            )


            self.log_success(
                "System Monitor Mark III ONLINE."
            )



        except Exception as error:


            self.set_error(
                str(error)
            )


            self.log_error(
                str(error)
            )





    def shutdown(self):


        if self.event_bus:


            try:

                self.event_bus.unsubscribe(
                    SystemEvents.READY,
                    self.system_ready
                )


            except Exception:

                pass



        with self._lock:

            self.history.clear()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "System Monitor encerrado."
        )





    # ======================================================
    # EVENTOS
    # ======================================================


    def system_ready(
        self,
        *args,
        **kwargs
    ):


        self.log_info(
            "Sistema pronto. Executando diagnóstico."
        )


        self.check_health()





    # ======================================================
    # DIAGNÓSTICO
    # ======================================================


    def check_health(self):


        with self._lock:


            software = self.check_modules()


            hardware = self.check_hardware()



            penalty = 0



            if hardware["cpu_percent"] > 90:

                penalty += 15



            if hardware["ram_percent"] > 90:

                penalty += 20



            if hardware["disk_percent"] > 95:

                penalty += 10




            self.health = max(

                0,

                min(

                    100,

                    int(
                        software["score"]
                        -
                        penalty
                    )

                )

            )



            report = {


                "health":

                    self.health,


                "software":

                    software,


                "hardware":

                    hardware,


                "time":

                    datetime.now()
                    .isoformat()

            }



            self.history.append(
                report
            )




            if self.health < 70:


                self.log_error(
                    (
                        "Sistema degradado: "
                        f"{self.health}%"
                    )
                )


                self.emit(
                    "SYSTEM_HEALTH_DEGRADED",
                    report
                )


            else:


                self.log_info(
                    (
                        "Saúde do sistema: "
                        f"{self.health}%"
                    )
                )



            self.emit(
                SystemEvents.HEALTH_CHECK,
                report
            )



            return self.health





    def check_modules(self):


        modules = []


        if self.kernel:


            modules = getattr(
                self.kernel,
                "modules",
                []
            )



        total = len(
            modules
        )


        online = 0


        degraded = 0



        for module in modules:


            try:


                if hasattr(
                    module,
                    "is_online"
                ) and module.is_online():


                    online += 1



                    if getattr(
                        module,
                        "errors",
                        0
                    ) > 5:

                        degraded += 1



            except Exception:

                degraded += 1





        if total == 0:


            score = 100



        else:


            score = (
                online /
                total
            ) * 100



            score -= (
                degraded /
                total
            ) * 50



        return {


            "total_modules":
                total,


            "online":
                online,


            "degraded":
                degraded,


            "score":
                max(
                    0,
                    score
                )

        }





    def check_hardware(self):


        result = {


            "cpu_percent":
                0,


            "ram_percent":
                0,


            "disk_percent":
                0,


            "temperature":
                None

        }



        if not psutil:

            return result




        try:


            result["cpu_percent"] = (
                psutil.cpu_percent()
            )


            result["ram_percent"] = (
                psutil.virtual_memory()
                .percent
            )


            result["disk_percent"] = (
                psutil.disk_usage("/")
                .percent
            )



            try:


                temps = (
                    psutil.sensors_temperatures()
                )


                if temps:

                    first = next(
                        iter(
                            temps.values()
                        )
                    )


                    if first:

                        result["temperature"] = (
                            first[0]
                            .current
                        )


            except Exception:

                pass



        except Exception:

            pass



        return result





    # ======================================================
    # CONSULTA
    # ======================================================


    def get_health(self):

        with self._lock:

            return self.health





    def get_history(self):


        with self._lock:


            return copy.deepcopy(
                list(self.history)
            )





    def get_report(self):


        return {


            "health":
                self.health,


            "history":
                self.get_history()

        }





    # ======================================================
    # AUXILIARES
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