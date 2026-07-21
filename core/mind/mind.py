"""
=========================================
GENESIS CORE - CENTRAL MIND CONTROL

Arquivo: core/mind/mind.py
Descrição: Orquestrador primário e emissor de objetos estruturados Thought.
Mark: IV - Thought Engine
=========================================
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from core.base.module import Module
from core.models.thought import Thought

class Mind(Module):
    """
    Controlador do ciclo de vida cognitivo. Instancia os 'Thoughts' e gerencia a Pipeline.
    """

    def __init__(
        self,
        tool_manager: Optional[Any] = None,
        logger: Optional[Any] = None,
        event_bus: Optional[Any] = None,
        config: Optional[Any] = None,
        identity: Optional[Any] = None,
        service_manager: Optional[Any] = None,
        runtime: Optional[Any] = None,
        engine: Optional[Any] = None,
        pipeline: Optional[Any] = None,
    ):
        super().__init__("mind")
        self.tool_manager = tool_manager
        self.logger = logger
        self.event_bus = event_bus
        self.config = config
        self.identity = identity
        self.service_manager = service_manager
        self.runtime = runtime or engine
        self.pipeline = pipeline

        self.last_thought: Optional[Thought] = None
        self.history: List[Dict[str, Any]] = []
        self.status = "OFFLINE"

    def initialize(self) -> None:
        self.status = "ONLINE"
        if self.event_bus:
            self.event_bus.emit("mind.started", {"time": datetime.now().isoformat()})
        self.log("Mente central unificada ONLINE no Mark IV.")

    def shutdown(self) -> None:
        self.status = "OFFLINE"
        self.log("Mente central deslogada.")

    def think(self, text: str) -> Any:
        try:
            if not self.pipeline:
                return "Pipeline cognitiva indisponível."

            # Instanciação estruturada do Thought (Mark IV)
            thought = Thought(
                message=text,
                metadata={
                    "identity": self.identity,
                    "history_size": len(self.history),
                    "created_by": "mind",
                    "received_at": datetime.now().isoformat()
                }
            )

            self.last_thought = thought
            if hasattr(thought, "processing"):
                thought.processing()
            if hasattr(thought, "add_history"):
                thought.add_history("thought_created")

            # Varredura dinâmica de execução da Pipeline
            if hasattr(self.pipeline, "process"):
                result = self.pipeline.process(thought)
            elif hasattr(self.pipeline, "run"):
                result = self.pipeline.run(thought)
            elif hasattr(self.pipeline, "execute"):
                result = self.pipeline.execute(thought)
            else:
                raise RuntimeError("A Pipeline acoplada não possui método de execução válido.")

            if hasattr(thought, "set_result"):
                thought.set_result(result)
            if hasattr(thought, "is_finished") and not thought.is_finished():
                if hasattr(thought, "completed"):
                    thought.completed()

            if hasattr(thought, "add_history"):
                thought.add_history("thought_finished")

            self.history.append({
                "thought_id": getattr(thought, "id", None),
                "input": text,
                "status": getattr(thought, "status", "completed"),
                "confidence": getattr(thought, "confidence", 1.0),
                "execution_time": getattr(thought, "execution_time", 0.0),
                "time": datetime.now().isoformat()
            })

            return result

        except Exception as error:
            if self.last_thought and hasattr(self.last_thought, "failed"):
                try:
                    self.last_thought.failed()
                    if hasattr(self.last_thought, "set_metadata"):
                        self.last_thought.set_metadata("exception", str(error))
                except Exception:
                    pass
            if self.logger:
                self.logger.error(f"Erro no ciclo cognitivo: {error}")
            return f"[FALHA COGNITIVA]: {error}"

    def get_brain_status(self) -> Dict[str, Any]:
        return {
            "name": "Genesis Mind",
            "status": self.status,
            "pipeline": self.pipeline is not None,
            "thoughts": len(self.history),
            "last_thought": self.last_thought.id if self.last_thought else None
        }

    def learn(self, data: Any) -> bool:
        self.log("Disparo automático de absorção de dados estruturados.")
        return True

    def reset(self) -> bool:
        self.last_thought = None
        self.history.clear()
        return True

    def log(self, message: str) -> None:
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[MIND] {message}")