"""
=========================================
JARVIS CORE

Arquivo:
event_bus.py

Descrição:
Sistema central de eventos do JARVIS.

Responsável por:
- Comunicação desacoplada e assíncrona entre módulos
- Distribuição de eventos thread-safe
- Histórico operacional circular otimizado
- Sincronização e isolamento de falhas de listeners

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.2 - High Concurrency)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from collections import defaultdict, deque
from datetime import datetime

from core.base.module import (
    Module,
    ModuleStatus
)


class EventBus(Module):
    """
    Barramento central thread-safe de comunicação assíncrona do JARVIS.
    """

    def __init__(self, logger=None):
        super().__init__("core.event_bus")
        self.version = "2.2"
        self.logger = logger
        
        self.listeners = defaultdict(list)
        self.max_history = 1000
        self.history = deque(maxlen=self.max_history)
        self.event_count = 0
        
        # Trava reentrante para gerenciar concorrência de cadastro e despacho
        self._lock = threading.RLock()

    # =====================================================
    # CICLO DE VIDA
    # =====================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        with self._lock:
            self.listeners.clear()
            self.history.clear()
            self.event_count = 0

            self.set_status(ModuleStatus.ONLINE)
            self.success("Event Bus iniciado em modo concorrente seguro")

    def shutdown(self):
        with self._lock:
            self.listeners.clear()
            self.set_status(ModuleStatus.OFFLINE)
            self.info("Event Bus encerrado")

    # =====================================================
    # INSCRIÇÃO
    # =====================================================

    def subscribe(self, event_name, callback):
        with self._lock:
            if callback not in self.listeners[event_name]:
                self.listeners[event_name].append(callback)
                self.info(f"Listener registrado para evento: {event_name}")

    def unsubscribe(self, event_name, callback):
        with self._lock:
            if event_name in self.listeners:
                if callback in self.listeners[event_name]:
                    self.listeners[event_name].remove(callback)
                    # Limpa a chave se não houver mais ouvintes
                    if not self.listeners[event_name]:
                        del self.listeners[event_name]

    # =====================================================
    # EMISSÃO DE EVENTOS
    # =====================================================

    def emit(self, event_name, *args, **kwargs):
        payload = None
        if args:
            payload = args[0]
        elif kwargs:
            payload = kwargs

        # Bloco com escopo de Lock reduzido: apenas para manipulação interna de estruturas
        with self._lock:
            self.event_count += 1
            event = {
                "id": self.event_count,
                "event": event_name,
                "payload": payload,
                "time": datetime.now().isoformat()
            }
            self.history.append(event)
            self.info(f"Evento emitido: {event_name}")
            
            # Captura uma cópia rápida da referência dos listeners atuais do evento
            targets = list(self.listeners.get(event_name, []))

        # Execução dos callbacks FORA da trava de sincronização principal do barramento.
        # Isso evita Deadlocks caso um callback precise chamar subscribe/emit de volta.
        for callback in targets:
            try:
                callback(*args, **kwargs)
            except Exception as error:
                self.error(f"Falha de execução no callback do evento '{event_name}': {str(error)}")

    # =====================================================
    # CONSULTAS
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

    # =====================================================
    # LOGGER INTERNO
    # =====================================================

    def info(self, message):
        if self.logger:
            self.logger.info(message)

    def success(self, message):
        if self.logger:
            self.logger.success(message)

    def error(self, message):
        if self.logger:
            self.logger.error(message)