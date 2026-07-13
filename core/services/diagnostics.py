"""
=========================================
JARVIS CORE

Arquivo:
diagnostics.py

Descrição:
Sistema de diagnóstico interno e integridade.

Responsável por:
- Gerar relatórios dinâmicos de subsistemas
- Verificar o estado operacional dos módulos do Kernel
- Exibir telemetria estruturada no terminal
- Rastreamento seguro do histórico de status

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.1 - Resilient)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from collections import deque
from datetime import datetime

from core.base.module import (
    Module,
    ModuleStatus
)


class Diagnostics(Module):
    """
    Sistema de diagnóstico e telemetria de integridade do JARVIS.
    """

    def __init__(self, kernel=None, logger=None):
        super().__init__("core.diagnostics")
        self.version = "2.1"
        self.kernel = kernel
        self.logger = logger

        # Evita vazamento de memória usando histórico circular controlado
        self.max_history = 500
        self.history = deque(maxlen=self.max_history)
        
        # Lock para isolamento em coletas simultâneas de relatórios
        self._lock = threading.Lock()

    # ==========================================================
    # Ciclo de Vida
    # ==========================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        with self._lock:
            self.history.clear()
            
        self.set_status(ModuleStatus.ONLINE)
        self.success("Diagnostics iniciado com sucesso")

    def shutdown(self):
        self.set_status(ModuleStatus.OFFLINE)
        self.info("Diagnostics encerrado")

    # ==========================================================
    # Relatório
    # ==========================================================

    def report(self):
        # Template padrão seguro
        report = {
            "time": datetime.now().isoformat(),
            "kernel": "OFFLINE",
            "modules": {},
            "health": 0,
            "memory": 0,
            "state": "UNKNOWN",
            "tasks": 0
        }

        if not self.kernel:
            return report

        with self._lock:
            try:
                # Extração segura do status do Kernel
                kernel_status = self.kernel.get_status()
                report["kernel"] = kernel_status.name if kernel_status else "UNKNOWN"
            except Exception as e:
                report["kernel"] = f"ERROR ({type(e).__name__})"

            # Módulos ativos (Tratamento thread-safe para varreduras dinâmicas)
            try:
                modules_list = list(getattr(self.kernel, "modules", []))
                for module in modules_list:
                    if hasattr(module, "name") and hasattr(module, "status"):
                        report["modules"][module.name] = module.status.name
            except Exception:
                report["modules"] = {"error": "Falha ao ler árvore de módulos"}

            # Coleta individual isolada dos subsistemas do Kernel
            try:
                monitor = getattr(self.kernel, "monitor", None)
                if monitor:
                    report["health"] = getattr(monitor, "health", 0)
            except Exception:
                report["health"] = -1

            try:
                memory = getattr(self.kernel, "memory", None)
                if memory:
                    report["memory"] = len(getattr(memory, "memories", []))
            except Exception:
                report["memory"] = 0

            try:
                state_manager = getattr(self.kernel, "state", None)
                if state_manager:
                    report["state"] = state_manager.get_state().value
            except Exception:
                report["state"] = "UNSTABLE"

            try:
                task_manager = getattr(self.kernel, "task_manager", None)
                if task_manager:
                    report["tasks"] = len(getattr(task_manager, "tasks", []))
            except Exception:
                report["tasks"] = 0

            # Adiciona ao histórico circular protegido
            self.history.append(report)

        return report

    # ==========================================================
    # Histórico e Exibição
    # ==========================================================

    def get_history(self):
        with self._lock:
            return list(self.history)

    def display(self):
        report = self.report()

        print("\n" + "=" * 45)
        print("         JARVIS CORE DIAGNOSTICS")
        print("=" * 45)
        print(f"Kernel Status : {report['kernel']}")
        print(f"System State  : {report['state']}")
        print(f"Core Health   : {report['health']}%")
        print("-" * 45)
        print("Módulos Identificados:")
        
        if report["modules"]:
            for name, status in report["modules"].items():
                print(f"  ▪ {name:<20} -> [{status}]")
        else:
            print("  (Nenhum módulo registrado)")
            
        print("-" * 45)
        print(f"Memórias Ativas : {report['memory']}")
        print(f"Tarefas Ativas  : {report['tasks']}")
        print("=" * 45 + "\n")

    # ==========================================================
    # Atalhos de Mensagens (Encaminhados para a Logger Base)
    # ==========================================================

    def info(self, message):
        if self.logger:
            self.logger.info(message)

    def success(self, message):
        if self.logger:
            self.logger.success(message)

    def error(self, message):
        if self.logger:
            self.logger.error(message)