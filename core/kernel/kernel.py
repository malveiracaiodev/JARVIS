"""
=========================================
JARVIS CORE

Arquivo:
kernel.py

Descrição:
Núcleo coordenador do sistema.

Responsável por:
- Criar componentes principais
- Controlar boot
- Registrar componentes
- Gerenciar ciclo de vida

Arquitetura:
Genesis Core

Mark:
II - Evolution Stable

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.services.logger import Logger
from core.services.event_bus import EventBus
from core.services.config_manager import ConfigManager


from core.managers.registry import Registry
from core.managers.service_manager import ServiceManager
from core.managers.plugin_manager import PluginManager





class Kernel:



    def __init__(self):


        self.name = "JARVIS CORE"


        self.version = "Genesis Mark II"



        self.status = "CREATED"


        self.started_at = None



        self.components = {}


        self.failed_components = {}



        self.registry = None



        self.build()






    # ==================================================
    # CONSTRUÇÃO DO SISTEMA
    # ==================================================


    def build(self):


        self.log(
            "Construindo núcleo..."
        )



        # ==============================================
        # Registry
        # ==============================================


        registry = Registry()



        self.registry = registry



        self.register(
            "registry",
            registry,
            "module"
        )




        # ==============================================
        # Logger
        # ==============================================


        logger = Logger()



        self.register(
            "logger",
            logger,
            "service"
        )





        # ==============================================
        # Event Bus
        # ==============================================


        event_bus = EventBus(
            logger
        )



        logger.connect_event_bus(
            event_bus
        )



        self.register(
            "event_bus",
            event_bus,
            "service"
        )






        # ==============================================
        # Config Manager
        # ==============================================


        config = ConfigManager(
            logger
        )



        self.register(
            "config",
            config,
            "service"
        )






        # ==============================================
        # Service Manager
        # ==============================================


        service_manager = ServiceManager(
            logger
        )



        self.register(
            "service_manager",
            service_manager,
            "service"
        )






        # ==============================================
        # Plugin Manager
        # ==============================================


        plugin_manager = PluginManager(
            logger,
            event_bus,
            registry,
            config
        )



        self.register(
            "plugin_manager",
            plugin_manager,
            "service"
        )









    # ==================================================
    # REGISTRO
    # ==================================================


    def register(
        self,
        name,
        component,
        category="module"
    ):



        self.components[name] = component





        if self.registry is not None:



            self.registry.register(
                name,
                component,
                category
            )





        self.log(
            f"Registrado: {name}"
        )









    # ==================================================
    # BOOT
    # ==================================================


    def boot(self):


        self.status = "BOOTING"



        self.started_at = datetime.now()



        self.log(
            "Inicializando Kernel..."
        )





        for name, component in self.components.items():



            try:



                if hasattr(
                    component,
                    "initialize"
                ):



                    component.initialize()




                elif hasattr(
                    component,
                    "start"
                ):



                    component.start()





                self.log(
                    f"{name}: ONLINE"
                )





            except Exception as error:



                self.failed_components[name] = str(
                    error
                )



                self.log(
                    f"{name}: ERRO -> {error}"
                )







        self.status = "ONLINE"



        self.log(
            "Kernel ONLINE"
        )









    # ==================================================
    # SHUTDOWN
    # ==================================================


    def shutdown(self):


        self.status = "SHUTDOWN"





        for name, component in reversed(
            list(
                self.components.items()
            )
        ):



            try:



                if hasattr(
                    component,
                    "shutdown"
                ):



                    component.shutdown()





                elif hasattr(
                    component,
                    "stop"
                ):



                    component.stop()





            except Exception as error:



                self.log(
                    f"Erro encerrando {name}: {error}"
                )






        self.status = "OFFLINE"



        self.log(
            "Kernel OFFLINE"
        )









    # ==================================================
    # DIAGNÓSTICO
    # ==================================================


    def uptime(self):


        if not self.started_at:


            return 0




        return (

            datetime.now()

            -

            self.started_at

        ).total_seconds()







    def health(self):


        online = 0





        for component in self.components.values():



            if hasattr(
                component,
                "is_online"
            ):



                if component.is_online():


                    online += 1







        return {



            "name":

            self.name,



            "version":

            self.version,



            "status":

            self.status,



            "components":

            len(
                self.components
            ),



            "online":

            online,



            "failed":

            len(
                self.failed_components
            ),



            "uptime":

            self.uptime()


        }









    # ==================================================
    # LOG
    # ==================================================


    def log(
        self,
        message
    ):



        print(


            f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "

            f"[KERNEL] "

            f"{message}"


        )