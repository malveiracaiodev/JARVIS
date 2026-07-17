"""
=========================================
JARVIS CORE

Arquivo:
core/managers/service_manager.py

Descrição:
Gerenciador do ciclo de vida dos serviços
centrais do Genesis Core.

Responsável por:
- Registrar serviços
- Inicializar módulos
- Controlar falhas
- Encerrar componentes

Arquitetura:
Genesis Core

Mark:
III - Matrix (Service Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import threading


from core.base.module import (
    Module,
    ModuleStatus
)





class ServiceManager(Module):

    """
    Controlador dos serviços internos do Core.
    """



    def __init__(
        self,
        logger=None,
        registry=None
    ):


        super().__init__(
            "core.service_manager"
        )


        self.version = "3.5"


        self.logger = logger

        self.registry = registry



        self.services = {}

        self.failed_services = {}

        self.service_status = {}



        self._lock = threading.RLock()





    # ==================================================
    # CICLO DE VIDA
    # ==================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log_success(
            "Service Manager Mark III ONLINE."
        )





    def shutdown(self):


        self.shutdown_all()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Service Manager encerrado."
        )





    # ==================================================
    # REGISTRO
    # ==================================================


    def register(
        self,
        name,
        service
    ):


        key = name.lower().strip()



        with self._lock:


            if key in self.services:


                self.log_info(
                    f"Serviço já registrado: {name}"
                )


                return False




            self.services[key] = service


            self.service_status[key] = "REGISTERED"



        if self.registry:


            self.registry.register_service(
                name,
                service
            )



        self.log_info(
            f"Serviço registrado: {name}"
        )


        return True





    def unregister(
        self,
        name
    ):


        key = name.lower().strip()



        with self._lock:


            if key not in self.services:

                return False



            del self.services[key]


            self.service_status.pop(
                key,
                None
            )



        if self.registry:


            self.registry.unregister(
                name
            )



        return True





    # ==================================================
    # CONSULTA
    # ==================================================


    def get(
        self,
        name
    ):


        with self._lock:


            return self.services.get(
                name.lower().strip()
            )





    def get_all(self):


        with self._lock:


            return dict(
                self.services
            )





    # ==================================================
    # BOOT DOS SERVIÇOS
    # ==================================================


    def initialize_all(self):


        with self._lock:


            items = list(
                self.services.items()
            )



        for name, service in items:


            try:


                self.service_status[name] = "INITIALIZING"



                if hasattr(
                    service,
                    "initialize"
                ):


                    service.initialize()



                elif hasattr(
                    service,
                    "start"
                ):


                    service.start()




                self.service_status[name] = "ONLINE"



                self.log_success(
                    f"Serviço online: {name}"
                )



            except Exception as error:



                self.service_status[name] = "ERROR"



                self.failed_services[name] = str(
                    error
                )


                self.log_error(
                    f"Falha no serviço {name}: {error}"
                )





    def shutdown_all(self):


        with self._lock:


            items = list(
                self.services.items()
            )[::-1]



        for name, service in items:


            try:


                if hasattr(
                    service,
                    "shutdown"
                ):


                    service.shutdown()



                elif hasattr(
                    service,
                    "stop"
                ):


                    service.stop()



                self.service_status[name] = "OFFLINE"



                self.log_info(
                    f"Serviço encerrado: {name}"
                )



            except Exception as error:


                self.log_error(
                    f"Erro desligando {name}: {error}"
                )





    # ==================================================
    # DIAGNÓSTICO
    # ==================================================


    def status(self):


        with self._lock:


            online = sum(


                1

                for status

                in self.service_status.values()

                if status == "ONLINE"


            )



            return {


                "total":

                    len(self.services),


                "online":

                    online,


                "failed":

                    len(self.failed_services)


            }





    # ==================================================
    # LOG
    # ==================================================


    def log_info(
        self,
        msg
    ):

        if self.logger:

            self.logger.info(msg)





    def log_success(
        self,
        msg
    ):

        if self.logger:

            self.logger.success(msg)





    def log_error(
        self,
        msg
    ):

        if self.logger:

            self.logger.error(msg)