"""
=========================================
JARVIS CORE

Arquivo:
core/events/task_events.py

Descrição:
Catálogo estrito de eventos de ciclo de vida de tarefas para o barramento.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

class TaskEvents:
    """
    Identificadores padronizados para eventos disparados pelo subsistema Runtime.
    """
    STARTED = "task.lifecycle.started"
    COMPLETED = "task.lifecycle.completed"
    FAILED = "task.lifecycle.failed"