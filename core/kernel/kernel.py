"""
=========================================
JARVIS CORE

Arquivo:
core/kernel/kernel.py

Descrição:
Núcleo coordenador e orquestrador central do ciclo de vida da Matriz.
Acopla a mente cognitiva (Mind) e gerencia o shell de comandos.

Arquitetura:
Genesis Core

Mark:
III - Matrix

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
from core.runtime.engine import Runtime  # O motor correto que estabilizamos!
from core.mind.mind import Mind          # Mapeamento do sistema cognitivo


class Kernel:
    """
    Controlador central de injeção de dependências, gerenciamento de estado e boot global.
    """

    def __init__(self):
        self.name = "JARVIS CORE"
        self.version = "Matrix Mark III"
        self.status = "CREATED"
        self.started_at = None

        self.components = {}
        self.failed_components = {}
        
        self.registry = None
        self.logger = None
        self.event_bus = None
        self.config = None
        self.runtime = None
        self.mind = None

        self.build()

    def build(self):
        """Instancia e amarra todos os serviços e managers primordiais."""
        # 1. Registry (Catálogo do Kernel)
        self.registry = Registry()
        self.register("registry", self.registry, "module")

        # 2. Logger Oficial
        self.logger = Logger()
        self.register("logger", self.logger, "service")

        # 3. Barramento de Eventos (Event Bus)
        self.event_bus = EventBus(self.logger)
        self.logger.connect_event_bus(self.event_bus)
        self.register("event_bus", self.event_bus, "service")

        # 4. Config Manager
        self.config = ConfigManager(self.logger)
        self.register("config", self.config, "service")

        # 5. Service Manager
        service_manager = ServiceManager(self.logger)
        self.register("service_manager", service_manager, "service")

        # 6. Runtime Engine (Motor Assíncrono com Pool de Workers)
        workers_count = 2
        if hasattr(self.config, "get"):
            workers_count = self.config.get("runtime.workers", 2)
        
        if not isinstance(workers_count, int):
            workers_count = 2
        
        self.runtime = Runtime(
            logger=self.logger, 
            event_bus=self.event_bus, 
            worker_pool_size=workers_count
        )
        self.register("runtime", self.runtime, "module")

        # 7. Sistema Cognitivo (Mind) - Acoplado com o motor assíncrono de tarefas!
        self.mind = Mind(
            logger=self.logger,
            event_bus=self.event_bus,
            engine=self.runtime
        )
        self.register("mind", self.mind, "module")

        # 8. Plugin Manager
        plugin_manager = PluginManager(self.logger, self.event_bus, self.registry, self.config)
        self.register("plugin_manager", plugin_manager, "service")

    def register(self, name, component, category="module"):
        """Insere o componente no dicionário interno e no Registry global."""
        self.components[name] = component
        if self.registry is not None:
            self.registry.register(name, component, category)
        
        self.log(f"Componente mapeado e acoplado: {name}")

    def boot(self):
        """Dispara a inicialização em cascata de todos os componentes da malha."""
        self.status = "BOOTING"
        self.started_at = datetime.now()
        self.log("Carregando subsistemas da Matriz...")

        for name, component in self.components.items():
            # Evita reinicializar os serviços de infraestrutura básica
            if name in ["registry", "logger", "event_bus", "config"]:
                continue
            try:
                if hasattr(component, "initialize"):
                    component.initialize()
                elif hasattr(component, "start"):
                    component.start()
                
                self.log(f"Subsistema [{name}] alocado com sucesso: ONLINE")
            except Exception as error:
                self.failed_components[name] = str(error)
                if self.logger and hasattr(self.logger, "error"):
                    self.logger.error(f"Falha crítica no boot de [{name}]: {error}")
                else:
                    self.log(f"ERRO CRÍTICO em {name} -> {error}")

        self.status = "ONLINE"
        if self.event_bus and hasattr(self.event_bus, "emit"):
            self.event_bus.emit("system.ready", {"timestamp": str(self.started_at)})
        
        if self.logger and hasattr(self.logger, "success"):
            self.logger.success("Kernel da Matriz 100% ONLINE e em escuta ativa.")
        else:
            self.log("Kernel ONLINE e estável.")

    def shutdown(self):
        """Realiza o desligamento seguro em ordem reversa de injeção."""
        self.status = "SHUTDOWN"
        self.log("Desativando Kernel de forma segura...")

        for name, component in reversed(list(self.components.items())):
            try:
                if hasattr(component, "shutdown"):
                    component.shutdown()
                elif hasattr(component, "stop"):
                    component.stop()
                self.log(f"Subsistema [{name}] desconectado com segurança.")
            except Exception as error:
                self.log(f"Erro ao encerrar subsistema [{name}]: {error}")

        self.status = "OFFLINE"
        self.log("Kernel totalmente OFFLINE. Processos encerrados.")

    def uptime(self):
        if not self.started_at:
            return 0
        return (datetime.now() - self.started_at).total_seconds()

    def health(self):
        online_count = 0
        for component in self.components.values():
            if hasattr(component, "is_online") and component.is_online():
                online_count += 1
            elif hasattr(component, "get_status"):
                status = component.get_status()
                if hasattr(status, "name") and status.name == "ONLINE":
                    online_count += 1
                elif status == "ONLINE":
                    online_count += 1

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "total_components": len(self.components),
            "online_components": online_count,
            "failed_components": len(self.failed_components),
            "uptime_seconds": self.uptime()
        }

    def log(self, message):
        """Roteador inteligente de mensagens."""
        if self.logger and hasattr(self.logger, "info"):
            self.logger.info(message)
        else:
            print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [KERNEL] {message}")