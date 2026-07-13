"""
=========================================
JARVIS CORE

Arquivo:
system_monitor.py

Descrição:
Monitor de saúde do sistema e hardware.

Responsável por:
- Verificar integridade de módulos
- Coletar telemetria de hardware (CPU/RAM)
- Calcular saúde operacional real
- Evitar vazamentos de memória no histórico

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.1 - Hardware Aware)

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from collections import deque
import os
import psutil  # Biblioteca recomendada para monitoramento de hardware

from core.base.module import (
    Module,
    ModuleStatus
)

from core.events import SystemEvents

class SystemMonitor(Module):
    """
    Monitora a saúde interna de software e hardware do JARVIS.
    """

    def __init__(self, kernel=None, logger=None, event_bus=None, max_history=100):
        super().__init__("core.system_monitor")
        self.version = "2.1"
        self.kernel = kernel
        self.logger = logger
        self.event_bus = event_bus

        self.health = 100
        # Evita estouro de memória limitando o histórico das últimas X medições
        self.history = deque(maxlen=max_history)

    # ==========================================================
    # Ciclo de vida
    # ==========================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)

        if self.event_bus:
            self.event_bus.subscribe(
                SystemEvents.READY,
                self.system_ready
            )

        self.set_status(ModuleStatus.ONLINE)
        self.log_success("System Monitor iniciado (v2.1 Telemetry Ready)")

    def shutdown(self):
        if self.event_bus:
            self.event_bus.unsubscribe(
                SystemEvents.READY,
                self.system_ready
            )

        self.history.clear()
        self.set_status(ModuleStatus.OFFLINE)
        self.log_info("System Monitor encerrado")

    # ==========================================================
    # Eventos
    # ==========================================================

    def system_ready(self, *args, **kwargs):
        self.log_info("Sistema pronto. Iniciando diagnóstico completo.")
        self.check_health()

    # ==========================================================
    # Diagnóstico
    # ==========================================================

    def check_health(self):
        if not self.kernel:
            self.health = 0
            return 0

        modules = getattr(self.kernel, "modules", [])
        total_modules = len(modules)
        
        # 1. Avaliação de Módulos (Software)
        online_modules = 0
        degraded_modules = 0

        if total_modules > 0:
            for module in modules:
                # Verifica se o método existe e o estado atual
                if hasattr(module, "is_online") and module.is_online():
                    # Uma verificação extra caso você decida adicionar a propriedade 'errors' no futuro
                    if getattr(module, "errors", 0) > 5:
                        degraded_modules += 1
                    else:
                        online_modules += 1

            # Cálculo base de software (0-100)
            software_health = (online_modules / total_modules) * 100
            if degraded_modules > 0:
                software_health -= (degraded_modules / total_modules) * 50
        else:
            software_health = 100  # Kernel sem módulos adicionais está saudável por padrão

        # 2. Avaliação de Recursos (Hardware)
        # Importante para monitorar gargalos causados por IAs locais ou conexões de rede
        try:
            cpu_usage = psutil.cpu_percent(interval=None)
            ram_usage = psutil.virtual_memory().percent
        except Exception:
            # Fallback caso a biblioteca psutil não esteja instalada no ambiente ainda
            cpu_usage = 0
            ram_usage = 0

        # Penaliza a saúde se o hardware estiver superaquecendo/sobrecarregado (acima de 90%)
        hardware_penalty = 0
        if cpu_usage > 90: hardware_penalty += 15
        if ram_usage > 90: hardware_penalty += 20

        # Calcular saúde final ponderada
        self.health = max(0, min(100, int(software_health - hardware_penalty)))

        report = {
            "health": self.health,
            "software": {
                "total_modules": total_modules,
                "online": online_modules,
                "degraded": degraded_modules
            },
            "hardware": {
                "cpu_percent": cpu_usage,
                "ram_percent": ram_usage
            },
            "time": datetime.now().isoformat()
        }

        self.history.append(report)

        # Logs inteligentes baseados no estado do sistema
        if self.health < 70:
            self.log_info(f"ALERTA: Saúde do sistema degradada: {self.health}% | CPU: {cpu_usage}% | RAM: {ram_usage}%")
            self.emit("SYSTEM_HEALTH_DEGRADED", report)
        else:
            self.log_info(f"Saúde do sistema: {self.health}% (Módulos: {online_modules}/{total_modules})")

        if self.event_bus:
            self.event_bus.emit(SystemEvents.HEALTH_CHECK, report)

        return self.health

    def get_health(self):
        return self.health

    def get_history(self):
        # Converte o deque de volta para lista na hora da leitura externa
        return list(self.history)

    # ==========================================================
    # Auxiliares
    # ==========================================================

    def emit(self, event, data):
        if self.event_bus:
            self.event_bus.emit(event, data)

    def log_info(self, message):
        if self.logger:
            self.logger.info(message)

    def log_success(self, message):
        if self.logger:
            self.logger.success(message)