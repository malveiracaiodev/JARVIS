"""
=========================================
JARVIS CORE

Arquivo:
core/services/event_bus.py

Descrição:
Sistema central de comunicação por eventos
do Genesis Core.

Responsável por:

- Comunicação desacoplada
- Dispatch thread-safe
- Histórico de eventos
- Estatísticas
- Listeners globais
- Listeners únicos

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from collections import defaultdict, deque
from datetime import datetime

from core.base.module import (
    Module,
    ModuleStatus,
)


class EventBus(Module):
    """
    Barramento central de eventos.

    Responsável pela comunicação desacoplada
    entre todos os módulos do Genesis Core.
    """

    GLOBAL_EVENT = "*"

    def __init__(self, logger=None):
        super().__init__("core.event_bus")

        self.version = "3.0"

        self.logger = logger

        self.listeners = defaultdict(list)

        self.max_history = 1000
        self.history = deque(maxlen=self.max_history)

        self.event_count = 0

        self._lock = threading.RLock()

    # =====================================================
    # Ciclo de vida
    # =====================================================

    def initialize(self):

        with self._lock:

            self.set_status(ModuleStatus.INITIALIZING)

            self.listeners.clear()
            self.history.clear()

            self.event_count = 0

            self.set_status(ModuleStatus.ONLINE)

        self.success("EventBus ONLINE.")

    def shutdown(self):

        with self._lock:

            self.listeners.clear()
            self.history.clear()

            self.set_status(ModuleStatus.OFFLINE)

        self.info("EventBus OFFLINE.")

    # =====================================================
    # Inscrição
    # =====================================================

    def subscribe(self, event_name, callback):

        with self._lock:

            if callback not in self.listeners[event_name]:

                self.listeners[event_name].append(callback)

                self.info(
                    f"Listener registrado: {event_name}"
                )

    def once(self, event_name, callback):

        def wrapper(*args, **kwargs):
            self.unsubscribe(event_name, wrapper)
            callback(*args, **kwargs)

        self.subscribe(event_name, wrapper)

    def unsubscribe(self, event_name, callback):

        with self._lock:

            listeners = self.listeners.get(event_name)

            if not listeners:
                return

            if callback in listeners:

                listeners.remove(callback)

            if not listeners:

                self.listeners.pop(event_name, None)

    def clear_listeners(self):

        with self._lock:

            self.listeners.clear()

    # =====================================================
    # Emissão
    # =====================================================

    def emit(self, event_name, *args, **kwargs):

        payload = None

        if args:
            payload = args[0]

        elif kwargs:
            payload = kwargs

        with self._lock:

            self.event_count += 1

            event = {
                "id": self.event_count,
                "event": event_name,
                "payload": payload,
                "time": datetime.now().isoformat(),
            }

            self.history.append(event)

            targets = list(
                self.listeners.get(event_name, [])
            )

            globals_ = list(
                self.listeners.get(self.GLOBAL_EVENT, [])
            )

        self.info(f"Evento: {event_name}")

        for callback in targets:

            try:
                callback(*args, **kwargs)

            except Exception as error:

                self.error(
                    f"Erro no listener '{event_name}': {error}"
                )

        for callback in globals_:

            try:
                callback(event_name, *args, **kwargs)

            except Exception as error:

                self.error(
                    f"Erro em listener global: {error}"
                )

    # =====================================================
    # Consulta
    # =====================================================

    def has_event(self, event_name):

        with self._lock:

            return event_name in self.listeners

    def get_history(self):

        with self._lock:

            return list(self.history)

    def get_event_count(self):

        with self._lock:

            return self.event_count

    def clear_history(self):

        with self._lock:

            self.history.clear()

    def status(self):

        with self._lock:

            return {
                "name": self.name,
                "version": self.version,
                "status": self.get_status().value,
                "events": self.event_count,
                "listeners": sum(
                    len(v)
                    for v in self.listeners.values()
                ),
                "registered_events": len(
                    self.listeners
                ),
                "history": len(self.history),
            }

    # =====================================================
    # Logging
    # =====================================================

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