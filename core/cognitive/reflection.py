"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/reflection.py

Descrição:
Módulo final de reflexão cognitiva (Mark V - Evolution).

Responsável por avaliar o ciclo completo
de um Thought e persistir o aprendizado
diretamente na memória de longo prazo.

Arquitetura:
Genesis Core

Mark:
V - Evolution / Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.pipeline.pipeline_step import (
    PipelineStep
)
from core.pipeline.pipeline_context import (
    PipelineContext
)


class Reflection(
    PipelineStep
):
    """
    Última etapa da Thought Engine na Mark V.
    Transforma execuções em experiências cognitivas persistentes.
    """

    def __init__(
        self,
        logger: Optional[Any] = None,
        memory: Optional[Any] = None
    ) -> None:
        super().__init__(
            "reflection"
        )

        self.logger = logger
        self.memory = memory  # Injeção do coordenador de memória de longo prazo
        self.reflections: int = 0
        self.failures: int = 0
        self.history: List[Dict[str, Any]] = []

    def process(
        self,
        context: PipelineContext
    ) -> PipelineContext:
        try:
            thought = context.thought

            if thought is None:
                context.add_error(
                    "Reflection recebeu Context sem Thought na malha neural."
                )
                return context

            reflection = self.analyze(
                thought
            )

            thought.set_metadata(
                "reflection",
                reflection
            )

            lesson = self.extract_lesson(
                reflection
            )

            thought.set_metadata(
                "lesson",
                lesson
            )

            # ==========================================
            # INTEGRAÇÃO COM A MEMÓRIA DE LONGO PRAZO (MARK V)
            # ==========================================
            if self.memory and hasattr(self.memory, "store"):
                try:
                    self.memory.store(
                        data=lesson,
                        memory_type="episodic"
                    )
                except Exception as mem_error:
                    self.log_error(f"Falha ao persistir lição na memória: {mem_error}")

            context.set(
                "reflection",
                reflection
            )

            context.add_history(
                {
                    "step": "reflection",
                    "status": "completed",
                    "timestamp": datetime.now().isoformat()
                }
            )

            self.reflections += 1
            self.history.append(
                reflection
            )

            if reflection.get("success", False):
                thought.confidence = reflection.get("quality", 1.0)
                thought.completed()
            else:
                thought.failed()

            return context

        except Exception as error:
            self.failures += 1

            self.log_error(
                str(error)
            )

            if context.thought:
                context.thought.set_metadata(
                    "reflection_error",
                    str(error)
                )
                context.thought.failed()

            context.add_error(
                str(error)
            )

            return context

    def analyze(
        self,
        thought: Any
    ) -> Dict[str, Any]:
        result = thought.result
        success: bool = False

        if isinstance(
            result,
            dict
        ):
            success = result.get(
                "success",
                False
            )
        elif result is not None:
            success = True

        quality: float = (
            1.0
            if success
            else 0.0
        )

        if success:
            evaluation = (
                "Execução cognitiva concluída com sucesso na Mark V."
            )
            improvement = (
                "Estratégia registrada e validada no sistema de memória."
            )
        else:
            evaluation = (
                "Execução apresentou falhas no ciclo cognitivo."
            )
            improvement = (
                "Reavaliar intenção, planejamento ou ferramentas utilizadas."
            )

        return {
            "id": str(
                uuid.uuid4()
            ),
            "thought_id": thought.id,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "quality": quality,
            "evaluation": evaluation,
            "improvement": improvement,
            "cognition": {
                "intention": thought.intention,
                "plan": thought.plan,
                "decision": thought.decision
            },
            "execution": result
        }

    def extract_lesson(
        self,
        reflection: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "id": str(
                uuid.uuid4()
            ),
            "type": "cognitive_experience",
            "success": reflection.get(
                "success"
            ),
            "quality": reflection.get(
                "quality"
            ),
            "lesson": reflection.get(
                "improvement"
            ),
            "created_at": datetime.now().isoformat()
        }

    def log_error(
        self,
        message: str
    ) -> None:
        if self.logger and hasattr(self.logger, "error"):
            self.logger.error(
                message
            )

    def info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "reflections": self.reflections,
            "failures": self.failures,
            "memory_connected": self.memory is not None,
            "history": len(
                self.history
            )
        }