"""
=========================================
GENESIS CORE - SYSTEM LIFECYCLE EVENTS

Arquivo: core/events/system_events.py
Descrição: Eventos estruturais do núcleo do Genesis.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemEvents:
    """
    Eventos globais do sistema. Representa o ciclo de vida completo do Genesis Core.
    """

    # Boot do Sistema
    BOOT_STARTED: str = "system.boot.started"
    BOOT_COMPLETED: str = "system.boot.completed"
    START: str = "system.start"
    READY: str = "system.ready"

    # Kernel
    KERNEL_CREATED: str = "system.kernel.created"
    KERNEL_STARTED: str = "system.kernel.started"
    KERNEL_READY: str = "system.kernel.ready"
    KERNEL_RESTARTED: str = "system.kernel.restarted"

    # Encerramento
    SHUTDOWN_REQUESTED: str = "system.shutdown.requested"
    SHUTDOWN: str = "system.shutdown"
    SHUTDOWN_COMPLETED: str = "system.shutdown.completed"

    # Módulos
    MODULE_LOADING: str = "system.module.loading"
    MODULE_STARTED: str = "system.module.started"
    MODULE_READY: str = "system.module.ready"
    MODULE_STOPPED: str = "system.module.stopped"
    MODULE_FAILED: str = "system.module.failed"
    MODULE_RESTARTED: str = "system.module.restarted"

    # Serviços
    SERVICE_STARTED: str = "system.service.started"
    SERVICE_STOPPED: str = "system.service.stopped"
    SERVICE_FAILED: str = "system.service.failed"

    # Configuração
    CONFIG_LOADED: str = "system.config.loaded"
    CONFIG_CHANGED: str = "system.config.changed"

    # Monitoramento
    HEALTH_CHECK: str = "system.health.check"
    HEALTH_WARNING: str = "system.health.warning"
    HEALTH_CRITICAL: str = "system.health.critical"
    RESOURCE_WARNING: str = "system.resource.warning"

    # Runtime
    TASK_STARTED: str = "system.task.started"
    TASK_COMPLETED: str = "system.task.completed"
    TASK_FAILED: str = "system.task.failed"

    # Telemetria
    METRIC_UPDATED: str = "system.metric.updated"
    STATUS_CHANGED: str = "system.status.changed"

    # Erros
    ERROR: str = "system.error"
    CRASH: str = "system.crash"