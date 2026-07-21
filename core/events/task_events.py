"""
=========================================
GENESIS CORE - TASK LIFECYCLE EVENTS

Arquivo: core/events/task_events.py
Descrição: Eventos do ciclo de vida de tarefas gerenciadas pelo TaskManager.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskEvents:
    """
    Catálogo de eventos do sistema de execução de tarefas.
    """

    # Criação
    CREATED: str = "task.lifecycle.created"
    REGISTERED: str = "task.lifecycle.registered"

    # Fila
    QUEUED: str = "task.lifecycle.queued"
    PRIORITY_CHANGED: str = "task.lifecycle.priority.changed"

    # Execução
    STARTED: str = "task.lifecycle.started"
    RUNNING: str = "task.lifecycle.running"
    PROGRESS_UPDATED: str = "task.lifecycle.progress.updated"

    # Controle
    WAITING: str = "task.lifecycle.waiting"
    PAUSED: str = "task.lifecycle.paused"
    RESUMED: str = "task.lifecycle.resumed"
    CANCEL_REQUESTED: str = "task.lifecycle.cancel.requested"
    CANCELLED: str = "task.lifecycle.cancelled"

    # Finalização
    COMPLETED: str = "task.lifecycle.completed"
    FAILED: str = "task.lifecycle.failed"
    TIMEOUT: str = "task.lifecycle.timeout"

    # Recuperação
    RETRY_REQUESTED: str = "task.lifecycle.retry.requested"
    RETRIED: str = "task.lifecycle.retried"

    # Resultados
    RESULT_AVAILABLE: str = "task.result.available"
    FEEDBACK_CREATED: str = "task.feedback.created"

    # Sistema
    RESOURCE_REQUIRED: str = "task.resource.required"
    DEPENDENCY_WAITING: str = "task.dependency.waiting"
    ERROR: str = "task.error"