"""
=========================================
GENESIS CORE

Arquivo:
core/runtime/boot_manager.py

Descrição:
Gerenciador oficial do ciclo de vida da
Genesis Matrix.

Responsável por:

- Registro de componentes
- Boot controlado
- Shutdown reverso
- Reinicialização
- Eventos de ciclo de vida
- Monitoramento de falhas

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime


class BootManager:

    def __init__(
        self,
        logger=None,
        event_bus=None,
        registry=None
    ):

        self.logger = logger
        self.event_bus = event_bus
        self.registry = registry

        self.components = {}
        self.failed = {}

        self.started_at = None

    # ==================================================
    # LOG
    # ==================================================

    def log(self, message):

        if self.logger:
            self.logger.info(message)
        else:
            print(f"[BOOT] {message}")

    # ==================================================
    # REGISTER
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

                self.failed[name] = str(error)

        self.log(f"Registrado: {name}")

    # ==================================================
    # BOOT
    # ==================================================

    def boot(self):

        self.started_at = datetime.now()

        self.log("Inicializando componentes...")

        if self.event_bus:

            try:
                self.event_bus.emit(
                    "system.boot.started",
                    {}
                )
            except Exception:
                pass

        for name, component in self.components.items():

            try:

                if hasattr(component, "initialize"):
                    component.initialize()

                elif hasattr(component, "start"):
                    component.start()

                self.log(f"[ONLINE] {name}")

                if self.event_bus:

                    try:
                        self.event_bus.emit(
                            "system.component.online",
                            {
                                "component": name
                            }
                        )
                    except Exception:
                        pass

            except Exception as error:

                self.failed[name] = str(error)

                self.log(f"[FAILED] {name}: {error}")

                if self.event_bus:

                    try:
                        self.event_bus.emit(
                            "system.component.failed",
                            {
                                "component": name,
                                "error": str(error)
                            }
                        )
                    except Exception:
                        pass

        if self.event_bus:

            try:
                self.event_bus.emit(
                    "system.ready",
                    {}
                )
            except Exception:
                pass

        self.log("Boot finalizado.")

    # ==================================================
    # SHUTDOWN
    # ==================================================

    def shutdown(self):

        self.log("Encerrando componentes...")

        components = list(
            self.components.items()
        )

        components.reverse()

        for name, component in components:

            try:

                if hasattr(component, "shutdown"):
                    component.shutdown()

                elif hasattr(component, "stop"):
                    component.stop()

                self.log(f"[OFFLINE] {name}")

            except Exception as error:

                self.log(
                    f"Erro desligando {name}: {error}"
                )

        if self.event_bus:

            try:
                self.event_bus.emit(
                    "system.shutdown.finished",
                    {}
                )
            except Exception:
                pass

        self.log("Shutdown concluído.")

    # ==================================================
    # RESTART
    # ==================================================

    def restart_component(self, name):

        component = self.components.get(name)

        if component is None:
            return False

        try:

            if hasattr(component, "shutdown"):
                component.shutdown()

            elif hasattr(component, "stop"):
                component.stop()

            if hasattr(component, "initialize"):
                component.initialize()

            elif hasattr(component, "start"):
                component.start()

            self.log(f"Reiniciado: {name}")

            return True

        except Exception as error:

            self.failed[name] = str(error)

            self.log(
                f"Falha reiniciando {name}: {error}"
            )

            return False

    # ==================================================
    # HEALTH
    # ==================================================

    def health(self):

        return {

            "components": len(self.components),

            "failed": len(self.failed),

            "uptime": (
                datetime.now() - self.started_at
            ).total_seconds()
            if self.started_at
            else 0

        }