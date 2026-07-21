"""
=========================================
GENESIS CORE - PIPELINE CONTEXT

Arquivo: core/pipeline/pipeline_context.py
Descrição: Contexto compartilhado da Pipeline Cognitiva.
Mark: V - Evolution / Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from core.models.thought import Thought


class PipelineContext:
    """
    Ambiente temporário da Pipeline (Mark V). Transporta o estado de uma execução cognitiva.
    """
    def __init__(self, thought: Optional[Thought] = None):
        self.thought: Optional[Thought] = thought
        self.result: Any = None
        self.data: Dict[str, Any] = {}

        # Componentes Injetados
        self.agent: Any = None
        self.persona: Any = None
        self.memory: Any = None
        self.knowledge: Any = None
        self.tools: List[Any] = []

        # Execução
        self.status: str = "created"
        self.current_step: Optional[str] = None
        self.created_at: datetime = datetime.now()
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None

        # Controle
        self.metadata: Dict[str, Any] = {}
        self.history: List[Union[str, Dict[str, Any]]] = []
        self.errors: List[Any] = []

    # ==================================================
    # THOUGHT
    # ==================================================
    def set_thought(self, thought: Thought) -> "PipelineContext":
        self.thought = thought
        return self

    def get_thought(self) -> Optional[Thought]:
        return self.thought

    def has_thought(self) -> bool:
        return self.thought is not None

    # ==================================================
    # RESULTADO
    # ==================================================
    def set_result(self, result: Any) -> "PipelineContext":
        self.result = result
        if self.thought:
            self.thought.set_result(result)
        return self

    def get_result(self) -> Any:
        return self.result

    # ==================================================
    # COMPONENTES
    # ==================================================
    def set_agent(self, agent: Any) -> "PipelineContext":
        self.agent = agent
        return self

    def set_persona(self, persona: Any) -> "PipelineContext":
        self.persona = persona
        return self

    def set_memory(self, memory: Any) -> "PipelineContext":
        self.memory = memory
        return self

    def set_knowledge(self, knowledge: Any) -> "PipelineContext":
        self.knowledge = knowledge
        return self

    def add_tool(self, tool: Any) -> "PipelineContext":
        self.tools.append(tool)
        return self

    # ==================================================
    # CICLO DO CONTEXTO
    # ==================================================
    def start(self) -> "PipelineContext":
        self.status = "processing"
        self.started_at = datetime.now()
        self.add_history("pipeline_started")
        return self

    def complete(self) -> "PipelineContext":
        self.status = "completed"
        self.finished_at = datetime.now()
        self.add_history("pipeline_completed")
        return self

    def fail(self, error: Optional[Any] = None) -> "PipelineContext":
        self.status = "failed"
        self.finished_at = datetime.now()
        if error:
            self.add_error(error)
        return self

    def is_completed(self) -> bool:
        return self.status == "completed"

    def is_failed(self) -> bool:
        return self.status == "failed"

    # ==================================================
    # ETAPA ATUAL
    # ==================================================
    def update_step(self, step_name: str) -> "PipelineContext":
        self.current_step = step_name
        self.add_history({
            "event": "step_changed",
            "step": step_name,
            "timestamp": datetime.now().isoformat()
        })
        return self

    # ==================================================
    # DADOS OPACOS / INTERNOS
    # ==================================================
    def set(self, key: str, value: Any) -> "PipelineContext":
        self.data[key] = value
        return self

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def contains(self, key: str) -> bool:
        return key in self.data

    # ==================================================
    # METADATA
    # ==================================================
    def set_metadata(self, key: str, value: Any) -> "PipelineContext":
        self.metadata[key] = value
        return self

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    # ==================================================
    # HISTÓRICO
    # ==================================================
    def add_history(self, event: Union[str, Dict[str, Any]]) -> "PipelineContext":
        if isinstance(event, str):
            event = {
                "event": event,
                "timestamp": datetime.now().isoformat()
            }
        self.history.append(event)
        if self.thought:
            self.thought.add_history(event)
        return self

    # ==================================================
    # ERROS
    # ==================================================
    def add_error(self, error: Any) -> "PipelineContext":
        self.errors.append(error)
        self.add_history({
            "event": "error",
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        })
        return self

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    # ==================================================
    # MÉTRICAS
    # ==================================================
    def metrics(self) -> Dict[str, Any]:
        duration = None
        if self.started_at and self.finished_at:
            duration = (self.finished_at - self.started_at).total_seconds()
        return {
            "status": self.status,
            "current_step": self.current_step,
            "history": len(self.history),
            "errors": len(self.errors),
            "duration": duration
        }

    # ==================================================
    # LIMPEZA
    # ==================================================
    def clear(self) -> "PipelineContext":
        self.data.clear()
        self.metadata.clear()
        self.history.clear()
        self.errors.clear()
        self.current_step = None
        self.result = None
        return self

    # ==================================================
    # SERIALIZAÇÃO
    # ==================================================
    def to_dict(self) -> Dict[str, Any]:
        return {
            "thought": self.thought.to_dict() if self.thought else None,
            "result": self.result,
            "status": self.status,
            "current_step": self.current_step,
            "data": self.data,
            "metadata": self.metadata,
            "history": self.history,
            "errors": self.errors,
            "metrics": self.metrics(),
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None
        }

    def summary(self) -> Dict[str, Any]:
        return self.to_dict()

    def __repr__(self) -> str:
        thought_id = self.thought.id[:8] if self.thought else "None"
        return f"PipelineContext(thought={thought_id}, step={self.current_step}, status={self.status}, errors={len(self.errors)})"