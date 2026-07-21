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
import traceback

class Worker(threading.Thread):
    def __init__(self, queue, logger=None):
        super().__init__(daemon=True)
        self.queue = queue
        self.logger = logger
        self._running = True

    def run(self):
        while self._running:
            task = self.queue.pop()
            if not task: continue
            
            try:
                # O Node processa e reporta telemetria de latência
                task.execute()
            except Exception:
                self.logger.error(f"Node Failure: {traceback.format_exc()}")