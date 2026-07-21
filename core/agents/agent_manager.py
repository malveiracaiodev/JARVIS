"""
=========================================
GENESIS CORE

Arquivo:
core/agents/agent_manager.py

Descrição:
Gerenciador central de agentes.

Responsável por:

- Registro
- Descoberta
- Inicialização
- Encerramento
- Comunicação
- Health Check
- Carregamento dinâmico de Personas

Arquitetura:

Kernel
   |
   ▼
AgentManager
   |
   ▼
PersonaFactory
   |
   ▼
identity.json


Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


import threading



from core.base.module import (
    Module,
    ModuleStatus
)



from personas.persona_factory import (
    PersonaFactory
)





class AgentManager(Module):


    """
    Controlador do ecossistema
    de agentes Genesis.

    Não conhece agentes específicos.

    Toda descoberta é feita
    através da PersonaFactory.
    """



    def __init__(
        self,
        logger=None,
        factory=None
    ):


        super().__init__(
            "core.agent_manager"
        )


        self.version = "4.0"


        self.logger = logger


        self.factory = (

            factory

            or

            PersonaFactory()

        )


        self.agents = {}


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


        self.success(
            "Agent Manager inicializado."
        )






    def shutdown(self):


        self.shutdown_all()


        self.agents.clear()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.info(
            "Agent Manager encerrado."
        )








    # ==================================================
    # DESCOBERTA DE PERSONAS
    # ==================================================


    def discover(self):


        """
        Descobre personas disponíveis
        no identity.json.
        """


        if not self.factory:

            return []



        return self.factory.available()







    # ==================================================
    # CARREGAMENTO DINÂMICO
    # ==================================================


    def load_personas(self):


        """
        Cria e registra todas as
        personas declaradas.
        """


        personas = self.discover()



        for name in personas:


            try:


                agent = self.factory.create(
                    name
                )


                self.register(
                    agent
                )



            except Exception as error:


                self.error(

                    f"Falha carregando {name}: {error}"

                )









    # ==================================================
    # REGISTRO
    # ==================================================


    def register(
        self,
        agent
    ):


        if agent is None:


            self.error(
                "Agente inválido."
            )


            return False




        if not hasattr(
            agent,
            "name"
        ):


            self.error(
                "Agente sem nome."
            )


            return False





        key = agent.name.lower()




        with self._lock:



            if key in self.agents:


                self.warning(
                    f"{agent.name} já registrado."
                )


                return False





            self.agents[key] = agent






        self.success(

            f"Agente registrado: {agent.name}"

        )


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


            try:

                agent.shutdown()


            except Exception as error:


                self.error(
                    str(error)
                )



            return True



        return False







    # ==================================================
    # CONSULTA
    # ==================================================


    def get(
        self,
        name
    ):


        return self.agents.get(

            name.lower()

        )







    def exists(
        self,
        name
    ):


        return (

            name.lower()

            in

            self.agents

        )







    def list_agents(
        self
    ):


        return list(

            self.agents.keys()

        )







    def count(
        self
    ):


        return len(

            self.agents

        )








    # ==================================================
    # CONTROLE
    # ==================================================


    def initialize_all(self):


        with self._lock:


            for agent in self.agents.values():


                try:


                    agent.initialize()



                except Exception as error:


                    self.error(

                        f"{agent.name}: {error}"

                    )








    def shutdown_all(self):


        with self._lock:


            for agent in self.agents.values():


                try:


                    agent.shutdown()



                except Exception as error:


                    self.error(

                        f"{agent.name}: {error}"

                    )








    def restart(
        self,
        name
    ):


        agent = self.get(
            name
        )



        if not agent:

            return False





        try:


            agent.shutdown()


            agent.initialize()



            return True



        except Exception as error:


            self.error(
                str(error)
            )


            return False








    # ==================================================
    # COMUNICAÇÃO
    # ==================================================


    def send(
        self,
        agent_name,
        message
    ):


        agent = self.get(
            agent_name
        )



        if not agent:


            return "Agente não encontrado."



        return agent.receive(
            message
        )








    def broadcast(
        self,
        message
    ):


        responses = {}



        with self._lock:


            for name, agent in self.agents.items():


                try:


                    responses[name] = agent.receive(
                        message
                    )



                except Exception as error:


                    responses[name] = str(error)



        return responses








    # ==================================================
    # HEALTH CHECK
    # ==================================================


    def online_agents(self):


        result = []



        for agent in self.agents.values():


            if agent.status == ModuleStatus.ONLINE:


                result.append(
                    agent.name
                )


        return result








    def stats(self):


        data = {

            "total": 0,

            "online": 0,

            "offline": 0,

            "error": 0

        }



        for agent in self.agents.values():


            data["total"] += 1



            if agent.status == ModuleStatus.ONLINE:


                data["online"] += 1



            elif agent.status == ModuleStatus.ERROR:


                data["error"] += 1



            else:


                data["offline"] += 1



        return data








    # ==================================================
    # LOG
    # ==================================================


    def info(
        self,
        message
    ):


        if self.logger:

            self.logger.info(
                message
            )





    def success(
        self,
        message
    ):


        if self.logger:

            self.logger.success(
                message
            )





    def warning(
        self,
        message
    ):


        if self.logger:

            self.logger.warning(
                message
            )





    def error(
        self,
        message
    ):


        if self.logger:

            self.logger.error(
                message
            )