"""
=========================================
JARVIS CORE

Arquivo:
core/services/task_manager.py

Descrição:
Gerenciador central de tarefas do Genesis Core.

Responsável por:
- Criar tarefas
- Controlar ciclo de execução
- Gerenciar estados
- Integrar com Runtime
- Monitorar resultados

Arquitetura:
Genesis Core

Mark:
III - Matrix (Task Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

import copy
import threading
import uuid
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

from core.base.module import Module, ModuleStatus

class TaskStatus(Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    DISABLED = "DISABLED"

class Task:
    """Unidade de execução atômica do Genesis Core (Mark III)."""
    def __init__(self, name, function, priority=1):
        self.id = str(uuid.uuid4())
        self.name = name
        self.function = function
        self.priority = priority
        self.status = TaskStatus.CREATED
        self.created = datetime.now()
        self.started = None
        self.last_run = None
        self.finished = None
        self.executions = 0
        self.duration = 0.0
        self.last_error = None
        self._lock = threading.Lock()

    def execute(self):
        """Execução encapsulada com medição de performance."""
        start = datetime.now()
        with self._lock:
            self.status = TaskStatus.RUNNING
            self.started = start
        
        try:
            result = self.function()
            finish = datetime.now()
            with self._lock:
                self.status = TaskStatus.COMPLETED
                self.executions += 1
                self.finished = finish
                self.last_run = finish
                self.duration = (finish - start).total_seconds()
            return result
        except Exception as e:
            with self._lock:
                self.status = TaskStatus.FAILED
                self.last_error = str(e)
            raise

class TaskManager(Module):
    """
    Controlador de Tarefas Mark III.
    Gerenciamento via ThreadPoolExecutor para controle de carga.
    """
    def __init__(self, logger=None, event_bus=None, runtime=None, max_workers=5):
        super().__init__("core.task_manager")
        self.version = "3.1"
        self.logger = logger
        self.event_bus = event_bus
        self.runtime = runtime
        self.tasks = {}
        self._lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def execute(self, name):
        """Execução delegada ao Runtime ou Pool de Threads interno."""
        with self._lock:
            task = self.tasks.get(name)
            if not task or task.status == TaskStatus.DISABLED:
                return False
            task.status = TaskStatus.QUEUED
        
        # Prioridade para o Runtime, fallback para thread local segura
        if self.runtime:
            return self.runtime.submit(task)
            
        self._executor.submit(self._run_task_safely, task)
        return True

    def _run_task_safely(self, task):
        """Invólucro para monitoramento de telemetria de execução."""
        self.emit("TASK_QUEUED", {"id": task.id, "name": task.name})
        try:
            task.execute()
            self.emit("TASK_COMPLETED", {"id": task.id, "name": task.name})
        except Exception as e:
            self.log_error(f"Falha na execução de {task.name}: {e}")
            self.emit("TASK_FAILED", {"id": task.id, "name": task.name, "error": str(e)})

    def shutdown(self):
        """Encerramento ordenado com drenagem do executor."""
        with self._lock:
            self._executor.shutdown(wait=True)
            self.tasks.clear()
        self.set_status(ModuleStatus.OFFLINE)