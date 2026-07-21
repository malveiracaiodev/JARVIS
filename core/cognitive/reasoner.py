"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/reasoner.py

Descrição:
Motor de raciocínio cognitivo do Genesis (Mark V - Evolution).

Responsável por analisar contexto,
avaliar alternativas (consultando a memória de longo prazo)
e produzir decisões dentro da malha neural.

Não executa ações.

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
from typing import Any, Dict, List, Optional, Union

from core.interfaces.reasoner_interface import (
    ReasonerInterface
)
from core.pipeline.pipeline_step import (
    PipelineStep
)
from core.pipeline.pipeline_context import (
    PipelineContext
)


class Reasoner(
    PipelineStep,
    ReasonerInterface
):
    """
    Núcleo de decisão cognitiva na Neural Lattice.

    Recebe planos.
    Consulta memória de longo prazo (Mark V).
    Avalia alternativas na malha.
    Produz decisão estruturada.

    Não executa.
    """

    def __init__(
        self,
        logger: Optional[Any] = None,
        memory: Optional[Any] = None
    ) -> None:
        super().__init__(
            "reasoner"
        )

        self.logger = logger
        self.memory = memory  # Injeção da memória de longo prazo
        self.decisions: int = 0
        self.errors: int = 0
        self.history: List[Dict[str, Any]] = []

    # ==================================================
    # IDENTIDADE
    # ==================================================

    def module_name(self) -> str:
        return self.name

    # ==================================================
    # STATUS
    # ==================================================

    def status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "decisions": self.decisions,
            "errors": self.errors,
            "memory_connected": self.memory is not None
        }

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
                "Reasoner recebeu Context sem Thought na Neural Lattice."
            )
            self.errors += 1
            return context

        try:
            thought.thinking()

            parsed = thought.get_metadata(
                "parsed",
                {}
            )

            plan = thought.plan

            if plan is None:
                plan = thought.get_metadata(
                    "plan",
                    {}
                )

            reasoning_context = {
                "input": parsed.get(
                    "content"
                ),
                "plan": plan
            }

            result = self.reason(
                reasoning_context
            )

            decision = result.get(
                "decision"
            )

            # ======================================
            # ATUALIZA CONTEXT
            # ======================================

            context.set(
                "reasoning",
                result
            )

            context.set(
                "decision",
                decision
            )

            # ======================================
            # ATUALIZA THOUGHT
            # ======================================

            thought.set_decision(
                decision
            )

            thought.set_metadata(
                "reasoning",
                result
            )

            thought.confidence = (
                result.get(
                    "confidence",
                    0
                )
            )

            thought.add_history(
                "reasoner_completed"
            )

            context.add_history(
                {
                    "event": "reasoner_completed",
                    "timestamp": datetime.now().isoformat()
                }
            )

        except Exception as error:
            self.errors += 1

            error_data = {
                "decision": None,
                "confidence": 0,
                "error": str(error)
            }

            context.add_error(
                error_data
            )

            context.set(
                "reasoning",
                error_data
            )

            self.log_error(
                str(error)
            )

        return context

    # ==================================================
    # RACIOCÍNIO
    # ==================================================

    def reason(
        self,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        plan = context.get(
            "plan"
        )

        if not plan:
            return {
                "decision": None,
                "confidence": 0,
                "analysis": "Nenhum plano disponível na Neural Lattice."
            }

        # ==========================================
        # INTEGRAÇÃO COM A MEMÓRIA DE LONGO PRAZO (MARK V)
        # ==========================================
        historical_insights = []
        if self.memory and hasattr(self.memory, "search"):
            try:
                query = plan.get("goal") or str(context.get("input", ""))
                historical_insights = self.memory.search(query=query, limit=3)
            except Exception as mem_error:
                self.log_error(f"Falha ao consultar memória no Reasoner: {mem_error}")

        options = self.generate_options(
            plan,
            insights=historical_insights
        )

        decision = self.decide(
            options
        )

        result = {
            "id": str(
                uuid.uuid4()
            ),
            "timestamp": datetime.now().isoformat(),
            "alternatives": options,
            "decision": decision,
            "confidence": self.confidence(
                decision
            ),
            "insights_used": len(historical_insights)
        }

        self.decisions += 1
        self.history.append(
            result
        )

        return result

    # ==================================================
    # OPÇÕES
    # ==================================================

    def generate_options(
        self,
        plan: Any,
        insights: Optional[List[Any]] = None
    ) -> List[Dict[str, Any]]:
        base_score = 1.0
        
        # Se houver insights de experiências passadas bem-sucedidas, podemos ponderar
        if insights:
            base_score = 1.2

        return [
            {
                "strategy": "execute_lattice_plan",
                "plan": plan,
                "score": base_score,
                "insights_applied": len(insights) if insights else 0
            }
        ]

    # ==================================================
    # AVALIAÇÃO
    # ==================================================

    def evaluate(
        self,
        option: Dict[str, Any],
        context: Optional[PipelineContext] = None
    ) -> Dict[str, Any]:
        if not option:
            return {
                "valid": False,
                "score": 0
            }

        return {
            "option": option,
            "score": option.get(
                "score",
                0
            ),
            "valid": True
        }

    # ==================================================
    # DECISÃO
    # ==================================================

    def decide(
        self,
        possibilities: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if not possibilities:
            return None

        return sorted(
            possibilities,
            key=lambda x: x.get(
                "score",
                0
            ),
            reverse=True
        )[0]

    # ==================================================
    # CONFIANÇA
    # ==================================================

    def confidence(
        self,
        decision: Optional[Dict[str, Any]]
    ) -> Union[int, float]:
        if not decision:
            return 0

        return decision.get(
            "score",
            0
        )

    # ==================================================
    # EXPLICAÇÃO
    # ==================================================

    def explain(
        self,
        decision: Optional[Dict[str, Any]]
    ) -> str:
        if not decision:
            return "Nenhuma decisão tomada na malha."

        return (
            "Decisão selecionada baseada "
            "na maior pontuação e histórico da Neural Lattice."
        )

    # ==================================================
    # COMPATIBILIDADE
    # ==================================================

    def evaluate_options(
        self,
        options: List[Dict[str, Any]],
        context: Optional[PipelineContext] = None
    ) -> List[Dict[str, Any]]:
        return [
            self.evaluate(
                option,
                context
            )
            for option in options
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
    # DIAGNÓSTICO
    # ==================================================

    def info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "decisions": self.decisions,
            "errors": self.errors,
            "memory_connected": self.memory is not None,
            "history": len(
                self.history
            )
        }