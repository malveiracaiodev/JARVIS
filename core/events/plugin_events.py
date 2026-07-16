"""
=========================================
GENESIS CORE

Arquivo:
core/events/plugin_events.py

Descrição:
Eventos relacionados ao ciclo de vida
dos plugins e extensões dinâmicas.

Responsável por comunicação entre:

- PluginManager
- Registry
- Kernel
- Diagnostics
- Runtime

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from dataclasses import dataclass



@dataclass(
    frozen=True
)
class PluginEvents:

    """
    Barramento de eventos do sistema
    de extensões dinâmicas.

    Permite evolução do Genesis
    sem alterar o núcleo.
    """



    # ==================================================
    # DESCOBERTA
    # ==================================================


    DISCOVERED: str = (
        "plugin.discovered"
    )


    SCANNING: str = (
        "plugin.scanning"
    )



    # ==================================================
    # CARREGAMENTO
    # ==================================================


    LOADING: str = (
        "plugin.loading"
    )


    LOADED: str = (
        "plugin.loaded"
    )


    INITIALIZED: str = (
        "plugin.initialized"
    )


    STARTED: str = (
        "plugin.started"
    )



    # ==================================================
    # EXECUÇÃO
    # ==================================================


    EXECUTING: str = (
        "plugin.executing"
    )


    EXECUTED: str = (
        "plugin.executed"
    )



    # ==================================================
    # ATUALIZAÇÃO
    # ==================================================


    UPDATE_AVAILABLE: str = (
        "plugin.update.available"
    )


    UPDATED: str = (
        "plugin.updated"
    )



    # ==================================================
    # DEPENDÊNCIAS
    # ==================================================


    DEPENDENCY_CHECK: str = (
        "plugin.dependency.check"
    )


    DEPENDENCY_FAILED: str = (
        "plugin.dependency.failed"
    )



    # ==================================================
    # REMOÇÃO
    # ==================================================


    STOPPING: str = (
        "plugin.stopping"
    )


    UNLOADING: str = (
        "plugin.unloading"
    )


    UNLOADED: str = (
        "plugin.unloaded"
    )


    REMOVED: str = (
        "plugin.removed"
    )



    # ==================================================
    # ESTADOS
    # ==================================================


    ENABLED: str = (
        "plugin.enabled"
    )


    DISABLED: str = (
        "plugin.disabled"
    )



    # ==================================================
    # SEGURANÇA
    # ==================================================


    PERMISSION_REQUIRED: str = (
        "plugin.permission.required"
    )


    SECURITY_BLOCKED: str = (
        "plugin.security.blocked"
    )



    # ==================================================
    # ERROS
    # ==================================================


    ERROR: str = (
        "plugin.error"
    )


    CRASHED: str = (
        "plugin.crashed"
    )