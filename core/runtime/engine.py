"""
=========================================
JARVIS CORE

Arquivo:
core/runtime/engine.py

Descrição:
Motor e orquestrador principal de processamento
assíncrono paralelo e ciclo de vida do Kernel.

Arquitetura:
Genesis Core

Mark:
III - Matrix (Mark IV - Neural Lattice)

Autor:
Caio Vitor Malveira
=========================================
"""

import os
import threading
from concurrent.futures import ProcessPoolExecutor
from core.base.module import Module, ModuleStatus


class Runtime(Module):
    """
    Motor Mark IV (Neural Lattice).
    Isolamento por Processos (Memory-Safe) e Backpressure-Ready.
    """

    def __init__(self, logger=None, event_bus=None, max_workers=None, worker_pool_size=None, **kwargs):
        super().__init__("core.runtime")
        self.version = "4.0-Lattice"
        self.logger = logger
        self.event_bus = event_bus
        self.max_workers = max_workers or worker_pool_size or os.cpu_count()
        self._executor = None
        self._lock = threading.RLock()
        
        # Mantém as métricas padrão da classe base Module e adiciona as específicas do Lattice
        self.metrics.update({
            "active_lattice_nodes": 0,
            "throughput": 0
        })

    # ==================================================
    # CICLO DE VIDA (CONTRATOS OBRIGATÓRIOS DO MODULE)
    # ==================================================

    def initialize(self):
        """Inicializa o executor do Neural Lattice."""
        with self._lock:
            if self.is_online():
                return

            self.set_status(ModuleStatus.INITIALIZING)
            try:
                if self._executor is None:
                    self._executor = ProcessPoolExecutor(max_workers=self.max_workers)
                
                self.metrics["active_lattice_nodes"] = 0
                self.set_status(ModuleStatus.ONLINE)

                if self.logger:
                    self.logger.success(f"Runtime Lattice Mark IV online (Workers: {self.max_workers}).")
            except Exception as error:
                self.set_error(f"Falha ao inicializar o Runtime: {error}")
                if self.logger:
                    self.logger.error(self.error_message)
                raise

    def shutdown(self):
        """Encerra o executor do Lattice de forma limpa."""
        with self._lock:
            self.set_status(ModuleStatus.OFFLINE)
            try:
                if self._executor:
                    self._executor.shutdown(wait=True, cancel_futures=True)
                    self._executor = None
            except Exception as error:
                if self.logger:
                    self.logger.error(f"Erro ao encerrar executor do Runtime: {error}")

            if self.logger:
                self.logger.info("Runtime Lattice encerrado.")

    # ==================================================
    # PROCESSAMENTO E SUBMISSÃO
    # ==================================================

    def submit(self, task):
        """Alocação dinâmica para o Lattice Node."""
        with self._lock:
            if not self.is_online() or self._executor is None:
                if self.logger:
                    self.logger.warning("Tentativa de submissão com Runtime offline.")
                return False

            try:
                self.metrics["active_lattice_nodes"] += 1
                future = self._executor.submit(task.execute)
                future.add_done_callback(self._on_lattice_node_complete)
                return True
            except Exception as error:
                self.metrics["active_lattice_nodes"] = max(0, self.metrics["active_lattice_nodes"] - 1)
                if self.logger:
                    self.logger.error(f"Erro ao submeter tarefa ao Lattice: {error}")
                return False

    def _on_lattice_node_complete(self, future):
        with self._lock:
            self.metrics["active_lattice_nodes"] = max(0, self.metrics["active_lattice_nodes"] - 1)
            self.metrics["throughput"] += 1
            
            try:
                exception = future.exception()
                if exception and self.logger:
                    self.logger.error(f"Erro em nó da Lattice: {exception}")
            except Exception:
                pass