"""
=========================================
GENESIS CORE

Arquivo:
core/managers/service_manager.py

Descrição:
Gerenciador do ciclo de vida dos serviços
centrais do Genesis Core (Mark IV - Neural Lattice).

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from core.base.module import Module, ModuleStatus
from core.runtime.component_state import ComponentState


class ServiceManager(Module):
    """
    Controlador dos serviços internos do Core otimizado para a Neural Lattice.
    """

    def __init__(
        self,
        logger=None,
        registry=None
    ):
        super().__init__(
            "core.service_manager"
        )
        self.version = "4.0-Lattice"
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
            "Service Manager Mark IV (Neural Lattice) ONLINE."
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
                    f"Serviço já registrado na Lattice: {name}"
                )
                return False

            self.services[key] = service
            self.service_status[key] = str(ComponentState.REGISTERED)

        if self.registry:
            try:
                self.registry.register_service(
                    name,
                    service
                )
            except Exception as error:
                self.log_error(f"Erro ao registrar serviço no Registry: {error}")

        self.log_info(
            f"Serviço integrado ao Lattice: {name}"
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
            try:
                self.registry.unregister(
                    name
                )
            except Exception as error:
                self.log_error(f"Erro ao desregistrar do Registry: {error}")

        self.log_info(f"Serviço removido da Lattice: {name}")
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
                self.service_status[name] = str(ComponentState.BOOTING)

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

                self.service_status[name] = str(ComponentState.ONLINE)

                self.log_success(
                    f"Serviço online na Lattice: {name}"
                )

            except Exception as error:
                self.service_status[name] = str(ComponentState.FAILED)

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
                self.service_status[name] = str(ComponentState.SHUTDOWN)

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

                self.service_status[name] = str(ComponentState.OFFLINE)

                self.log_info(
                    f"Serviço encerrado: {name}"
                )

            except Exception as error:
                self.log_error(
                    f"Erro desligando {name}: {error}"
                )

    # ==================================================
    # ISOLAMENTO (Mark IV)
    # ==================================================

    def isolate_service(self, name):
        """Isola um serviço com comportamento anômalo para proteger o Core."""
        key = name.lower().strip()
        with self._lock:
            service = self.services.get(key)
            if not service:
                return False

            try:
                self.service_status[key] = str(ComponentState.ISOLATED)
                if hasattr(service, "stop"):
                    service.stop()
                elif hasattr(service, "shutdown"):
                    service.shutdown()

                self.log_info(f"[ISOLATED] Serviço isolado da malha: {name}")
                return True
            except Exception as error:
                self.log_error(f"Erro ao isolar serviço {name}: {error}")
                return False

    # ==================================================
    # DIAGNÓSTICO
    # ==================================================

    def status(self):
        with self._lock:
            online = sum(
                1
                for status
                in self.service_status.values()
                if status == str(ComponentState.ONLINE)
            )

            degraded = sum(
                1
                for status
                in self.service_status.values()
                if status == str(ComponentState.DEGRADED)
            )

            isolated = sum(
                1
                for status
                in self.service_status.values()
                if status == str(ComponentState.ISOLATED)
            )

            return {
                "total":
                    len(self.services),
                "online":
                    online,
                "degraded":
                    degraded,
                "isolated":
                    isolated,
                "failed":
                    len(self.failed_services),
                "states":
                    dict(self.service_status)
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
            if hasattr(self.logger, "success"):
                self.logger.success(msg)
            else:
                self.logger.info(msg)

    def log_error(
        self,
        msg
    ):
        if self.logger:
            self.logger.error(msg)