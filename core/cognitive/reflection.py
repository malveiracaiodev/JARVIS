"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/reflection.py

Descrição:
Módulo final de reflexão cognitiva (Mark IV - Neural Lattice).

Responsável por avaliar o ciclo completo
de um Thought após execução dentro da malha neural.

Analisa:

- intenção;
- plano;
- decisão;
- execução;
- resultado;
- aprendizado integrado à Lattice.

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice / Thought Engine

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
    Última etapa da Thought Engine na Neural Lattice.

    Responsável por transformar uma
    execução em experiência cognitiva na malha neural.

    Não executa.
    Não decide.

    Aprende com o resultado.
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
        self.memory = memory
        self.reflections: int = 0
        self.failures: int = 0
        self.history: List[Dict[str, Any]] = []

    # ==================================================
    # PIPELINE
    # ==================================================

    def process(
        self,
        context: PipelineContext
    ) -> PipelineContext:
        try:
            thought = context.thought

            if thought is None:
                context.add_error(
                    "Reflection recebeu Context sem Thought na Neural Lattice."
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

            # ==========================================
            # FINALIZA THOUGHT
            # ==========================================

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

    # ==================================================
    # ANÁLISE
    # ==================================================

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
                "Execução cognitiva concluída na Neural Lattice."
            )
            improvement = (
                "Estratégia registrada como eficiente na malha."
            )
        else:
            evaluation = (
                "Execução apresentou falhas na Lattice."
            )
            improvement = (
                "Reavaliar intenção, "
                "planejamento ou ferramentas no espaço de estados."
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

    # ==================================================
    # APRENDIZADO
    # ==================================================

    def extract_lesson(
        self,
        reflection: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "id": str(
                uuid.uuid4()
            ),
            "type": "lattice_experience",
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

    # ==================================================
    # COMPARAÇÃO
    # ==================================================

    def compare(
        self,
        expected: Any,
        actual: Any
    ) -> Dict[str, Any]:
        return {
            "expected": expected,
            "actual": actual,
            "match": expected == actual,
            "timestamp": datetime.now().isoformat()
        }

    # ==================================================
    # MELHORIAS
    # ==================================================

    def suggest_improvement(
        self,
        reflection: Optional[Dict[str, Any]]
    ) -> List[str]:
        if not reflection:
            return []

        if not reflection.get(
            "success",
            False
        ):
            return [
                "Reavaliar intenção na Lattice.",
                "Criar novo plano estruturado.",
                "Buscar outra estratégia ou ferramenta."
            ]

        return [
            "Registrar padrão eficiente na malha.",
            "Reutilizar estratégia cognitiva."
        ]

    # ==================================================
    # LOG
    # ==================================================

    def log_error(
        self,
        message: str
    ) -> None:
        if self.logger and hasattr(self.logger, "error"):
            self.logger.error(
                message
            )

    # ==================================================
    # STATUS
    # ==================================================

    def info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "reflections": self.reflections,
            "failures": self.failures,
            "history": len(
                self.history
            )
        }