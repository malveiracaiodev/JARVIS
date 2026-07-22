"""
=========================================
GENESIS CORE

Arquivo:
core/kernel/kernel.py

Descrição:
Núcleo coordenador central do Genesis Core.

Responsável por:
- Construção da Matriz
- Registro de componentes
- Controle do ciclo de vida
- Inicialização dos serviços
- Orquestração dos módulos

Arquitetura:
Genesis Core

Mark:
V - Evolution

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
from core.services.ai_service import AIService



# ======================================================
# MANAGERS
# ======================================================

from core.managers.registry import Registry
from core.managers.service_manager import ServiceManager
from core.managers.plugin_manager import PluginManager
from core.managers.tool_manager import ToolManager



# ======================================================
# COGNITION
# ======================================================

from core.runtime.engine import Runtime
from core.mind.mind import Mind
from core.pipeline.pipeline_initializer import PipelineInitializer




class Kernel:
    """
    Orquestrador central do Genesis Core.

    O Kernel não pensa.

    Ele apenas cria, conecta
    e controla o organismo.
    """



    def __init__(self):

        self.name = "JARVIS CORE"

        self.version = (
            "Genesis Core Mark V - Evolution"
        )

        self.status = "CREATED"

        self.started_at = None


        self.components = {}

        self.failed_components = {}


        # Serviços

        self.logger = None
        self.event_bus = None
        self.config = None
        self.identity = None
        self.ai_service = None


        # Managers

        self.registry = None
        self.service_manager = None
        self.tool_manager = None
        self.plugin_manager = None


        # Cognição

        self.runtime = None
        self.pipeline = None
        self.mind = None


        self.build()



    # ==================================================
    # BUILD
    # ==================================================

    def build(self):


        # Registry

        self.registry = Registry()

        self.register(
            "registry",
            self.registry,
            "module"
        )



        # Logger

        self.logger = Logger()

        self.register(
            "logger",
            self.logger,
            "service"
        )



        # Event Bus

        self.event_bus = EventBus(
            self.logger
        )


        if hasattr(
            self.logger,
            "connect_event_bus"
        ):

            self.logger.connect_event_bus(
                self.event_bus
            )


        self.register(
            "event_bus",
            self.event_bus,
            "service"
        )



        # Config

        self.config = ConfigManager(
            self.logger
        )


        self.register(
            "config",
            self.config,
            "service"
        )



        # Identity

        self.identity = IdentityManager(
            logger=self.logger,
            event_bus=self.event_bus
        )


        self.register(
            "identity",
            self.identity,
            "service"
        )



        # ==================================================
        # IA
        # ==================================================

        self.ai_service = AIService()


        self.register(
            "ai_service",
            self.ai_service,
            "service"
        )



        # ==================================================
        # MANAGERS
        # ==================================================

        self.service_manager = ServiceManager(
            logger=self.logger
        )


        self.register(
            "service_manager",
            self.service_manager,
            "manager"
        )



        self.tool_manager = ToolManager(
            logger=self.logger
        )


        self.register(
            "tool_manager",
            self.tool_manager,
            "manager"
        )



        # ==================================================
        # RUNTIME
        # ==================================================

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
            "runtime"
        )



        # ==================================================
        # PLUGINS
        # ==================================================

        self.plugin_manager = PluginManager(
            logger=self.logger,
            event_bus=self.event_bus,
            registry=self.registry,
            config=self.config
        )


        self.register(
            "plugin_manager",
            self.plugin_manager,
            "manager"
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
            "cognitive"
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
            "cognitive"
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



        if self.registry and name != "registry":

            try:

                self.registry.register(
                    name,
                    component,
                    category
                )

            except Exception as error:

                self.failed_components[name] = str(
                    error
                )



        self.log(
            f"Componente acoplado: {name}"
        )



    # ==================================================
    # ACCESS
    # ==================================================

    def get(
        self,
        name
    ):

        return self.components.get(
            name
        )



    def has(
        self,
        name
    ):

        return name in self.components



    def list_components(self):

        return list(
            self.components.keys()
        )



    # ==================================================
    # BOOT
    # ==================================================

    def boot(self):


        self.status = "BOOTING"

        self.started_at = datetime.now()



        self.log(
            "Inicializando Genesis Core Evolution..."
        )



        order = [

            "logger",
            "event_bus",
            "config",
            "registry",
            "identity",
            "ai_service",
            "service_manager",
            "tool_manager",
            "runtime",
            "plugin_manager",
            "pipeline",
            "mind"

        ]



        for name in order:


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


                self.log(
                    f"[ERRO] {name}: {error}"
                )



        self.status = "ONLINE"



        self.log(
            "Genesis Core Evolution ONLINE."
        )



    # ==================================================
    # SHUTDOWN
    # ==================================================

    def shutdown(self):


        self.status = "SHUTDOWN"


        self.log(
            "Encerrando Genesis Core..."
        )


        for name, component in reversed(
            list(self.components.items())
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

        return {

            "name":
                self.name,

            "version":
                self.version,

            "status":
                self.status,

            "components":
                len(self.components),

            "failed":
                len(self.failed_components),

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


        if self.logger:

            self.logger.info(
                message
            )

        else:

            print(
                f"[KERNEL] {message}"
            )