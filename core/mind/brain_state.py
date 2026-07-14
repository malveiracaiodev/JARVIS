"""
=========================================
JARVIS CORE

Arquivo:
core/mind/state.py

Descrição:
Gerenciador central do estado cognitivo.

Responsável por concentrar todos os
componentes responsáveis pelo estado da
mente do JARVIS.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from core.mind.brain_context import Context
from core.mind.memory import Memory
from core.mind.knowledge import Knowledge


class BrainState:
    """
    Estado global da mente.

    Todos os módulos cognitivos devem acessar
    informações através desta classe, evitando
    acoplamento direto entre Brain e os
    componentes internos.
    """

    def __init__(self, logger=None):

        self.logger = logger

        self.context = Context()

        self.memory = Memory()

        self.knowledge = Knowledge()

        self.session = {}

        self.variables = {}

        self.goals = []

        self.history = []

    # =====================================================
    # Inicialização
    # =====================================================

    def initialize(self):

        self.memory.logger = self.logger
        self.knowledge.logger = self.logger

        if hasattr(self.memory, "initialize"):
            self.memory.initialize()

        if hasattr(self.knowledge, "initialize"):
            self.knowledge.initialize()

        if self.logger:
            self.logger.success("BrainState inicializado.")

    # =====================================================
    # Sessão
    # =====================================================

    def set_session(self, key, value):

        self.session[key] = value

    def get_session(self, key, default=None):

        return self.session.get(key, default)

    # =====================================================
    # Variáveis Cognitivas
    # =====================================================

    def set_variable(self, key, value):

        self.variables[key] = value

    def get_variable(self, key, default=None):

        return self.variables.get(key, default)

    # =====================================================
    # Objetivos
    # =====================================================

    def add_goal(self, goal):

        self.goals.append(goal)

    def remove_goal(self, goal):

        if goal in self.goals:
            self.goals.remove(goal)

    def clear_goals(self):

        self.goals.clear()

    # =====================================================
    # Histórico Cognitivo
    # =====================================================

    def add_history(self, thought):

        self.history.append(thought)

    def clear_history(self):

        self.history.clear()

    # =====================================================
    # Estado
    # =====================================================

    def snapshot(self):

        return {

            "session": self.session,

            "variables": self.variables,

            "goals": self.goals,

            "history_size": len(self.history),

            "context": self.context.snapshot()

        }

    # =====================================================

    def shutdown(self):

        if hasattr(self.memory, "shutdown"):
            self.memory.shutdown()

        if hasattr(self.knowledge, "shutdown"):
            self.knowledge.shutdown()

        if self.logger:
            self.logger.info("BrainState finalizado.")