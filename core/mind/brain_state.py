"""
=========================================
JARVIS CORE

Arquivo:
core/mind/brain_state.py

Descrição:
Gerenciador central do estado cognitivo.

Responsável por concentrar:
- Contexto atual
- Memória
- Conhecimento
- Sessão
- Objetivos
- Histórico cognitivo

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from copy import deepcopy


from core.mind.brain_context import Context

from core.mind.memory import Memory

from core.mind.knowledge import Knowledge



class BrainState:
    """
    Estado central da mente do Genesis Core.

    Representa o estado interno utilizado
    pelos componentes cognitivos.
    """



    def __init__(
        self,
        logger=None
    ):

        self.logger = logger


        self.initialized = False



        # Estado atual

        self.context = Context()



        # Memória persistente

        self.memory = Memory()



        # Base de conhecimento

        self.knowledge = Knowledge()



        # Sessão atual

        self.session = {}



        # Variáveis internas

        self.variables = {}



        # Objetivos

        self.goals = []



        # Histórico cognitivo

        self.history = []



    # =====================================================
    # Inicialização
    # =====================================================


    def initialize(
        self
    ):

        if self.initialized:

            return True



        self.memory.logger = self.logger

        self.knowledge.logger = self.logger



        if hasattr(
            self.memory,
            "initialize"
        ):

            self.memory.initialize()



        if hasattr(
            self.knowledge,
            "initialize"
        ):

            self.knowledge.initialize()



        self.initialized = True



        if self.logger:

            self.logger.success(
                "BrainState inicializado."
            )



        return True



    # =====================================================
    # Sessão
    # =====================================================


    def set_session(
        self,
        key,
        value
    ):

        self.session[key] = value



    def get_session(
        self,
        key,
        default=None
    ):

        return self.session.get(
            key,
            default
        )



    # =====================================================
    # Variáveis
    # =====================================================


    def set_variable(
        self,
        key,
        value
    ):

        self.variables[key] = value



    def get_variable(
        self,
        key,
        default=None
    ):

        return self.variables.get(
            key,
            default
        )



    # =====================================================
    # Objetivos
    # =====================================================


    def add_goal(
        self,
        goal
    ):

        self.goals.append(
            goal
        )



    def remove_goal(
        self,
        goal
    ):

        if goal in self.goals:

            self.goals.remove(
                goal
            )



    def clear_goals(
        self
    ):

        self.goals.clear()



    # =====================================================
    # Histórico
    # =====================================================


    def add_history(
        self,
        entry
    ):

        self.history.append(
            entry
        )



    def clear_history(
        self
    ):

        self.history.clear()



    # =====================================================
    # Integração Cognitiva
    # =====================================================


    def set_thought(
        self,
        thought
    ):

        self.context.set_thought(
            thought
        )



    def get_snapshot(
        self
    ):

        return self.snapshot()



    # =====================================================
    # Snapshot
    # =====================================================


    def snapshot(
        self
    ):

        return {


            "session":
                deepcopy(
                    self.session
                ),


            "variables":
                deepcopy(
                    self.variables
                ),


            "goals":
                deepcopy(
                    self.goals
                ),


            "history_size":
                len(
                    self.history
                ),


            "context":
                self.context.snapshot()

        }



    # =====================================================
    # Finalização
    # =====================================================


    def shutdown(
        self
    ):


        if hasattr(
            self.memory,
            "shutdown"
        ):

            self.memory.shutdown()



        if hasattr(
            self.knowledge,
            "shutdown"
        ):

            self.knowledge.shutdown()



        self.initialized = False



        if self.logger:

            self.logger.info(
                "BrainState finalizado."
            )