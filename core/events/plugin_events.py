"""
=========================================
GENESIS CORE - PLUGINS LIFECYCLE EVENTS

Arquivo: core/events/plugin_events.py
Descrição: Eventos do ciclo de vida dos plugins e extensões dinâmicas.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PluginEvents:
    """
    Barramento de eventos do sistema de extensões dinâmicas.
    """

    # Descoberta
    DISCOVERED: str = "plugin.discovered"
    SCANNING: str = "plugin.scanning"

    # Carregamento
    LOADING: str = "plugin.loading"
    LOADED: str = "plugin.loaded"
    INITIALIZED: str = "plugin.initialized"
    STARTED: str = "plugin.started"

    # Execução
    EXECUTING: str = "plugin.executing"
    EXECUTED: str = "plugin.executed"

    # Atualização
    UPDATE_AVAILABLE: str = "plugin.update.available"
    UPDATED: str = "plugin.updated"

    # Dependências
    DEPENDENCY_CHECK: str = "plugin.dependency.check"
    DEPENDENCY_FAILED: str = "plugin.dependency.failed"

    # Remoção
    STOPPING: str = "plugin.stopping"
    UNLOADING: str = "plugin.unloading"
    UNLOADED: str = "plugin.unloaded"
    REMOVED: str = "plugin.removed"

    # Estados
    ENABLED: str = "plugin.enabled"
    DISABLED: str = "plugin.disabled"

    # Segurança
    PERMISSION_REQUIRED: str = "plugin.permission.required"
    SECURITY_BLOCKED: str = "plugin.security.blocked"

    # Erros
    ERROR: str = "plugin.error"
    CRASHED: str = "plugin.crashed"