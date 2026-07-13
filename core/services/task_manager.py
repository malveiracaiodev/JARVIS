"""
=========================================
JARVIS CORE

Arquivo:
task_manager.py

Descrição:
Gerenciador de tarefas do JARVIS.

Responsável por:
- Registrar tarefas
- Controlar estados
- Enviar tarefas ao Runtime

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.1 - Async Ready)

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from enum import Enum
import threading  # Adicionado para evitar concorrência bloqueante no fallback

from core.base.module import (
    Module,
    ModuleStatus
)

class TaskStatus(Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DISABLED = "DISABLED"

class Task:
    def __init__(self, name, function, priority=1):
        self.id = id(self)
        self.name = name
        self.function = function
        self.priority = priority
        self.status = TaskStatus.CREATED
        self.created = datetime.now()
        self.last_run = None
        self.executions = 0
        self.last_error = None

    def execute(self):
        try:
            self.status = TaskStatus.RUNNING
            self.last_error = None  # Correção: Limpa o erro anterior antes de rodar
            
            result = self.function()
            
            self.status = TaskStatus.COMPLETED
            self.executions += 1
            self.last_run = datetime.now()
            return result
            
        except Exception as error:
            self.status = TaskStatus.FAILED
            self.last_error = str(error)
            raise

class TaskManager(Module):
    """
    Gerenciador de tarefas do ecossistema Genesis.
    """
    def __init__(self, logger=None, event_bus=None, runtime=None):
        super().__init__("core.task_manager")
        self.version = "2.1"
        self.logger = logger
        self.event_bus = event_bus
        self.runtime = runtime
        self.tasks = {}

    # ======================================================
    # CICLO DE VIDA
    # ======================================================
    def initialize(self):
        self.set_status(ModuleStatus.ONLINE)
        self.log_success("Task Manager iniciado (v2.1 Async Ready)")

    def shutdown(self):
        self.tasks.clear()
        self.set_status(ModuleStatus.OFFLINE)
        self.log_info("Task Manager encerrado")

    # ======================================================
    # REGISTRO
    # ======================================================
    def register(self, task):
        self.tasks[task.name] = task
        self.emit("TASK_CREATED", {"id": task.id, "name": task.name})
        self.log_info(f"Tarefa registrada: {task.name}")

    def remove(self, name):
        if name in self.tasks:
            del self.tasks[name]
            self.emit("TASK_REMOVED", {"name": name})

    # ======================================================
    # EXECUÇÃO
    # ======================================================
    def execute(self, name):
        task = self.tasks.get(name)
        if not task:
            self.log_info(f"Tentativa de execução falhou: tarefa '{name}' não encontrada.")
            return False

        if task.status == TaskStatus.DISABLED:
            self.log_info(f"Tarefa '{name}' está desativada.")
            return False

        task.status = TaskStatus.QUEUED
        self.emit("TASK_QUEUED", {"id": task.id, "name": task.name})

        if self.runtime:
            # O Runtime assume a responsabilidade de gerenciar as threads/processos
            self.runtime.submit(task)
        else:
            # Fallback seguro: Executa em uma thread separada para não travar o Core do JARVIS
            thread = threading.Thread(target=self._run_task_safely, args=(task,), daemon=True)
            thread.start()

        return True

    def _run_task_safely(self, task):
        """Método auxiliar para executar tarefas em segundo plano sem quebrar o Core."""
        try:
            task.execute()
            self.emit("TASK_COMPLETED", {"id": task.id, "name": task.name})
        except Exception:
            self.emit("TASK_FAILED", {"id": task.id, "name": task.name, "error": task.last_error})

    # ======================================================
    # CONSULTAS
    # ======================================================
    def get(self, name):
        return self.tasks.get(name)

    def list_tasks(self):
        return list(self.tasks.keys())

    def report(self):
        return {
            name: {
                "id": task.id,
                "status": task.status.value,
                "executions": task.executions,
                "last_error": task.last_error,
                "last_run": task.last_run.isoformat() if task.last_run else None
            }
            for name, task in self.tasks.items()
        }

    # ======================================================
    # Auxiliares
    # ======================================================
    def emit(self, event, data):
        if self.event_bus:
            self.event_bus.emit(event, data)

    def log_info(self, message):
        if self.logger:
            self.logger.info(message)

    def log_success(self, message):
        if self.logger:
            self.logger.success(message)