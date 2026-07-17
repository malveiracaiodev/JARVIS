"""
=========================================
JARVIS CORE

Arquivo:
core/services/diagnostics.py

Descrição:
Sistema de diagnóstico interno e
telemetria do Genesis Core.

Responsável por:

- Diagnóstico dos módulos
- Estado do Kernel
- Estado do Runtime
- Histórico circular
- Relatórios estruturados

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from collections import deque
from datetime import datetime

from core.base.module import (
    Module,
    ModuleStatus,
)


class Diagnostics(Module):
    """
    Sistema responsável pela inspeção da
    integridade do Genesis Core.
    """

    def __init__(self, kernel=None, logger=None):
        super().__init__("core.diagnostics")

        self.version = "3.0"

        self.kernel = kernel
        self.logger = logger

        self.max_history = 500
        self.history = deque(maxlen=self.max_history)

        self._lock = threading.RLock()

    # =====================================================
    # Ciclo de vida
    # =====================================================

    def initialize(self):

        with self._lock:

            self.set_status(ModuleStatus.INITIALIZING)

            self.history.clear()

            self.set_status(ModuleStatus.ONLINE)

        self.success("Diagnostics ONLINE.")

    def shutdown(self):

        self.set_status(ModuleStatus.OFFLINE)

        self.info("Diagnostics OFFLINE.")

    # =====================================================
    # Relatório
    # =====================================================

    def report(self):

        report = {
            "timestamp": datetime.now().isoformat(),
            "kernel": "OFFLINE",
            "health": 0,
            "state": "UNKNOWN",
            "modules": {},
            "runtime": {},
            "memory": 0,
            "tasks": 0,
        }

        if not self.kernel:
            return report

        with self._lock:

            report["kernel"] = self._kernel_status()

            report["modules"] = self._modules()

            report["health"] = self._health(report["modules"])

            report["memory"] = self._memory()

            report["state"] = self._state()

            report["tasks"] = self._tasks()

            report["runtime"] = self._runtime()

            self.history.append(report)

        return report

    # =====================================================
    # Coleta
    # =====================================================

    def _kernel_status(self):

        try:
            status = self.kernel.get_status()
            return status.name

        except Exception:
            return "UNKNOWN"

    def _modules(self):

        modules = {}

        try:

            for module in list(getattr(self.kernel, "modules", [])):

                name = getattr(module, "name", "Unknown")

                if hasattr(module, "get_status"):
                    status = module.get_status().name
                else:
                    status = getattr(module, "status", "UNKNOWN")

                    if hasattr(status, "name"):
                        status = status.name

                modules[name] = status

        except Exception:

            modules["error"] = "Falha ao coletar módulos"

        return modules

    def _health(self, modules):

        if not modules:
            return 0

        total = len(modules)

        online = sum(
            1
            for status in modules.values()
            if status == "ONLINE"
        )

        return round((online / total) * 100)

    def _memory(self):

        try:

            memory = getattr(self.kernel, "memory", None)

            if memory is None:
                return 0

            return len(getattr(memory, "memories", []))

        except Exception:

            return 0

    def _tasks(self):

        try:

            runtime = getattr(self.kernel, "runtime", None)

            if runtime:

                return runtime.queue.size()

            manager = getattr(self.kernel, "task_manager", None)

            if manager:

                return len(getattr(manager, "tasks", []))

        except Exception:
            pass

        return 0

    def _runtime(self):

        runtime = getattr(self.kernel, "runtime", None)

        if runtime is None:
            return {}

        try:
            return runtime.status()

        except Exception:
            return {}

    def _state(self):

        try:

            state = getattr(self.kernel, "state", None)

            if state:

                return state.get_state().value

        except Exception:
            pass

        return "UNKNOWN"

    # =====================================================
    # Histórico
    # =====================================================

    def get_history(self):

        with self._lock:
            return list(self.history)

    # =====================================================
    # Exibição
    # =====================================================

    def display(self):

        report = self.report()

        print("\n" + "=" * 60)
        print("             GENESIS CORE DIAGNOSTICS")
        print("=" * 60)

        print(f"Kernel : {report['kernel']}")
        print(f"Estado : {report['state']}")
        print(f"Health : {report['health']}%")

        runtime = report["runtime"]

        if runtime:

            print("-" * 60)
            print("Runtime")

            print(f"Workers : {runtime.get('active_workers', 0)}")
            print(f"Fila    : {runtime.get('pending_tasks', 0)}")
            print(f"Uptime  : {runtime.get('uptime_seconds', 0)} s")

        print("-" * 60)

        print("Módulos")

        for name, status in report["modules"].items():
            print(f"  {name:<30} [{status}]")

        print("-" * 60)

        print(f"Memórias : {report['memory']}")
        print(f"Tarefas  : {report['tasks']}")

        print("=" * 60)
        print()

    # =====================================================
    # Logging
    # =====================================================

    def info(self, message):
        if self.logger:
            self.logger.info(message)

    def success(self, message):
        if self.logger:
            self.logger.success(message)

    def warning(self, message):
        if self.logger:
            self.logger.warning(message)

    def error(self, message):
        if self.logger:
            self.logger.error(message)