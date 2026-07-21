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
import copy
from collections import defaultdict, deque
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from core.base.module import Module, ModuleStatus


class EventBus(Module):
    """
    Barramento central de eventos com execução isolada e resiliente (Mark III).
    """
    GLOBAL_EVENT = "*"

    def __init__(self, logger=None, max_workers=4):
        super().__init__("core.event_bus")
        self.version = "3.1"
        self.logger = logger
        self.listeners = defaultdict(list)
        self.max_history = 1000
        self.history = deque(maxlen=self.max_history)
        self.event_count = 0
        self._lock = threading.RLock()
        
        # Executor para evitar bloqueio do EventBus por listeners lentos
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="EventBus-Worker"
        )

    # ==================================================
    # CICLO DE VIDA (CONTRATOS OBRIGATÓRIOS)
    # ==================================================

    def initialize(self):
        with self._lock:
            if self.is_online():
                return

            self.set_status(ModuleStatus.INITIALIZING)
            self.set_status(ModuleStatus.ONLINE)
            
            if self.logger:
                self.logger.success("EventBus online e operacional.")

    def shutdown(self):
        with self._lock:
            self.set_status(ModuleStatus.OFFLINE)
            
            try:
                self._executor.shutdown(wait=True, cancel_futures=True)
            except Exception:
                pass

            if self.logger:
                self.logger.info("EventBus encerrado.")

    # ==================================================
    # EMISSÃO E DISPATCH
    # ==================================================

    def emit(self, event_name, *args, **kwargs):
        """Emissão atômica com dispatch isolado."""
        payload = args[0] if args else (kwargs if kwargs else None)

        with self._lock:
            self.event_count += 1
            event = {
                "id": self.event_count,
                "event": event_name,
                "payload": copy.deepcopy(payload),
                "time": datetime.now().isoformat(),
            }
            self.history.append(event)
            
            # Captura snapshots seguros das listas de listeners
            targets = list(self.listeners.get(event_name, []))
            globals_ = list(self.listeners.get(self.GLOBAL_EVENT, []))

        # Execução fora do Lock para permitir processamento paralelo
        self._dispatch(targets, event_name, *args, **kwargs)
        self._dispatch(globals_, event_name, *args, **kwargs, is_global=True)

    def _dispatch(self, callbacks, event_name, *args, **kwargs):
        """Dispara callbacks de forma isolada."""
        is_global = kwargs.pop("is_global", False)
        
        for callback in callbacks:
            def runner(cb, en, *a, **kw):
                try:
                    if is_global:
                        cb(en, *a, **kw)
                    else:
                        cb(*a, **kw)
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Erro no listener {'global' if is_global else en}: {e}")
            
            # Dispara no pool de threads para não bloquear o emissor
            self._executor.submit(runner, callback, event_name, *args, **kwargs)

    # ==================================================
    # GERENCIAMENTO DE LISTENERS
    # ==================================================

    def on(self, event_name, callback):
        """Registra um listener para um evento específico."""
        with self._lock:
            if callback not in self.listeners[event_name]:
                self.listeners[event_name].append(callback)

    def off(self, event_name, callback):
        """Remove um listener de um evento."""
        with self._lock:
            if callback in self.listeners[event_name]:
                self.listeners[event_name].remove(callback)

    def get_stats(self):
        """Retorna estatísticas do barramento de eventos."""
        with self._lock:
            return {
                "event_count": self.event_count,
                "history_size": len(self.history),
                "registered_events": list(self.listeners.keys())
            }