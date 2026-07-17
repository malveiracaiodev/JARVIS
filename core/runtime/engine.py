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

import os
import threading
from datetime import datetime

from core.base.module import Module, ModuleStatus
from core.runtime.queue import TaskQueue
from core.runtime.worker import Worker


class Runtime(Module):
    """
    Gerenciador unificado de execução em background.

    Responsável por:

    • Gerenciar o pool de Workers
    • Receber tarefas assíncronas
    • Distribuir tarefas na fila
    • Coletar métricas de execução
    • Controlar o ciclo de vida do Runtime

    Não executa lógica cognitiva.
    Não conhece Brain.
    Não conhece IA.
    Apenas coordena a infraestrutura de execução.
    """

    def __init__(
        self,
        logger=None,
        event_bus=None,
        worker_pool_size=None,
    ):
        super().__init__("core.runtime")

        self.version = "3.1"

        self.logger = logger
        self.event_bus = event_bus

        # Número automático de Workers
        if worker_pool_size is None:
            cpu = os.cpu_count() or 2
            self.worker_count = max(2, cpu)
        else:
            self.worker_count = max(1, worker_pool_size)

        self.queue = TaskQueue()

        self.workers = []

        self.start_time = None

        self._lock = threading.RLock()

        # Métricas
        self.metrics = {
            "queued_tasks": 0,
            "processed_tasks": 0,
            "failed_tasks": 0,
            "running_tasks": 0,
            "queue_peak": 0,
        }

    # =====================================================
    # Ciclo de vida
    # =====================================================

    def initialize(self):
        with self._lock:

            if self.get_status() == ModuleStatus.ONLINE:
                self.info("Runtime já está ONLINE.")
                return

            self.set_status(ModuleStatus.INITIALIZING)

            self.start_time = datetime.now()

            self.workers = [
                Worker(
                    queue=self.queue,
                    logger=self.logger,
                    event_bus=self.event_bus,
                )
                for _ in range(self.worker_count)
            ]

            for worker in self.workers:
                worker.start()

            self.set_status(ModuleStatus.ONLINE)

            self.success(
                f"Motor de execução ONLINE com {self.worker_count} Workers."
            )

            self._emit("runtime.started")

    def start(self):
        self.initialize()

    def stop(self):
        with self._lock:

            if self.get_status() == ModuleStatus.OFFLINE:
                return

            self.set_status(ModuleStatus.STOPPING)

            for worker in self.workers:
                worker.stop()

            # Aguarda encerramento das threads
            for worker in self.workers:
                worker.join()

            self.workers.clear()

            self.set_status(ModuleStatus.OFFLINE)

            self.info("Runtime finalizado.")

            self._emit("runtime.stopped")

    def shutdown(self):
        self.stop()

    # =====================================================
    # Fila
    # =====================================================

    def add_task(self, task):
        """
        Adiciona uma tarefa à fila de execução.
        """

        self.queue.push(task)

        self.metrics["queued_tasks"] += 1

        queue_size = self.queue.size()

        if queue_size > self.metrics["queue_peak"]:
            self.metrics["queue_peak"] = queue_size

        task_name = getattr(
            task,
            "name",
            task.__class__.__name__
            if hasattr(task, "__class__")
            else "LambdaTask",
        )

        self.info(
            f"Carga assíncrona adicionada à fila: '{task_name}'"
        )

        self._emit(
            "runtime.task.queued",
            task=task_name,
        )

    # =====================================================
    # Consulta
    # =====================================================

    def status(self):
        with self._lock:

            uptime = 0

            if self.start_time:
                uptime = (
                    datetime.now() - self.start_time
                ).total_seconds()

            return {
                "name": self.name,
                "version": self.version,
                "status": self.get_status().value,
                "worker_count": self.worker_count,
                "active_workers": len(self.workers),
                "pending_tasks": self.queue.size(),
                "uptime_seconds": round(uptime, 2),
                "metrics": self.metrics.copy(),
            }

    # =====================================================
    # Eventos
    # =====================================================

    def _emit(self, event, **payload):
        if self.event_bus:
            try:
                self.event_bus.emit(event, **payload)
            except Exception as e:
                self.info(f"Falha ao emitir evento '{event}': {e}")

    # =====================================================
    # Logging
    # =====================================================

    def info(self, msg):
        if self.logger:
            self.logger.info(msg)

    def success(self, msg):
        if self.logger:
            self.logger.success(msg)

    def warning(self, msg):
        if self.logger:
            self.logger.warning(msg)

    def error(self, msg):
        if self.logger:
            self.logger.error(msg)