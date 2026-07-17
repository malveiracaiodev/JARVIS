"""
=========================================
JARVIS CORE

Arquivo:
core/runtime/worker.py

Descrição:
Trabalhador concorrente para consumo
e execução isolada de tarefas da fila.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
import time

from core.events.task_events import TaskEvents


class Worker(threading.Thread):
    """
    Worker responsável por consumir tarefas da
    TaskQueue e executá-las em segundo plano.
    """

    def __init__(
        self,
        queue,
        logger=None,
        event_bus=None,
        name=None,
    ):
        super().__init__(
            name=name,
            daemon=True,
        )

        self.queue = queue
        self.logger = logger
        self.event_bus = event_bus

        self._stop_event = threading.Event()

    # =====================================================
    # Ciclo de vida
    # =====================================================

    def stop(self):
        self._stop_event.set()

    # =====================================================
    # Loop principal
    # =====================================================

    def run(self):

        self.log_success(
            f"{self.name} iniciado."
        )

        while not self._stop_event.is_set():

            task = self.queue.pop()

            if task is None:
                time.sleep(0.05)
                continue

            self.execute(task)

        self.log_info(
            f"{self.name} finalizado."
        )

    # =====================================================
    # Execução
    # =====================================================

    def execute(self, task):

        task_name = getattr(
            task,
            "name",
            task.__class__.__name__,
        )

        try:

            self.log_info(
                f"Executando tarefa: {task_name}"
            )

            self.emit(
                TaskEvents.STARTED,
                task=task_name,
            )

            if hasattr(task, "execute"):
                result = task.execute()

            elif callable(task):
                result = task()

            else:
                raise TypeError(
                    f"Tarefa '{task_name}' não é executável."
                )

            self.queue.complete(
                task,
                result,
            )

            self.emit(
                TaskEvents.COMPLETED,
                task=task_name,
                result=str(result),
            )

            self.log_success(
                f"Tarefa concluída: {task_name}"
            )

        except Exception as error:

            self.queue.fail(
                task,
                error,
            )

            self.emit(
                TaskEvents.FAILED,
                task=task_name,
                error=str(error),
            )

            self.log_error(
                f"Falha na tarefa '{task_name}': {error}"
            )

    # =====================================================
    # Eventos
    # =====================================================

    def emit(self, event, **payload):

        if not self.event_bus:
            return

        try:
            self.event_bus.emit(
                event,
                payload,
            )

        except Exception as error:
            self.log_error(
                f"Erro ao emitir evento '{event}': {error}"
            )

    # =====================================================
    # Logging
    # =====================================================

    def log_info(self, message):
        if self.logger:
            self.logger.info(message)

    def log_success(self, message):
        if self.logger:
            self.logger.success(message)

    def log_warning(self, message):
        if self.logger:
            self.logger.warning(message)

    def log_error(self, message):
        if self.logger:
            self.logger.error(message)