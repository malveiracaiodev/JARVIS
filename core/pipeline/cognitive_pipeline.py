"""
=========================================
GENESIS CORE - COGNITIVE PIPELINE ENGINE

Arquivo: core/pipeline/cognitive_pipeline.py
Descrição: Motor principal da Pipeline Cognitiva.
Mark: V - Evolution / Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from core.base.module import Module, ModuleStatus
from core.interfaces.pipeline_interface import PipelineInterface
from core.models.thought import Thought
from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.pipeline_step import PipelineStep


class CognitivePipeline(Module, PipelineInterface):
    """
    Gerencia e executa a sequência linear ordenada de etapas sobre um Thought (Mark V).
    """
    def __init__(self, name: str = "core.cognitive_pipeline"):
        self.steps_list: List[PipelineStep] = []
        self.history: List[Dict[str, Any]] = []
        self.errors: List[str] = []
        self._name: str = name
        super().__init__(name)

    def name(self) -> str:
        """Implementação do método abstrato exigido pela interface/base."""
        return self._name

    @property
    def status(self) -> ModuleStatus:
        """
        Retorna o objeto ModuleStatus diretamente para compatibilidade com a classe base.
        """
        if hasattr(self, "_state_lock") and hasattr(self, "_status"):
            with self._state_lock:
                return self._status
        return getattr(self, "_status", ModuleStatus.OFFLINE)

    @status.setter
    def status(self, new_status: Any) -> None:
        """Setter compatível com o controle de estado do Module e enums/strings."""
        if isinstance(new_status, str):
            try:
                new_status = ModuleStatus[new_status.upper()]
            except KeyError:
                new_status = ModuleStatus.OFFLINE

        if hasattr(self, "_state_lock") and hasattr(self, "_status") and hasattr(self, "_status_lock"):
            self.set_status(new_status)
        else:
            self._status = new_status

    # ==================================================
    # CICLO DE VIDA
    # ==================================================
    def initialize(self) -> bool:
        self.set_status(ModuleStatus.ONLINE)
        return True

    def shutdown(self) -> bool:
        self.steps_list.clear()
        self.set_status(ModuleStatus.OFFLINE)
        return True

    def reset(self) -> bool:
        self.steps_list.clear()
        self.history.clear()
        self.errors.clear()
        return True

    # ==================================================
    # ETAPAS
    # ==================================================
    def add_step(self, step: PipelineStep) -> None:
        if not isinstance(step, PipelineStep):
            raise TypeError("PipelineStep inválido.")
        self.steps_list.append(step)

    def remove_step(self, step_name: str) -> None:
        self.steps_list = [step for step in self.steps_list if step.name != step_name]

    def steps(self) -> List[PipelineStep]:
        return self.steps_list

    def list_steps(self) -> List[str]:
        return [step.name for step in self.steps_list]

    # ==================================================
    # PROCESSAMENTO
    # ==================================================
    def process(self, thought: Thought, context: Optional[PipelineContext] = None) -> PipelineContext:
        if thought is None:
            raise ValueError("Thought não pode ser None.")

        if context is None:
            context = PipelineContext(thought)

        context.start()
        self.history.append({
            "event": "pipeline_started",
            "thought": thought.id,
            "timestamp": datetime.now().isoformat()
        })

        for step in self.steps_list:
            try:
                context.update_step(step.name)
                context = step.run(context)
                if context.has_errors():
                    break
            except Exception as error:
                context.add_error(str(error))
                self.errors.append(str(error))
                break

        if context.has_errors():
            context.fail()
        else:
            context.complete()

        self.history.append({
            "event": "pipeline_finished",
            "thought": thought.id,
            "errors": len(context.errors),
            "timestamp": datetime.now().isoformat()
        })

        return context

    # ==================================================
    # MONITORAMENTO & HISTÓRICO
    # ==================================================
    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

    def get_errors(self) -> List[str]:
        return self.errors

    def clear_history(self) -> None:
        self.history.clear()

    def clear_errors(self) -> None:
        self.errors.clear()

    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Expositor de telemetria do motor.
        """
        current_status = self.status.name if hasattr(self.status, "name") else str(self.status)
        return {
            "name": self._name,
            "status": current_status,
            "steps": self.list_steps(),
            "history": len(self.history),
            "errors": len(self.errors)
        }