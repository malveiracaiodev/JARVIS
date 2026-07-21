"""
=========================================
GENESIS CORE - COGNITIVE BRAIN ORCHESTRATOR

Arquivo: core/mind/brain.py
Descrição: Coordenador supremo dos estados e fluxos mentais.
Mark: IV - Thought Engine
=========================================
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from core.base.module import Module, ModuleStatus
from core.interfaces.brain_interface import BrainInterface
from core.mind.brain_state import BrainState

class BrainStatus(Enum):
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    ONLINE = "online"
    THINKING = "thinking"
    ERROR = "error"

class Brain(Module, BrainInterface):
    """
    Núcleo de orquestração do ecossistema. Conecta barramentos e executa pipelines.
    """

    def __init__(self, logger: Optional[Any] = None, event_bus: Optional[Any] = None):
        super().__init__("core.mind.brain")
        self.version = "Genesis Core Mark IV"
        self.logger = logger
        self.event_bus = event_bus
        
        self.state = BrainState(logger=self.logger)
        self.pipeline: Optional[Any] = None
        self._brain_status = BrainStatus.OFFLINE
        
        self.started_at: Optional[datetime] = None
        self.cycles = 0
        self.errors = 0

    def get_brain_status(self) -> BrainStatus:
        return self._brain_status

    def _log(self, level: str, message: str) -> None:
        if self.logger:
            method = getattr(self.logger, level, None)
            if callable(method):
                method(message)
                return
        print(f"[BRAIN] [{level.upper()}] {message}")

    def connect(self, pipeline: Optional[Any] = None, reasoner: Optional[Any] = None) -> None:
        if pipeline:
            self.pipeline = pipeline
        self._log("info", "Subsistemas da Thought Engine Mark IV acoplados com sucesso.")

    def initialize(self) -> bool:
        self._brain_status = BrainStatus.INITIALIZING
        self.set_status(ModuleStatus.INITIALIZING)
        
        self.state.initialize()
        self.started_at = datetime.now()
        
        self._brain_status = BrainStatus.ONLINE
        self.set_status(ModuleStatus.ONLINE)
        self._log("success", "Orquestrador Brain operativo e unificado.")
        return True

    def shutdown(self) -> bool:
        self.state.shutdown()
        self._brain_status = BrainStatus.OFFLINE
        self.set_status(ModuleStatus.OFFLINE)
        self._log("info", "Orquestrador Brain finalizado em segurança.")
        return True

    def process(self, input_data: Any) -> Any:
        if not self.pipeline:
            self.errors += 1
            self._brain_status = BrainStatus.ERROR
            return {"error": "Pipeline Cognitiva não conectada ao cérebro."}

        try:
            self._brain_status = BrainStatus.THINKING
            self.state.context.set_last_message(str(input_data))

            result = self.pipeline.process(input_data)
            self.cycles += 1

            self.state.add_history({
                "timestamp": datetime.now().isoformat(),
                "input": input_data,
                "result": result
            })

            self._brain_status = BrainStatus.ONLINE
            return result

        except Exception as error:
            self.errors += 1
            self._brain_status = BrainStatus.ERROR
            self._log("error", f"Exceção no processamento do cérebro: {error}")
            return {"error": str(error)}

    def remember(self, data: Any, memory_type: str = "general", importance: int = 1) -> Dict[str, Any]:
        return self.state.memory.store(data, memory_type, importance)

    def recall(self, query: str) -> Any:
        return self.state.memory.retrieve(query)

    def learn(self, topic: str, information: str, source: str = "internal", tags: Optional[list] = None) -> Dict[str, Any]:
        return self.state.knowledge.add(topic, information, source, tags)

    def search(self, query: str) -> Any:
        return self.state.knowledge.search(query)

    def reset(self) -> bool:
        if self.get_status() != ModuleStatus.ONLINE:
            return False
        self.state.context.clear_temporary()
        return True

    def get_brain_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": self._brain_status.value,
            "module_status": self.get_status().value,
            "pipeline": self.pipeline is not None,
            "cycles": self.cycles,
            "errors": self.errors,
            "state": self.state.snapshot()
        }