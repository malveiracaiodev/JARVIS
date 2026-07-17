"""
=========================================
JARVIS CORE

Arquivo:
core/runtime/queue.py

Descrição:
Fila de execução concorrente e thread-safe
com priorização dinâmica de tarefas.

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
    Fila inteligente thread-safe responsável por
    armazenar, priorizar e despachar tarefas.

    Mantém histórico de execução e suporta
    priorização dinâmica.
    """

    def __init__(self):
        self.tasks = []
        self.history = []
        self._lock = threading.RLock()

    # =====================================================
    # Inserção
    # =====================================================

    def push(self, task):
        with self._lock:

            if hasattr(task, "queued_at"):
                task.queued_at = datetime.now()

            if hasattr(task, "status"):
                status_enum = task.status.__class__
                if hasattr(status_enum, "QUEUED"):
                    task.status = status_enum.QUEUED

            self.tasks.append(task)

            self._sort()

    # =====================================================
    # Remoção
    # =====================================================

    def pop(self):
        with self._lock:

            if not self.tasks:
                return None

            return self.tasks.pop(0)

    def peek(self):
        with self._lock:

            if not self.tasks:
                return None

            return self.tasks[0]

    # =====================================================
    # Finalização
    # =====================================================

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

    # =====================================================
    # Consulta
    # =====================================================

    def pending(self):
        with self._lock:
            return list(self.tasks)

    def logs(self):
        with self._lock:
            return list(self.history)

    def size(self):
        with self._lock:
            return len(self.tasks)

    def empty(self):
        with self._lock:
            return len(self.tasks) == 0

    # =====================================================
    # Manutenção
    # =====================================================

    def clear(self):
        with self._lock:
            self.tasks.clear()
            self.history.clear()

    # =====================================================
    # Utilidades
    # =====================================================

    def _sort(self):
        self.tasks.sort(
            key=lambda task: getattr(task, "priority", 0),
            reverse=True,
        )

    def __len__(self):
        return self.size()