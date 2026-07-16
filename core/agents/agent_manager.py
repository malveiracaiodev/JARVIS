"""
=========================================
GENESIS CORE

Arquivo:
core/agents/agent_manager.py

Descrição:
Gerenciador central de agentes do ecossistema.

Responsabilidades:
- Registro de agentes
- Descoberta
- Ciclo de vida
- Broadcast
- Estatísticas
- Health Check

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading

from core.base.module import (
    Module,
    ModuleStatus
)


class AgentManager(Module):
    """
    Gerenciador central dos agentes do Genesis.

    Este módulo NÃO possui inteligência.

    Sua única responsabilidade é administrar
    o ciclo de vida dos agentes registrados.
    """

    def __init__(self, logger=None):
        super().__init__("core.agent_manager")

        self.version = "3.0"

        self.logger = logger

        self.agents = {}

        self._lock = threading.RLock()

    # ==========================================================
    # CICLO DE VIDA
    # ==========================================================

    def initialize(self):

        self.set_status(ModuleStatus.INITIALIZING)

        with self._lock:
            self.agents.clear()

        self.set_status(ModuleStatus.ONLINE)

        self.success("Agent Manager inicializado.")

    def shutdown(self):

        self.stop_all()

        with self._lock:
            self.agents.clear()

        self.set_status(ModuleStatus.OFFLINE)

        self.info("Agent Manager finalizado.")

    # ==========================================================
    # REGISTRO
    # ==========================================================

    def register(self, agent):

        if agent is None:
            self.error("Tentativa de registrar agente nulo.")
            return False

        if not hasattr(agent, "name"):
            self.error("O agente não possui atributo 'name'.")
            return False

        key = agent.name.lower()

        with self._lock:

            if key in self.agents:
                self.error(
                    f"Agente '{agent.name}' já registrado."
                )
                return False

            self.agents[key] = agent

        self.success(
            f"Agente registrado: {agent.name}"
        )

        return True

    def unregister(self, name):

        with self._lock:

            agent = self.agents.pop(name.lower(), None)

        if agent is None:
            return False

        try:

            if hasattr(agent, "stop"):
                agent.stop()

        except Exception as e:

            self.error(
                f"Erro ao finalizar agente '{name}': {e}"
            )

        self.info(
            f"Agente removido: {name}"
        )

        return True

    # ==========================================================
    # CONSULTAS
    # ==========================================================

    def exists(self, name):

        with self._lock:
            return name.lower() in self.agents

    def get(self, name):

        with self._lock:
            return self.agents.get(name.lower())

    def list_agents(self):

        with self._lock:
            return sorted(self.agents.keys())

    def count(self):

        with self._lock:
            return len(self.agents)

    # ==========================================================
    # CICLO DOS AGENTES
    # ==========================================================

    def start_all(self):

        with self._lock:

            for agent in self.agents.values():

                if hasattr(agent, "start"):

                    try:

                        agent.start()

                    except Exception as e:

                        self.error(
                            f"Erro ao iniciar '{agent.name}': {e}"
                        )

    def stop_all(self):

        with self._lock:

            for agent in self.agents.values():

                if hasattr(agent, "stop"):

                    try:

                        agent.stop()

                    except Exception as e:

                        self.error(
                            f"Erro ao parar '{agent.name}': {e}"
                        )

    def restart(self, name):

        agent = self.get(name)

        if agent is None:
            return False

        try:

            if hasattr(agent, "stop"):
                agent.stop()

            if hasattr(agent, "start"):
                agent.start()

            return True

        except Exception as e:

            self.error(
                f"Erro ao reiniciar '{name}': {e}"
            )

            return False

    # ==========================================================
    # COMUNICAÇÃO
    # ==========================================================

    def broadcast(self, event):

        with self._lock:

            for agent in self.agents.values():

                if hasattr(agent, "handle"):

                    try:

                        agent.handle(event)

                    except Exception as e:

                        self.error(
                            f"Erro no broadcast para "
                            f"{agent.name}: {e}"
                        )

    # ==========================================================
    # HEALTH CHECK
    # ==========================================================

    def get_online_agents(self):

        online = []

        with self._lock:

            for agent in self.agents.values():

                if hasattr(agent, "status"):

                    if agent.status == ModuleStatus.ONLINE:
                        online.append(agent)

        return online

    # ==========================================================
    # ESTATÍSTICAS
    # ==========================================================

    def stats(self):

        with self._lock:

            total = len(self.agents)

            online = 0
            offline = 0
            initializing = 0
            error = 0

            for agent in self.agents.values():

                status = getattr(agent, "status", None)

                if status == ModuleStatus.ONLINE:
                    online += 1

                elif status == ModuleStatus.OFFLINE:
                    offline += 1

                elif status == ModuleStatus.INITIALIZING:
                    initializing += 1

                elif status == ModuleStatus.ERROR:
                    error += 1

            return {
                "total": total,
                "online": online,
                "offline": offline,
                "initializing": initializing,
                "error": error
            }

    # ==========================================================
    # LOGS
    # ==========================================================

    def info(self, message):

        if self.logger:
            self.logger.info(message)

    def success(self, message):

        if self.logger:
            self.logger.success(message)

    def warning(self, message):

        if self.logger:
            self.logger.warning(message)

    def error(self, message):

        if self.logger:
            self.logger.error(message)