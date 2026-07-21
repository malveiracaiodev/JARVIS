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
import heapq
import threading
import time

class TaskQueue:
    """Fila de prioridade O(log n) para o padrão Lattice."""
    def __init__(self):
        self._buffer = []
        self._lock = threading.RLock()

    def push(self, task):
        with self._lock:
            # Heapq armazena tuplas: (prioridade, timestamp, task)
            priority = getattr(task, "priority", 0)
            heapq.heappush(self._buffer, (-priority, time.time(), task))

    def pop(self):
        with self._lock:
            if not self._buffer: return None
            return heapq.heappop(self._buffer)[2]