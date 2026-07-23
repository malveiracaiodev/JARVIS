"""
=========================================
GENESIS CORE

Arquivo:
core/agents/agent_manager.py

Descrição:

Gerenciador central dos agentes cognitivos.

Responsável por:

- Registro de agentes
- Inicialização
- Comunicação
- Controle de ciclo de vida
- Health check
- Integração com Mind
- Integração com Memory
- Integração com Tools


Arquitetura:

Kernel
  |
  v
AgentManager
  |
  v
AgentFactory
  |
  v
GenesisAgent
  |
  v
Persona


Mark:
V - Evolution
=========================================
"""


import threading


from core.base.module import (
    Module,
    ModuleStatus
)



class AgentManager(Module):


    """
    Controlador do ecossistema
    de agentes Genesis.
    """


    def __init__(
        self,
        logger=None,
        factory=None
    ):


        super().__init__(
            name="agent_manager"
        )


        self.version = "5.0"


        self.logger = logger


        self.factory = factory


        self.agents = {}


        self.default_agent = None


        self._lock = threading.RLock()



    # =========================================
    # LOG
    # =========================================


    def log(
        self,
        message
    ):


        if self.logger:

            self.logger.info(message)

        else:

            print(
                "[AGENT_MANAGER]",
                message
            )



    # =========================================
    # LIFE CYCLE
    # =========================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log(
            "AgentManager online."
        )



    def shutdown(self):


        self.shutdown_all()


        self.agents.clear()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log(
            "AgentManager offline."
        )



    # =========================================
    # FACTORY
    # =========================================


    def create_agent(
        self,
        name
    ):


        if not self.factory:

            raise RuntimeError(
                "AgentFactory não conectado."
            )


        agent = self.factory.create(
            name
        )


        self.register(
            agent
        )


        return agent



    # =========================================
    # REGISTRO
    # =========================================


    def register(
        self,
        agent
    ):


        if not agent:

            return False



        key = agent.name.lower()



        with self._lock:


            if key in self.agents:

                return False


            self.agents[key] = agent



        self.log(
            f"Agente registrado: {agent.name}"
        )


        if not self.default_agent:

            self.default_agent = key


        return True



    def unregister(
        self,
        name
    ):


        with self._lock:

            agent = self.agents.pop(
                name.lower(),
                None
            )


        if agent:

            agent.shutdown()

            return True


        return False



    # =========================================
    # CONSULTA
    # =========================================


    def get(
        self,
        name
    ):


        return self.agents.get(
            name.lower()
        )



    def list_agents(self):

        return list(
            self.agents.keys()
        )



    def count(self):

        return len(
            self.agents
        )



    # =========================================
    # CICLO DOS AGENTES
    # =========================================


    def initialize_all(self):


        for agent in self.agents.values():

            try:

                agent.initialize()

            except Exception as error:

                self.log(
                    f"Erro iniciando {agent.name}: {error}"
                )




    def shutdown_all(self):


        for agent in self.agents.values():

            try:

                agent.shutdown()

            except Exception as error:

                self.log(
                    str(error)
                )



    # =========================================
    # COMUNICAÇÃO
    # =========================================


    def send(
        self,
        agent_name,
        message
    ):


        agent = self.get(
            agent_name
        )


        if not agent:

            return {
                "error":
                "Agente inexistente"
            }


        return agent.receive(
            message
        )



    def ask(
        self,
        message
    ):


        if not self.default_agent:

            return None


        return self.agents[
            self.default_agent
        ].receive(
            message
        )



    def broadcast(
        self,
        message
    ):


        result = {}


        for name, agent in self.agents.items():

            try:

                result[name] = agent.receive(
                    message
                )

            except Exception as error:

                result[name] = str(error)


        return result



    # =========================================
    # HEALTH
    # =========================================


    def health(self):


        data = {

            "total":
                len(self.agents),

            "online":
                0,

            "offline":
                0,

            "error":
                0

        }



        for agent in self.agents.values():


            status = agent.status


            if status == ModuleStatus.ONLINE:

                data["online"] += 1


            elif status == ModuleStatus.ERROR:

                data["error"] += 1


            else:

                data["offline"] += 1



        return data



    # =========================================
    # INFO
    # =========================================


    def info(self):


        return {

            "version":
                self.version,

            "agents":
                self.list_agents(),

            "default":
                self.default_agent,

            "health":
                self.health()

        }