"""
=========================================
JARVIS CORE

Arquivo:
engine.py

Descrição:
Motor e orquestrador principal de processamento assíncrono paralelo e ciclo de vida do Kernel.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from datetime import datetime
from core.base.module import Module, ModuleStatus
from core.runtime.queue import TaskQueue
from core.runtime.worker import Worker


class Runtime(Module):
    """
    Gerenciador unificado de execução em background. Controla o pool de workers e o barramento.
    """

    def __init__(self, logger=None, event_bus=None, worker_pool_size=2):
        super().__init__("core.runtime")
        self.version = "3.0"
        self.logger = logger
        self.event_bus = event_bus
        self.worker_count = worker_pool_size
        
        self.queue = TaskQueue()
        self.workers = []
        self.start_time = None
        self._lock = threading.RLock()

    def initialize(self):
        with self._lock:
            self.set_status(ModuleStatus.INITIALIZING)
            self.start_time = datetime.now()
            
            # Alocação e inicialização do Pool de Workers concorrentes
            self.workers = [
                Worker(queue=self.queue, logger=self.logger, event_bus=self.event_bus)
                for _ in range(self.worker_count)
            ]
            
            for worker in self.workers:
                worker.start()

            self.set_status(ModuleStatus.ONLINE)
            self.success(f"Motor de execução assíncrona ONLINE com Pool de {self.worker_count} Workers.")

    def start(self):
        self.initialize()

    def add_task(self, task):
        """
        Interface unificada consumida pelo Brain e Agentes para injetar tarefas em segundo plano.
        """
        self.queue.push(task)
        task_name = getattr(task, "name", task.__class__.__name__ if hasattr(task, "__class__") else "LambdaTask")
        self.info(f"Carga assíncrona acoplada à fila: '{task_name}'")

    def stop(self):
        with self._lock:
            self.set_status(ModuleStatus.OFFLINE)
            for worker in self.workers:
                worker.stop()
            self.workers.clear()
            self.info("Motor de execução assíncrona e workers finalizados.")

    def shutdown(self):
        self.stop()

    def status(self):
        with self._lock:
            return {
                "name": self.name,
                "version": self.version,
                "status": self.get_status().value,
                "pending_tasks": self.queue.size(),
                "active_workers": len(self.workers),
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
            }

    def info(self, msg):
        if self.logger: self.logger.info(msg)
    def success(self, msg):
        if self.logger: self.logger.success(msg)