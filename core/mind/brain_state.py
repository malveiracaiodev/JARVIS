"""
=========================================
GENESIS CORE - BRAIN STATE

Arquivo: core/mind/brain_state.py
Descrição: Concentrador central do estado mental e subsistemas de memória.
Mark: IV - Thought Engine
=========================================
"""

from copy import deepcopy
from typing import Dict, Any, List, Optional
from core.mind.context import Context
from core.mind.memory import Memory
from core.mind.knowledge import Knowledge

class BrainState:
    """
    Representação unificada e thread-safe do estado interno da mente.
    """

    def __init__(self, logger: Optional[Any] = None):
        self.logger = logger
        self.initialized = False
        
        self.context = Context()
        self.memory = Memory()
        self.knowledge = Knowledge()
        
        self.session: Dict[str, Any] = {}
        self.variables: Dict[str, Any] = {}
        self.goals: List[Any] = []
        self.history: List[Any] = []

    def initialize(self) -> bool:
        if self.initialized:
            return True

        self.memory.logger = self.logger
        self.knowledge.logger = self.logger

        if hasattr(self.memory, "initialize"):
            self.memory.initialize()

        if hasattr(self.knowledge, "initialize"):
            self.knowledge.initialize()

        self.initialized = True
        if self.logger and hasattr(self.logger, "success"):
            self.logger.success("BrainState inicializado no padrão Mark IV.")
        return True

    def set_session(self, key: str, value: Any) -> None:
        self.session[key] = value

    def get_session(self, key: str, default: Any = None) -> Any:
        return self.session.get(key, default)

    def set_variable(self, key: str, value: Any) -> None:
        self.variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)

    def add_goal(self, goal: Any) -> None:
        self.goals.append(goal)

    def remove_goal(self, goal: Any) -> None:
        if goal in self.goals:
            self.goals.remove(goal)

    def clear_goals(self) -> None:
        self.goals.clear()

    def add_history(self, entry: Any) -> None:
        self.history.append(entry)

    def clear_history(self) -> None:
        self.history.clear()

    def set_thought(self, thought: Any) -> None:
        self.context.set_thought(thought)

    def get_snapshot(self) -> Dict[str, Any]:
        return self.snapshot()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "session": deepcopy(self.session),
            "variables": deepcopy(self.variables),
            "goals": deepcopy(self.goals),
            "history_size": len(self.history),
            "context": self.context.snapshot()
        }

    def shutdown(self) -> bool:
        if hasattr(self.memory, "shutdown"):
            self.memory.shutdown()
        if hasattr(self.knowledge, "shutdown"):
            self.knowledge.shutdown()

        self.initialized = False
        if self.logger and hasattr(self.logger, "info"):
            self.logger.info("BrainState finalizado.")
        return True