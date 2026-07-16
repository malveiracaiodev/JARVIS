"""
=========================================
GENESIS CORE

Arquivo:
core/agents/agent.py

Descrição:
Classe base universal para agentes
inteligentes do ecossistema Genesis.

Responsável por:
- Personalidade
- Memória interna
- Comunicação com Mind
- Processamento cognitivo
- Ciclo de vida de agentes

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


import threading

from collections import deque
from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)



class Agent(Module):

    """
    Classe base para agentes autônomos
    e integrados ao Genesis.

    Exemplos:

    - Jarvis
    - Rafiki
    - Vision
    - Planner
    - Programmer
    """



    def __init__(
        self,
        name,
        personality="default",
        description="",
        capabilities=None
    ):


        super().__init__(
            name=name,
            description=description,
            version="3.0",
            tags=[
                "agent",
                "cognitive"
            ],
            capabilities=capabilities or []
        )


        # ==================================================
        # PERSONALIDADE
        # ==================================================

        self.personality = personality



        # ==================================================
        # MEMÓRIA INTERNA
        # ==================================================

        self.memory = deque(
            maxlen=500
        )



        # ==================================================
        # CONEXÕES
        # ==================================================

        self.mind = None

        self.event_bus = None

        self.memory_manager = None



        # ==================================================
        # LOCK DO AGENTE
        # ==================================================

        self._agent_lock = threading.RLock()



    # ======================================================
    # INICIALIZAÇÃO
    # ======================================================


    def initialize(self):

        with self._agent_lock:

            self.set_status(
                ModuleStatus.INITIALIZING
            )


            self.on_start()


            self.set_status(
                ModuleStatus.ONLINE
            )


    def shutdown(self):

        with self._agent_lock:

            self.on_stop()


            self.set_status(
                ModuleStatus.OFFLINE
            )



    # ======================================================
    # CONEXÕES
    # ======================================================


    def connect_mind(self, mind):

        with self._agent_lock:

            self.mind = mind

            self.speak(
                "Conexão estabelecida com Mind."
            )



    def connect_memory(self, memory):

        with self._agent_lock:

            self.memory_manager = memory



    def connect_event_bus(self, event_bus):

        with self._agent_lock:

            self.event_bus = event_bus



    # ======================================================
    # COMUNICAÇÃO
    # ======================================================


    def receive(self, message):

        with self._agent_lock:


            self.memory.append({

                "message":
                    message,

                "time":
                    datetime.now()
                    .isoformat()

            })


            self.register_event()



            try:


                if self.mind:

                    return self.mind.think(
                        message
                    )


                return self.think(
                    message
                )



            except Exception as e:


                self.set_error(
                    str(e)
                )


                return (
                    "Erro cognitivo: "
                    +
                    str(e)
                )



    # ======================================================
    # PROCESSAMENTO
    # ======================================================


    def think(self, message):

        """
        Método padrão.

        Deve ser sobrescrito pelos agentes
        especializados.
        """


        return (
            f"{self.name}: "
            "Núcleo cognitivo padrão ativo."
        )



    def execute(self, command):

        """
        Executor específico do agente.

        Pode ser sobrescrito.
        """


        return None



    # ======================================================
    # MEMÓRIA
    # ======================================================


    def remember(self, data):

        with self._agent_lock:

            self.memory.append({

                "data":
                    data,

                "time":
                    datetime.now()
                    .isoformat()

            })



    def recall(self):

        with self._agent_lock:

            return list(
                self.memory
            )



    # ======================================================
    # HOOKS
    # ======================================================


    def on_start(self):

        pass



    def on_stop(self):

        pass



    def on_message(self, message):

        pass



    # ======================================================
    # SAÍDA
    # ======================================================


    def speak(self, text):

        """
        Temporário.

        Futuramente será substituído
        pelo Voice Engine + EventBus.
        """


        print(
            f"[{self.name.upper()}] -> {text}"
        )



    # ======================================================
    # INFORMAÇÕES
    # ======================================================


    def info(self):

        data = super().info()


        data.update({

            "personality":
                self.personality,


            "memory_size":
                len(self.memory),


            "mind_connected":
                self.mind is not None

        })


        return data