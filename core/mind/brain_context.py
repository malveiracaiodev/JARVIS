"""
=========================================
JARVIS CORE

Arquivo:
core/mind/context.py

Descrição:
Gerenciador do contexto cognitivo do JARVIS.

Responsável por manter o estado atual do
ambiente, da conversa, do usuário e das
tarefas em execução.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from copy import deepcopy
from datetime import datetime


class Context:
    """
    Mantém o estado atual da mente do JARVIS.

    Este módulo funciona como uma memória de
    contexto temporária (Working Context),
    permitindo que os demais componentes
    cognitivos consultem informações sobre
    o ambiente atual.
    """

    def __init__(self):

        self._context = {
            "system": {
                "status": "booting",
                "started_at": datetime.now(),
                "last_update": datetime.now(),
            },

            "user": {
                "name": None,
                "id": None,
            },

            "agent": {
                "active": "jarvis",
            },

            "conversation": {
                "last_message": None,
                "last_response": None,
            },

            "task": {
                "current": None,
                "queue": [],
            },

            "thought": {
                "current": None,
                "last": None,
            },

            "environment": {
                "os": None,
                "internet": None,
                "location": None,
            },

            "applications": {},

            "devices": {
                "bluetooth": [],
                "wifi": [],
            },

            "custom": {}
        }

    # ==========================================================
    # Atualização
    # ==========================================================

    def update(self, section, key, value):
        """
        Atualiza um campo do contexto.
        """

        if section not in self._context:
            self._context[section] = {}

        self._context[section][key] = value
        self._context["system"]["last_update"] = datetime.now()

    # ==========================================================
    # Consulta
    # ==========================================================

    def get(self, section=None, key=None):

        if section is None:
            return deepcopy(self._context)

        if section not in self._context:
            return None

        if key is None:
            return deepcopy(self._context[section])

        return deepcopy(self._context[section].get(key))

    # ==========================================================
    # Aplicações
    # ==========================================================

    def register_application(self, name, data=None):

        self._context["applications"][name] = data or {}

    def unregister_application(self, name):

        self._context["applications"].pop(name, None)

    def application_running(self, name):

        return name in self._context["applications"]

    # ==========================================================
    # Dispositivos
    # ==========================================================

    def set_bluetooth_devices(self, devices):

        self._context["devices"]["bluetooth"] = devices

    def set_wifi_devices(self, devices):

        self._context["devices"]["wifi"] = devices

    # ==========================================================
    # Conversa
    # ==========================================================

    def set_last_message(self, message):

        self._context["conversation"]["last_message"] = message

    def set_last_response(self, response):

        self._context["conversation"]["last_response"] = response

    # ==========================================================
    # Pensamentos
    # ==========================================================

    def set_current_thought(self, thought):

        self._context["thought"]["current"] = thought

    def finish_thought(self):

        self._context["thought"]["last"] = self._context["thought"]["current"]
        self._context["thought"]["current"] = None

    # ==========================================================
    # Tarefas
    # ==========================================================

    def set_current_task(self, task):

        self._context["task"]["current"] = task

    def add_task(self, task):

        self._context["task"]["queue"].append(task)

    def clear_tasks(self):

        self._context["task"]["queue"].clear()

    # ==========================================================
    # Custom
    # ==========================================================

    def set_custom(self, key, value):

        self._context["custom"][key] = value

    def get_custom(self, key, default=None):

        return self._context["custom"].get(key, default)

    # ==========================================================
    # Utilidades
    # ==========================================================

    def clear(self):
        """
        Limpa apenas informações temporárias.
        """

        self._context["conversation"] = {
            "last_message": None,
            "last_response": None,
        }

        self._context["task"] = {
            "current": None,
            "queue": [],
        }

        self._context["thought"] = {
            "current": None,
            "last": None,
        }

        self._context["applications"].clear()

    def snapshot(self):
        """
        Retorna uma cópia completa do contexto.
        """

        return deepcopy(self._context)

    def __repr__(self):

        return (
            f"<Context "
            f"agent={self.get('agent', 'active')} "
            f"task={self.get('task', 'current')}>"
        )