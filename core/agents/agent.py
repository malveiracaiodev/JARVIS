"""
=========================================
GENESIS CORE

Arquivo:
core/agents/agent.py

Descrição:

Classe base universal para todos os
agentes do Genesis Core.

Responsabilidades:

- Identidade
- Ciclo de vida
- Estado
- Memória local
- Comunicação
- Eventos
- Conexões

Não possui inteligência.

Toda cognição pertence ao:

- GenesisAgent
- Mind
- Thought Engine
- AIManager

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations

import threading

from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.base.module import Module, ModuleStatus


class Agent(Module):
    """
    Infraestrutura base de qualquer agente.

    Não executa raciocínio.

    Apenas fornece a estrutura comum
    utilizada pelos agentes do Genesis.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        capabilities: Optional[List[str]] = None
    ) -> None:

        super().__init__(
            name=name,
            description=description,
            version="5.0",
            tags=[
                "agent",
                "genesis"
            ],
            capabilities=capabilities or []
        )

        # =====================================
        # IDENTIDADE
        # =====================================

        self.identity = {
            "name": name,
            "created_at": datetime.now().isoformat()
        }

        # =====================================
        # MEMÓRIA LOCAL
        # =====================================

        self.memory = deque(maxlen=500)

        # =====================================
        # CONEXÕES
        # =====================================

        self.mind = None
        self.memory_manager = None
        self.event_bus = None
        self.tool_manager = None

        # =====================================
        # CONTROLE
        # =====================================

        self.active = True

        self.last_input = None
        self.last_output = None

        self._lock = threading.RLock()

    # ==================================================
    # CICLO DE VIDA
    # ==================================================

    def initialize(self):

        with self._lock:

            self.set_status(
                ModuleStatus.INITIALIZING
            )

            self.on_start()

            self.active = True

            self.set_status(
                ModuleStatus.ONLINE
            )

    def shutdown(self):

        with self._lock:

            self.on_stop()

            self.active = False

            self.set_status(
                ModuleStatus.OFFLINE
            )

    # ==================================================
    # CONEXÕES
    # ==================================================

    def connect_mind(self, mind):

        self.mind = mind

    def connect_memory(self, memory):

        self.memory_manager = memory

    def connect_event_bus(self, event_bus):

        self.event_bus = event_bus

    def connect_tools(self, tool_manager):

        self.tool_manager = tool_manager

    # ==================================================
    # COMUNICAÇÃO
    # ==================================================

    def receive(
        self,
        message: Any
    ):

        with self._lock:

            self.last_input = message

            self.remember({

                "type": "input",

                "content": message

            })

            self.on_message(message)

            response = self.think(message)

            self.last_output = response

            self.remember({

                "type": "output",

                "content": response

            })

            return response

    # ==================================================
    # PENSAMENTO
    # ==================================================

    def think(
        self,
        message: Any
    ):
        """
        Método sobrescrito pelo GenesisAgent.
        """

        return {

            "status": "no_cognitive_layer",

            "agent": self.name,

            "message": message

        }

    # ==================================================
    # FERRAMENTAS
    # ==================================================

    def execute(
        self,
        tool: str,
        data: Any = None
    ):

        if self.tool_manager is None:

            return None

        if hasattr(
            self.tool_manager,
            "execute"
        ):

            return self.tool_manager.execute(
                tool,
                data
            )

        return None

    # ==================================================
    # MEMÓRIA
    # ==================================================

    def remember(
        self,
        data: Any
    ):

        self.memory.append({

            "time": datetime.now().isoformat(),

            "data": data

        })

    def recall(self):

        return list(
            self.memory
        )

    def clear_memory(self):

        self.memory.clear()

    # ==================================================
    # EVENTOS
    # ==================================================

    def emit(
        self,
        event: str,
        data: Any = None
    ):

        if (

            self.event_bus

            and

            hasattr(
                self.event_bus,
                "publish"
            )

        ):

            self.event_bus.publish(
                event,
                data
            )

    # ==================================================
    # HOOKS
    # ==================================================

    def on_start(self):

        pass

    def on_stop(self):

        pass

    def on_message(
        self,
        message
    ):

        pass

    # ==================================================
    # STATUS
    # ==================================================

    def info(self) -> Dict[str, Any]:

        data = super().info()

        data.update({

            "active": self.active,

            "identity": self.identity,

            "memory_size": len(self.memory),

            "mind_connected":
                self.mind is not None,

            "memory_connected":
                self.memory_manager is not None,

            "tools_connected":
                self.tool_manager is not None,

            "event_bus_connected":
                self.event_bus is not None,

            "last_input":
                self.last_input,

            "last_output":
                self.last_output

        })

        return data

    def __repr__(self):

        return (
            f"<Agent {self.name}>"
        )