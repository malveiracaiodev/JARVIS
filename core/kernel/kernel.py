"""
=========================================
GENESIS CORE

Arquivo:
core/kernel/kernel.py

Descrição:
Núcleo coordenador central do Genesis Core.

Responsável por:
- Construção da Matriz
- Injeção de dependências
- Controle do ciclo de vida
- Registro de componentes
- Orquestração dos Managers
- Inicialização da inteligência

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


# ======================================================
# SERVICES
# ======================================================

from core.services.logger import Logger
from core.services.event_bus import EventBus
from core.services.config_manager import ConfigManager
from core.services.identity_manager import IdentityManager



# ======================================================
# MANAGERS
# ======================================================

from core.managers.registry import Registry
from core.managers.service_manager import ServiceManager
from core.managers.plugin_manager import PluginManager
from core.managers.tool_manager import ToolManager



# ======================================================
# RUNTIME / COGNITION
# ======================================================

from core.runtime.engine import Runtime
from core.mind.mind import Mind
from core.pipeline.pipeline_initializer import PipelineInitializer




class Kernel:
    """
    Orquestrador principal da Matriz Genesis.

    O Kernel não executa inteligência.
    Ele apenas constrói, conecta e controla
    o ciclo de vida dos módulos.
    """



    def __init__(self):

        self.name = "JARVIS CORE"

        self.version = "Genesis Core Mark III"

        self.status = "CREATED"

        self.started_at = None


        self.components = {}

        self.failed_components = {}



        # Serviços

        self.logger = None

        self.event_bus = None

        self.config = None

        self.identity = None



        # Managers

        self.registry = None

        self.service_manager = None

        self.plugin_manager = None

        self.tool_manager = None



        # Inteligência

        self.runtime = None

        self.pipeline = None

        self.mind = None



        self.build()



    # ==================================================
    # BUILD
    # ==================================================


    def build(self):


        self.registry = Registry()


        self.register(
            "registry",
            self.registry,
            "module"
        )



        self.logger = Logger()


        self.register(
            "logger",
            self.logger,
            "service"
        )



        self.event_bus = EventBus(
            self.logger
        )


        self.logger.connect_event_bus(
            self.event_bus
        )


        self.register(
            "event_bus",
            self.event_bus,
            "service"
        )



        self.config = ConfigManager(
            self.logger
        )


        self.register(
            "config",
            self.config,
            "service"
        )



        self.identity = IdentityManager(
            logger=self.logger,
            event_bus=self.event_bus
        )


        self.register(
            "identity",
            self.identity,
            "service"
        )



        self.service_manager = ServiceManager(
            logger=self.logger
        )


        self.register(
            "service_manager",
            self.service_manager,
            "module"
        )



        self.tool_manager = ToolManager(
            logger=self.logger
        )


        self.register(
            "tool_manager",
            self.tool_manager,
            "module"
        )



        workers = 2


        try:

            workers = self.config.get(
                "runtime",
                "workers",
                2
            )

        except Exception:

            pass



        if not isinstance(
            workers,
            int
        ):

            workers = 2



        self.runtime = Runtime(
            logger=self.logger,
            event_bus=self.event_bus,
            worker_pool_size=workers
        )


        self.register(
            "runtime",
            self.runtime,
            "module"
        )



        self.plugin_manager = PluginManager(
            logger=self.logger,
            event_bus=self.event_bus,
            registry=self.registry,
            config=self.config
        )


        self.register(
            "plugin_manager",
            self.plugin_manager,
            "module"
        )



        # ==================================================
        # THOUGHT ENGINE
        # ==================================================


        self.pipeline = PipelineInitializer(
            logger=self.logger,
            tool_manager=self.tool_manager
        ).build()



        self.register(
            "pipeline",
            self.pipeline,
            "module"
        )



        # ==================================================
        # MIND
        # ==================================================


        self.mind = Mind(
            logger=self.logger,
            event_bus=self.event_bus,
            engine=self.runtime,
            pipeline=self.pipeline
        )


        self.register(
            "mind",
            self.mind,
            "module"
        )




    # ==================================================
    # REGISTRY
    # ==================================================


    def register(
        self,
        name,
        component,
        category="module"
    ):


        self.components[name] = component



        if self.registry:

            try:

                self.registry.register(
                    name,
                    component,
                    category
                )


            except Exception as error:

                self.failed_components[name] = str(error)



        self.log(
            f"Componente acoplado: {name}"
        )




    # ==================================================
    # BOOT
    # ==================================================


    def boot(self):


        self.status = "BOOTING"

        self.started_at = datetime.now()



        self.log(
            "Inicializando Genesis Core Matrix..."
        )



        boot_order = [

            "logger",

            "event_bus",

            "config",

            "registry",

            "identity",

            "service_manager",

            "tool_manager",

            "runtime",

            "plugin_manager",

            "pipeline",

            "mind"

        ]



        for name in boot_order:


            component = self.components.get(
                name
            )


            if not component:

                continue



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
                    f"[ONLINE] {name}"
                )



            except Exception as error:


                self.failed_components[name] = str(
                    error
                )


                if self.logger:

                    self.logger.error(
                        f"Falha iniciando {name}: {error}"
                    )



        self.status = "ONLINE"



        if self.event_bus:

            try:

                self.event_bus.emit(
                    "system.ready",
                    {
                        "time":
                        datetime.now().isoformat()
                    }
                )


            except Exception:

                pass



        self.log(
            "Genesis Core Matrix ONLINE."
        )




    # ==================================================
    # SHUTDOWN
    # ==================================================


    def shutdown(self):


        self.status = "SHUTDOWN"


        self.log(
            "Encerrando Genesis Core..."
        )



        components = list(
            self.components.items()
        )


        components.reverse()



        for name, component in components:


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



                self.log(
                    f"[OFFLINE] {name}"
                )


            except Exception as error:


                self.log(
                    f"Erro encerrando {name}: {error}"
                )



        self.status = "OFFLINE"



        self.log(
            "Genesis Core desligado."
        )




    # ==================================================
    # HEALTH
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


            try:


                if hasattr(
                    component,
                    "is_online"
                ) and component.is_online():

                    online += 1



            except Exception:

                pass



        return {

            "name": self.name,

            "version": self.version,

            "status": self.status,

            "components": len(
                self.components
            ),

            "online": online,

            "failed": len(
                self.failed_components
            ),

            "uptime": self.uptime()

        }




    # ==================================================
    # LOG
    # ==================================================


    def log(
        self,
        message
    ):


        if self.logger:

            self.logger.info(
                message
            )

        else:

            print(
                f"[KERNEL] {message}"
            )