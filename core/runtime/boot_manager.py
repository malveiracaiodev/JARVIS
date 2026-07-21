"""
=========================================
GENESIS CORE

Arquivo:
core/runtime/boot_manager.py

Descrição:
Gerenciador oficial do ciclo de vida da
Genesis Matrix (Mark IV - Neural Lattice).

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from core.runtime.component_state import ComponentState


class BootManager:
    """
    Gerenciador de Boot Mark IV com suporte a Lattice Nodes,
    isolamento de falhas e estados adaptativos.
    """

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
        self.states = {}
        self.failed = {}
        self.started_at = None

    # ==================================================
    # LOG
    # ==================================================

    def log(self, message):
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[BOOT-LATTICE] {message}")

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
        self.states[name] = ComponentState.REGISTERED

        if self.registry:
            try:
                self.registry.register(
                    name,
                    component,
                    category
                )
            except Exception as error:
                self.failed[name] = str(error)
                self.states[name] = ComponentState.FAILED

        self.log(f"Nó registrado na Lattice: {name}")

    # ==================================================
    # BOOT
    # ==================================================

    def boot(self):
        self.started_at = datetime.now()
        self.log("Inicializando a Neural Lattice...")

        if self.event_bus:
            try:
                self.event_bus.emit(
                    "system.boot.started",
                    {"lattice_version": "Mark IV"}
                )
            except Exception:
                pass

        for name, component in self.components.items():
            try:
                self.states[name] = ComponentState.BOOTING

                if hasattr(component, "initialize"):
                    component.initialize()
                elif hasattr(component, "start"):
                    component.start()

                # Verifica se o componente suporta estado dinâmico ou assume online
                self.states[name] = ComponentState.ONLINE
                self.log(f"[ONLINE] {name}")

                if self.event_bus:
                    try:
                        self.event_bus.emit(
                            "system.component.online",
                            {"component": name, "state": str(self.states[name])}
                        )
                    except Exception:
                        pass

            except Exception as error:
                self.failed[name] = str(error)
                self.states[name] = ComponentState.FAILED
                self.log(f"[FAILED] {name}: {error}")

                if self.event_bus:
                    try:
                        self.event_bus.emit(
                            "system.component.failed",
                            {
                                "component": name,
                                "error": str(error),
                                "state": str(ComponentState.FAILED)
                            }
                        )
                    except Exception:
                        pass

        if self.event_bus:
            try:
                self.event_bus.emit(
                    "system.ready",
                    {"lattice_status": "stable"}
                )
            except Exception:
                pass

        self.log("Boot da Lattice finalizado.")

    # ==================================================
    # SHUTDOWN
    # ==================================================

    def shutdown(self):
        self.log("Desacoplando nós da Lattice...")

        components = list(
            self.components.items()
        )
        components.reverse()

        for name, component in components:
            try:
                self.states[name] = ComponentState.SHUTDOWN

                if hasattr(component, "shutdown"):
                    component.shutdown()
                elif hasattr(component, "stop"):
                    component.stop()

                self.states[name] = ComponentState.OFFLINE
                self.log(f"[OFFLINE] {name}")

            except Exception as error:
                self.log(
                    f"Erro desligando nó {name}: {error}"
                )

        if self.event_bus:
            try:
                self.event_bus.emit(
                    "system.shutdown.finished",
                    {}
                )
            except Exception:
                pass

        self.log("Shutdown da Lattice concluído.")

    # ==================================================
    # RESTART & ISOLATION (Mark IV)
    # ==================================================

    def restart_component(self, name):
        component = self.components.get(name)

        if component is None:
            return False

        try:
            self.states[name] = ComponentState.RESTARTING

            if hasattr(component, "shutdown"):
                component.shutdown()
            elif hasattr(component, "stop"):
                component.stop()

            if hasattr(component, "initialize"):
                component.initialize()
            elif hasattr(component, "start"):
                component.start()

            self.states[name] = ComponentState.ONLINE
            self.log(f"Nó reiniciado com sucesso: {name}")

            return True

        except Exception as error:
            self.failed[name] = str(error)
            self.states[name] = ComponentState.FAILED
            self.log(
                f"Falha reiniciando nó {name}: {error}"
            )
            return False

    def isolate_component(self, name):
        """Isola um nó para proteger a integridade do Core (Mark IV)."""
        component = self.components.get(name)
        if not component:
            return False

        try:
            self.states[name] = ComponentState.ISOLATED
            if hasattr(component, "stop"):
                component.stop()
            elif hasattr(component, "shutdown"):
                component.shutdown()
            
            self.log(f"[ISOLATED] Nó isolado por anomalia: {name}")
            return True
        except Exception as error:
            self.log(f"Erro ao isolar nó {name}: {error}")
            return False

    # ==================================================
    # HEALTH
    # ==================================================

    def health(self):
        online_count = sum(
            1 for state in self.states.values() if state.is_online()
        )
        return {
            "components": len(self.components),
            "online": online_count,
            "failed": len(self.failed),
            "states": {name: str(st) for name, st in self.states.items()},
            "uptime": (
                datetime.now() - self.started_at
            ).total_seconds()
            if self.started_at
            else 0
        }