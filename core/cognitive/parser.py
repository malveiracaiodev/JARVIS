"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/parser.py

Descrição:
Primeira etapa da Pipeline Cognitiva do Genesis Core (Mark V - Evolution).

Responsável por transformar entradas
brutas em estruturas cognitivas dentro da malha neural.

Arquitetura:
Genesis Core

Mark:
V - Evolution / Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from typing import Any, Dict, Optional

from core.interfaces.parser_interface import (
    ParserInterface
)
from core.pipeline.pipeline_step import (
    PipelineStep
)
from core.pipeline.pipeline_context import (
    PipelineContext
)


class Parser(
    PipelineStep,
    ParserInterface
):
    """
    Primeira etapa cognitiva na Neural Lattice.

    Responsabilidades:

    - interpretar entrada;
    - identificar tipo;
    - estruturar dados.

    Não raciocina.
    Não planeja.
    Não executa.
    """

    def __init__(
        self,
        logger: Optional[Any] = None
    ) -> None:
        super().__init__(
            "parser"
        )

        self.logger = logger
        self.processed: int = 0
        self.errors: int = 0

    # ==================================================
    # IDENTIDADE
    # ==================================================

    def module_name(self) -> str:
        return self.name

    # ==================================================
    # CONFIANÇA
    # ==================================================

    def confidence(
        self,
        input_data: Any
    ) -> float:
        if not input_data:
            return 0.0

        if self.errors > self.processed:
            return 0.2

        return 1.0

    # ==================================================
    # PROCESSAMENTO
    # ==================================================

    def process(
        self,
        context: PipelineContext
    ) -> PipelineContext:
        thought = context.thought

        if thought is None:
            context.add_error(
                "Parser recebeu Context sem Thought na Neural Lattice."
            )
            self.errors += 1
            return context

        try:
            thought.thinking()

            parsed = self.parse(
                thought.message
            )

            context.set(
                "parsed",
                parsed
            )

            thought.set_metadata(
                "parsed",
                parsed
            )

            thought.add_history(
                "parser_completed"
            )

            context.add_history(
                {
                    "event": "parser_completed",
                    "timestamp": datetime.now().isoformat()
                }
            )

            self.processed += 1

        except Exception as error:
            self.errors += 1

            error_data = {
                "type": "error",
                "content": None,
                "error": str(error)
            }

            context.add_error(
                error_data
            )

            context.set(
                "parsed",
                error_data
            )

            self.log_error(
                str(error)
            )

        return context

    # ==================================================
    # INTERPRETAÇÃO
    # ==================================================

    def parse(
        self,
        input_data: Any,
        context: Optional[PipelineContext] = None
    ) -> Dict[str, Any]:
        timestamp = datetime.now().isoformat()

        if not input_data:
            return {
                "type": "empty",
                "content": None,
                "intent": "empty",
                "metadata": {
                    "source": "unknown",
                    "timestamp": timestamp
                }
            }

        content = str(
            input_data
        ).strip()

        return {
            "type": self.detect_type(
                input_data
            ),
            "content": content,
            "intent": self.detect_intent(
                content
            ),
            "confidence": self.confidence(
                input_data
            ),
            "metadata": {
                "source": "user",
                "timestamp": timestamp,
                "length": len(content)
            }
        }

    # ==================================================
    # DETECÇÃO
    # ==================================================

    def detect_type(
        self,
        data: Any
    ) -> str:
        if isinstance(
            data,
            str
        ):
            return "text"

        return type(
            data
        ).__name__

    def detect_intent(
        self,
        text: str
    ) -> str:
        text = text.lower()

        if "teste" in text:
            return "system_test"

        if (
            "olá" in text
            or
            "ola" in text
            or
            "oi" in text
        ):
            return "greeting"

        if "jarvis" in text:
            return "jarvis_command"

        return "unknown"

    # ==================================================
    # SUPORTE
    # ==================================================

    def supports(
        self,
        input_type: str
    ) -> bool:
        return input_type in [
            "text",
            "command",
            "voice",
            "image",
            "file"
        ]

    # ==================================================
    # DIAGNÓSTICO
    # ==================================================

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "processed": self.processed,
            "errors": self.errors,
            "pipeline_status": self.status
        }

    def info(self) -> Dict[str, Any]:
        return self.diagnostics()

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