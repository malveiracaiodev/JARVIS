"""
=========================================
JARVIS CORE

Arquivo:
core/services/system_monitor.py

Descrição:
Monitor de saúde do Genesis Core.

Responsável por:
- Diagnóstico de módulos
- Telemetria de hardware
- Avaliação operacional
- Histórico de saúde do sistema

Arquitetura:
Genesis Core

Mark:
III - Matrix (Monitoring Layer)

Autor:
Caio Vitor Malveira
=========================================
"""
import threading
from datetime import datetime
from collections import deque
try:
    import psutil
except ImportError:
    psutil = None

from core.base.module import Module, ModuleStatus
from core.events import SystemEvents

class SystemMonitor(Module):
    """
    Monitor de saúde Mark III (Matrix).
    Foco em telemetria de precisão e diagnóstico multicamada.
    """

    def __init__(self, kernel=None, logger=None, event_bus=None, max_history=200):
        super().__init__("core.system_monitor")
        self.version = "3.1"
        self.kernel = kernel
        self.logger = logger
        self.event_bus = event_bus
        self.health = 100
        self.history = deque(maxlen=max_history)
        self._lock = threading.RLock()

    # ... [initialize e shutdown inalterados] ...

    def check_health(self):
        """Diagnóstico consolidado com pesos de severidade (Matrix)."""
        with self._lock:
            software = self.check_modules()
            hardware = self.check_hardware()

            # Cálculo de penalidade baseado em thresholds críticos
            penalty = 0
            if hardware["cpu_percent"] > 90: penalty += 15
            if hardware["ram_percent"] > 90: penalty += 20
            if hardware["disk_percent"] > 95: penalty += 10
            
            # Escalonamento de saúde
            raw_health = int(software["score"] - penalty)
            self.health = max(0, min(100, raw_health))

            report = {
                "health": self.health,
                "software": software,
                "hardware": hardware,
                "timestamp": datetime.now().isoformat()
            }

            self.history.append(report)
            self._handle_health_events(report)
            
            return self.health

    def _handle_health_events(self, report):
        """Orquestrador de eventos de saúde."""
        if self.health < 70:
            self.log_error(f"Alerta de degradação: {self.health}%")
            self.emit("SYSTEM_HEALTH_DEGRADED", report)
        else:
            self.log_info(f"Saúde operacional: {self.health}%")
        
        self.emit(SystemEvents.HEALTH_CHECK, report)

    def check_modules(self):
        """Análise de prontidão dos serviços do núcleo."""
        modules = getattr(self.kernel, "modules", []) if self.kernel else []
        total = len(modules)
        if total == 0: return {"total": 0, "score": 100}

        online = 0
        degraded = 0

        for m in modules:
            try:
                # Validação de status de interface
                if getattr(m, "is_online", lambda: False)():
                    online += 1
                    if getattr(m, "errors", 0) > 5:
                        degraded += 1
                else:
                    degraded += 1
            except Exception:
                degraded += 1

        # Score ponderado: (Online - Degraded) / Total
        score = max(0, ((online - degraded) / total) * 100)
        return {"total_modules": total, "online": online, "degraded": degraded, "score": score}

    def check_hardware(self):
        """Telemetria de hardware via psutil (Fallback seguro)."""
        stats = {"cpu_percent": 0.0, "ram_percent": 0.0, "disk_percent": 0.0, "temp": None}
        if not psutil: return stats

        try:
            stats["cpu_percent"] = psutil.cpu_percent(interval=0.1)
            stats["ram_percent"] = psutil.virtual_memory().percent
            stats["disk_percent"] = psutil.disk_usage("/").percent
            
            # Extração térmica segura
            temps = psutil.sensors_temperatures()
            if temps:
                first_key = next(iter(temps))
                stats["temp"] = temps[first_key][0].current
        except Exception as e:
            self.log_error(f"Erro na telemetria de hardware: {e}")
            
        return stats