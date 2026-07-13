"""
=========================================
JARVIS CORE

Arquivo:
service_manager.py

Descrição:
Orquestrador de ciclo de vida e tratamento de falhas para serviços do Core.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from core.base.module import Module, ModuleStatus


class ServiceManager(Module):
    """
    Gerenciador encarregado de carregar, monitorar e derrubar serviços sob demanda.
    """

    def __init__(self, logger=None):
        super().__init__("core.service_manager")
        self.version = "3.0"
        self.logger = logger
        self.services = {}
        self.failed_services = {}
        self._lock = threading.RLock()

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        self.set_status(ModuleStatus.ONLINE)
        self.success("Service Manager ativado com barramento concorrente seguro")

    def shutdown(self):
        self.shutdown_all()
        self.set_status(ModuleStatus.OFFLINE)
        self.info("Service Manager encerrado.")

    def register(self, name, service):
        with self._lock:
            self.services[name] = service
            self.info(f"Serviço acoplado à malha: {name}")

    def get(self, name):
        with self._lock:
            return self.services.get(name)

    def get_all(self):
        with self._lock:
            return dict(self.services)

    def initialize_all(self):
        # Tira snapshot das chaves sob lock para evitar deadlock na inicialização interna
        with self._lock:
            items = list(self.services.items())

        for name, service in items:
            try:
                if hasattr(service, "initialize"):
                    service.initialize()
                elif hasattr(service, "start"):
                    service.start()
                self.success(f"Serviço ativado com sucesso: {name}")
            except Exception as error:
                with self._lock:
                    self.failed_services[name] = str(error)
                self.error(f"Falha crítica no serviço {name}: {str(error)}")

    def shutdown_all(self):
        with self._lock:
            # Desligamento em ordem estritamente inversa à inicialização
            items = list(self.services.items())[::-1]

        for name, service in items:
            try:
                if hasattr(service, "shutdown"):
                    service.shutdown()
                elif hasattr(service, "stop"):
                    service.stop()
                self.info(f"Serviço encerrado de forma controlada: {name}")
            except Exception as error:
                self.error(f"Exceção detectada no shutdown de {name}: {str(error)}")

    def status(self):
        with self._lock:
            online = sum(1 for s in self.services.values() if hasattr(s, "is_online") and s.is_online())
            return {
                "services": len(self.services),
                "online": online,
                "failed": len(self.failed_services)
            }

    def info(self, msg):
        if self.logger: self.logger.info(msg)
    def success(self, msg):
        if self.logger: self.logger.success(msg)
    def error(self, msg):
        if self.logger: self.logger.error(msg)