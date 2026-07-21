"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/thought_engine.py

Descrição:
Motor central do ciclo cognitivo Mark V - Evolution (Neural Lattice).

Responsável por:

- Criar Thoughts integrados à Lattice
- Controlar ciclo cognitivo
- Executar Pipeline na malha neural
- Finalizar estados
- Registrar histórico
- Emitir eventos para o ecossistema
- Medir desempenho

Não raciocina.
Não decide.
Não executa.

Apenas controla o ciclo.

Arquitetura:
Genesis Core

Mark:
V - Evolution / Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from core.models.thought import Thought


class ThoughtEngine:
    """
    Controlador do ciclo cognitivo na Neural Lattice (Mark V).

    Fluxo:

        Entrada
            |
            v
        Thought
            |
            v
        Pipeline (Neural Lattice)
            |
            v
        Reflection
            |
            v
        Memória (Longo Prazo)
    """

    def __init__(
        self,
        logger: Optional[Any] = None,
        event_bus: Optional[Any] = None,
        pipeline: Optional[Any] = None
    ) -> None:
        self.logger = logger
        self.event_bus = event_bus
        self.pipeline = pipeline

        self.version: str = (
            "Genesis Core Mark V - Evolution Thought Engine"
        )

        self.active_thoughts: Dict[str, Thought] = {}
        self.history: List[Thought] = []

        # MÉTRICAS
        self.created: int = 0
        self.completed: int = 0
        self.failed_count: int = 0

        self.last_execution: Optional[float] = None

    # ==================================================
    # LOG
    # ==================================================

    def _log(
        self,
        level: str,
        message: str
    ) -> None:
        if self.logger:
            method = getattr(
                self.logger,
                level,
                None
            )

            if callable(method):
                method(
                    message
                )
                return

        print(
            "[THOUGHT_ENGINE]",
            message
        )

    # ==================================================
    # EVENTOS
    # ==================================================

    def _emit(
        self,
        event: str,
        thought: Thought
    ) -> None:
        if not self.event_bus:
            return

        try:
            self.event_bus.emit(
                event,
                thought.to_dict()
            )

        except Exception as error:
            self._log(
                "error",
                str(error)
            )

    # ==================================================
    # PIPELINE
    # ==================================================

    def connect_pipeline(
        self,
        pipeline: Any
    ) -> None:
        self.pipeline = pipeline

        self._log(
            "info",
            "Pipeline Cognitiva conectada à Neural Lattice (Mark V)."
        )

    # ==================================================
    # CRIAÇÃO
    # ==================================================

    def create(
        self,
        message: str,
        agent: str = "jarvis",
        source: str = "user"
    ) -> Thought:
        thought = Thought(
            message=message,
            agent=agent,
            source=source
        )

        self.active_thoughts[
            thought.id
        ] = thought

        self.created += 1

        self._emit(
            "THOUGHT_CREATED",
            thought
        )

        return thought

    # ==================================================
    # INÍCIO
    # ==================================================

    def start(
        self,
        thought: Thought
    ) -> Thought:
        thought.processing()

        started = datetime.now()

        thought.set_metadata(
            "started_at",
            started.isoformat()
        )

        self._emit(
            "THOUGHT_STARTED",
            thought
        )

        return thought

    # ==================================================
    # CICLO PRINCIPAL
    # ==================================================

    def think(
        self,
        message: str,
        agent: str = "jarvis",
        source: str = "user"
    ) -> Thought:
        thought = self.create(
            message,
            agent,
            source
        )

        execution_start = datetime.now()

        try:
            self.start(
                thought
            )

            if self.pipeline is None:
                return self.fail(
                    thought,
                    "Pipeline Cognitiva não conectada à Neural Lattice."
                )

            context = self.pipeline.process(
                thought
            )

            result = (
                context.summary()
                if hasattr(
                    context,
                    "summary"
                )
                else context
            )

            return self.complete(
                thought,
                result
            )

        except Exception as error:
            return self.fail(
                thought,
                error
            )

        finally:
            self.last_execution = (
                datetime.now()
                -
                execution_start
            ).total_seconds()

    # ==================================================
    # FINALIZAÇÃO
    # ==================================================

    def complete(
        self,
        thought: Thought,
        result: Optional[Any] = None
    ) -> Thought:
        if result is not None:
            thought.set_result(
                result
            )

        if not thought.is_finished():
            thought.completed()

        self.completed += 1

        self._archive(
            thought
        )

        self._emit(
            "THOUGHT_COMPLETED",
            thought
        )

        self._log(
            "info",
            f"Thought concluído na Neural Lattice (Mark V) {thought.id[:8]}"
        )

        return thought

    def fail(
        self,
        thought: Thought,
        error: Any
    ) -> Thought:
        thought.set_metadata(
            "error",
            str(error)
        )

        if not thought.is_finished():
            thought.failed()

        self.failed_count += 1

        self._archive(
            thought
        )

        self._emit(
            "THOUGHT_FAILED",
            thought
        )

        self._log(
            "error",
            f"Thought falhou na Neural Lattice (Mark V) {thought.id[:8]}"
        )

        return thought

    # ==================================================
    # ARQUIVO
    # ==================================================

    def _archive(
        self,
        thought: Thought
    ) -> None:
        if thought not in self.history:
            self.active_thoughts.pop(
                thought.id,
                None
            )

            self.history.append(
                thought
            )

    # ==================================================
    # CONSULTA
    # ==================================================

    def get_history(self) -> List[Thought]:
        return self.history

    def get_active(self) -> List[Thought]:
        return list(
            self.active_thoughts.values()
        )

    def get(
        self,
        thought_id: str
    ) -> Optional[Thought]:
        active = self.active_thoughts.get(
            thought_id
        )

        if active:
            return active

        for thought in self.history:
            if thought.id == thought_id:
                return thought

        return None

    # ==================================================
    # MÉTRICAS
    # ==================================================

    def metrics(self) -> Dict[str, Any]:
        total = self.created
        success_rate: float = 0.0

        if total:
            success_rate = (
                self.completed /
                total
            )

        return {
            "created": self.created,
            "completed": self.completed,
            "failed": self.failed_count,
            "success_rate": success_rate,
            "active": len(
                self.active_thoughts
            ),
            "history": len(
                self.history
            ),
            "last_execution": self.last_execution
        }

    # ==================================================
    # LIMPEZA
    # ==================================================

    def clear(self) -> bool:
        self.active_thoughts.clear()
        self.history.clear()

        self.created = 0
        self.completed = 0
        self.failed_count = 0

        return True

    # ==================================================
    # STATUS
    # ==================================================

    def status(self) -> Dict[str, Any]:
        return {
            "name": "ThoughtEngine",
            "version": self.version,
            "pipeline": self.pipeline is not None,
            "metrics": self.metrics()
        }