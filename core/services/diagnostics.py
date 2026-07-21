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
import copy
from collections import deque
from datetime import datetime
from core.base.module import Module, ModuleStatus

class Diagnostics(Module):
    """
    Sistema de diagnóstico robusto (Mark III - Matrix).
    """

    def __init__(self, kernel=None, logger=None):
        super().__init__("core.diagnostics")
        self.version = "3.1"
        self.kernel = kernel
        self.logger = logger
        
        self.max_history = 500
        self.history = deque(maxlen=self.max_history)
        self._lock = threading.RLock() # RLock para segurança em chamadas recursivas

    # =====================================================
    # Relatório com Proteção contra Falhas
    # =====================================================

    def report(self):
        """Gera um snapshot estruturado do sistema."""
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
            # Coleta isolada para evitar que falhas em sub-módulos bloqueiem o relatório
            report.update({
                "kernel": self._kernel_status(),
                "modules": self._modules(),
                "memory": self._memory(),
                "state": self._state(),
                "tasks": self._tasks(),
                "runtime": self._runtime()
            })
            
            # Cálculo de saúde dependente dos módulos coletados
            report["health"] = self._health(report["modules"])
            
            # Armazena cópia profunda para manter o histórico imutável
            self.history.append(copy.deepcopy(report))

        return report

    def _modules(self):
        """Coleta o estado dos módulos com tolerância total a erros."""
        modules = {}
        try:
            # Uso de list() para evitar RuntimeError se a lista mudar durante iteração
            kernel_modules = list(getattr(self.kernel, "modules", []))
            for module in kernel_modules:
                name = getattr(module, "name", "Unknown")
                try:
                    status = module.get_status().name if hasattr(module, "get_status") else getattr(module, "status", "UNKNOWN")
                    modules[name] = status.name if hasattr(status, "name") else str(status)
                except Exception:
                    modules[name] = "ERROR_INSPECTING"
        except Exception as e:
            self.error(f"Falha severa na inspeção de módulos: {e}")
            modules["error"] = "Falha no coletor"
        return modules

    def _health(self, modules):
        if not modules: return 0
        
        # Filtra entradas de erro antes do cálculo
        valid_statuses = [s for s in modules.values() if s != "ERROR_INSPECTING"]
        if not valid_statuses: return 0
        
        online = sum(1 for status in valid_statuses if status == "ONLINE")
        return round((online / len(valid_statuses)) * 100)

    # ... [Manter _kernel_status, _memory, _tasks, _runtime, _state] ...
    # (Eles já estão bem estruturados, apenas certifique-se de usar getattr com default)

    def display(self):
        """Exibição segura dos dados processados."""
        report = self.report()
        
        print(f"\n{'='*60}\n GENESIS CORE DIAGNOSTICS ({report['timestamp']})\n{'='*60}")
        print(f"Kernel : {report['kernel']} | Estado : {report['state']} | Health : {report['health']}%")

        runtime = report["runtime"]
        if runtime:
            print(f"{'-'*60}\nRuntime: Workers: {runtime.get('active_workers', 0)} | Fila: {runtime.get('pending_tasks', 0)} | Uptime: {runtime.get('uptime_seconds', 0)}s")

        print(f"{'-'*60}\nMódulos:")
        for name, status in report["modules"].items():
            print(f"  {name:<30} [{status}]")
            
        print(f"{'-'*60}\nMemórias: {report['memory']} | Tarefas: {report['tasks']}\n{'='*60}\n")