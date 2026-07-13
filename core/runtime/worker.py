"""
=========================================
JARVIS CORE

Arquivo:
worker.py

Descrição:
Trabalhador concorrente para esvaziamento e execução isolada de tarefas da fila.

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
from core.events.task_events import TaskEvents  # Catálogo estrito de barramento do Mark III


class Worker:
    """
    Agente de subprocessamento encarregado de consumir a TaskQueue sem travar o loop do Kernel.
    """

    def __init__(self, queue, logger=None, event_bus=None):
        self.queue = queue
        self.logger = logger
        self.event_bus = event_bus
        self.running = False
        self.thread = None
        self._lock = threading.RLock()

    def start(self):
        with self._lock:
            if self.running:
                return

            self.running = True
            self.thread = threading.Thread(
                target=self._loop,
                name=f"JARVIS_Worker_{threading.get_ident()}",
                daemon=True
            )
            self.thread.start()
            self.log_success("Trabalhador assíncrono acoplado e em escuta ativa.")

    def _loop(self):
        while True:
            with self._lock:
                if not self.running:
                    break
            
            task = self.queue.next()
            if task:
                self.execute(task)
            else:
                time.sleep(0.1)  # Latência otimizada para diminuir overhead de CPU em ociosidade

    def execute(self, task):
        task_name = getattr(task, "name", task.__class__.__name__)
        try:
            self.log_info(f"Executando tarefa mapeada: {task_name}")
            self.emit(TaskEvents.STARTED, {"task": task_name})

            # Suporte a objetos Task estruturados ou simples callables (funções lambda anônimas)
            if hasattr(task, "execute"):
                result = task.execute()
            else:
                result = task()

            self.queue.complete(task, result)
            self.emit(TaskEvents.COMPLETED, {"task": task_name, "result": str(result)})
            self.log_success(f"Tarefa concluída com sucesso: {task_name}")

        except Exception as error:
            self.queue.fail(task, error)
            self.emit(TaskEvents.FAILED, {"task": task_name, "error": str(error)})
            self.log_error(f"Falha de runtime na execução da tarefa '{task_name}': {error}")

    def stop(self):
        with self._lock:
            self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        self.log_info("Trabalhador assíncrono desacoplado.")

    def emit(self, event, data):
        if self.event_bus:
            self.event_bus.emit(event, data)

    def log_info(self, message):
        if self.logger: self.logger.info(message)

    def log_success(self, message):
        if self.logger: self.logger.success(message)

    def log_error(self, message):
        if self.logger: self.logger.error(message)