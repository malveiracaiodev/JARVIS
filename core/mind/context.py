"""
=========================================
GENESIS CORE - COGNITIVE CONTEXT

Arquivo: core/mind/context.py
Descrição: Gerenciador do contexto cognitivo e memória de trabalho.
Mark: IV - Thought Engine
=========================================
"""

from copy import deepcopy
from datetime import datetime
from typing import Dict, Any, Optional, List

class Context:
    """
    Memória de trabalho cognitiva. Mantém o estado dinâmico do ecossistema.
    """

    def __init__(self):
        now = datetime.now().isoformat()
        self._context: Dict[str, Any] = {
            "session": {"id": None, "created_at": now, "updated_at": now},
            "system": {"status": "booting", "version": "Genesis Core Mark IV"},
            "user": {"name": None, "id": None},
            "agent": {"active": "jarvis", "available": ["jarvis", "rafiki"]},
            "conversation": {"last_message": None, "last_response": None},
            "task": {"current": None, "queue": []},
            "thought": {"current": None, "history": []},
            "environment": {"os": None, "internet": None, "location": None},
            "applications": {},
            "devices": {"bluetooth": [], "wifi": []},
            "custom": {}
        }

    def update(self, section: str, key: str, value: Any) -> None:
        if section not in self._context:
            self._context[section] = {}
        self._context[section][key] = value
        self._context["session"]["updated_at"] = datetime.now().isoformat()

    def get(self, section: Optional[str] = None, key: Optional[str] = None) -> Any:
        if section is None:
            return deepcopy(self._context)
        if section not in self._context:
            return None
        if key is None:
            return deepcopy(self._context[section])
        return deepcopy(self._context[section].get(key))

    def set_agent(self, agent: str) -> None:
        self._context["agent"]["active"] = agent.lower().strip()

    def get_agent(self) -> str:
        return self._context["agent"]["active"]

    def set_last_message(self, message: str) -> None:
        self._context["conversation"]["last_message"] = message

    def set_last_response(self, response: str) -> None:
        self._context["conversation"]["last_response"] = response

    def set_thought(self, thought: Any) -> None:
        self._context["thought"]["current"] = thought

    def finish_thought(self) -> None:
        current = self._context["thought"]["current"]
        if current:
            self._context["thought"]["history"].append(current)
        self._context["thought"]["current"] = None

    def set_task(self, task: Any) -> None:
        self._context["task"]["current"] = task

    def add_task(self, task: Any) -> None:
        self._context["task"]["queue"].append(task)

    def clear_tasks(self) -> None:
        self._context["task"]["queue"].clear()

    def register_application(self, name: str, data: Optional[Dict] = None) -> None:
        self._context["applications"][name] = data or {}

    def unregister_application(self, name: str) -> None:
        self._context["applications"].pop(name, None)

    def set_devices(self, device_type: str, devices: List[Any]) -> None:
        if device_type in self._context["devices"]:
            self._context["devices"][device_type] = devices

    def set_custom(self, key: str, value: Any) -> None:
        self._context["custom"][key] = value

    def get_custom(self, key: str, default: Any = None) -> Any:
        return self._context["custom"].get(key, default)

    def clear_temporary(self) -> None:
        self._context["conversation"] = {"last_message": None, "last_response": None}
        self._context["task"]["current"] = None
        self._context["thought"]["current"] = None

    def snapshot(self) -> Dict[str, Any]:
        return deepcopy(self._context)

    def __repr__(self) -> str:
        return f"<Context agent={self.get_agent()}>"