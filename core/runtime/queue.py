"""
=========================================
JARVIS CORE

Arquivo:
queue.py

Descrição:
Fila de execução concorrente e thread-safe com priorização dinâmica de tarefas.

Arquitetura:
Genesis Core

Mark:
III - Matrix (Runtime Engine)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from datetime import datetime


class TaskQueue:
    """
    Fila inteligente thread-safe para priorização e despacho de cargas cognitivas e operacionais.
    """

    def __init__(self):
        self.tasks = []
        self.history = []
        self._lock = threading.RLock()

    def push(self, task):
        with self._lock:
            if hasattr(task, "status") and hasattr(task.status, "__class__"):
                if hasattr(task.status.__class__, "QUEUED"):
                    task.status = task.status.__class__.QUEUED
            
            self.tasks.append(task)
            self.sort()

    def sort(self):
        with self._lock:
            # Ordenação estável priorizando maiores valores numéricos de prioridade
            self.tasks.sort(
                key=lambda t: getattr(t, "priority", 0),
                reverse=True
            )

    def next(self):
        with self._lock:
            return self.tasks.pop(0) if self.tasks else None

    def complete(self, task, result=None):
        with self._lock:
            if hasattr(task, "result"):
                task.result = result
            if hasattr(task, "finished"):
                task.finished = datetime.now()
            self.history.append(task)

    def fail(self, task, error):
        with self._lock:
            if hasattr(task, "last_error"):
                task.last_error = str(error)
            if hasattr(task, "finished"):
                task.finished = datetime.now()
            self.history.append(task)

    def pending(self):
        with self._lock:
            return list(self.tasks)

    def logs(self):
        with self._lock:
            return list(self.history)

    def size(self):
        with self._lock:
            return len(self.tasks)