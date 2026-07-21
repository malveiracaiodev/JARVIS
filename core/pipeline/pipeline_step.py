"""
=========================================
GENESIS CORE - PIPELINE STEP BASE

Arquivo: core/pipeline/pipeline_step.py
Descrição: Classe base para as etapas da Pipeline Cognitiva.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional
from core.pipeline.pipeline_context import PipelineContext

class PipelineStep(ABC):
    """
    Classe abstrata base para as etapas da Pipeline Cognitiva.
    """
    def __init__(self, name: str):
        self._name: str = name
        self.status: str = "created"
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None
        self.execution_time: float = 0.0

    @property
    def name(self) -> str:
        return self._name

    def execute(self, context: PipelineContext) -> PipelineContext:
        return self.run(context)

    def run(self, context: PipelineContext) -> PipelineContext:
        if not isinstance(context, PipelineContext):
            raise TypeError("PipelineStep precisa receber PipelineContext.")

        self.started_at = datetime.now()
        self.status = "processing"

        context.add_history({
            "event": "step_started",
            "step": self.name,
            "timestamp": self.started_at.isoformat()
        })

        try:
            result = self.process(context)
            if not isinstance(result, PipelineContext):
                raise TypeError(f"A etapa {self.name} não retornou um PipelineContext.")

            self.finished_at = datetime.now()
            self.status = "completed"
            self.execution_time = (self.finished_at - self.started_at).total_seconds()

            result.add_history({
                "event": "step_completed",
                "step": self.name,
                "duration": self.execution_time,
                "timestamp": self.finished_at.isoformat()
            })
            return result

        except Exception as error:
            self.status = "failed"
            self.finished_at = datetime.now()

            context.add_error({
                "step": self.name,
                "error": str(error)
            })
            context.add_history({
                "event": "step_failed",
                "step": self.name,
                "error": str(error),
                "timestamp": datetime.now().isoformat()
            })
            return context

    @abstractmethod
    def process(self, context: PipelineContext) -> PipelineContext:
        raise NotImplementedError()

    def get_name(self) -> str:
        return self.name

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "execution_time": self.execution_time
        }

    def __repr__(self) -> str:
        return f"<PipelineStep:{self.name}>"