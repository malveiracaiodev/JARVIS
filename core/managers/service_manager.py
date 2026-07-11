"""
=========================================
JARVIS CORE

Arquivo:
service_manager.py

Descrição:
Gerenciador central dos serviços
do núcleo do sistema.

Responsável por:
- Registrar serviços
- Inicializar serviços
- Controlar ciclo de vida
- Monitorar falhas

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.base.module import (
    Module,
    ModuleStatus
)





class ServiceManager(Module):


    """
    Gerenciador dos serviços internos
    do JARVIS.
    """



    def __init__(
        self,
        logger=None
    ):


        super().__init__(
            "core.service_manager"
        )


        self.version = "2.0"


        self.logger = logger


        self.services = {}


        self.failed_services = {}







    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )



        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log_success(
            "Service Manager iniciado"
        )







    def shutdown(self):


        self.shutdown_all()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Service Manager encerrado"
        )








    # ==========================================================
    # Registro
    # ==========================================================


    def register(
        self,
        name,
        service
    ):


        self.services[name] = service



        self.log_info(
            f"Serviço registrado: {name}"
        )








    def get(
        self,
        name
    ):


        return self.services.get(
            name
        )







    def get_all(self):


        return self.services







    # ==========================================================
    # Inicialização
    # ==========================================================


    def initialize_all(self):


        for name, service in self.services.items():


            try:


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



                self.log_success(
                    f"{name}: ONLINE"
                )



            except Exception as error:


                self.failed_services[name] = str(error)



                self.log_error(
                    f"{name}: ERRO -> {error}"
                )








    # ==========================================================
    # Encerramento
    # ==========================================================


    def shutdown_all(self):


        for name, service in reversed(
            list(
                self.services.items()
            )
        ):


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



                self.log_info(
                    f"{name}: encerrado"
                )



            except Exception as error:


                self.log_error(
                    f"Erro encerrando {name}: {error}"
                )








    # ==========================================================
    # Status
    # ==========================================================


    def status(self):


        online = 0



        for service in self.services.values():


            if hasattr(
                service,
                "is_online"
            ):


                if service.is_online():

                    online += 1





        return {


            "services":

            len(
                self.services
            ),



            "online":

            online,



            "failed":

            len(
                self.failed_services
            )


        }








    # ==========================================================
    # Logs
    # ==========================================================


    def log_info(
        self,
        message
    ):


        if self.logger:


            self.logger.info(
                message
            )



        else:


            print(
                "[SERVICE MANAGER]",
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



        else:


            print(
                "[SERVICE MANAGER][OK]",
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



        else:


            print(
                "[SERVICE MANAGER][ERROR]",
                message
            )