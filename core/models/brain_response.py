"""
=========================================
GENESIS CORE - COGNITIVE BRAIN RESPONSE

Arquivo: core/models/brain_response.py
Descrição: Modelo de resposta cognitiva do Brain.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class BrainResponse:
    """
    Resposta produzida pelo Brain. Saída oficial da cognição antes da
    Transformação em linguagem natural pela Personality Engine.
    """
    # Identificação
    thought_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    # Resultado Cognitivo
    success: bool = True
    status: str = "completed"
    message: str = ""
    confidence: float = 0.0

    # Componentes Cognitivos
    intention: Any = None
    plan: Any = None
    decision: Any = None
    result: Any = None
    reflection: Any = None

    # Execução
    execution_time: float = 0.0

    # Informações Extras
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Métodos de Atribuição
    def set_message(self, message: str) -> None:
        self.message = message

    def set_result(self, result: Any) -> None:
        self.result = result

    def set_reflection(self, reflection: Any) -> None:
        self.reflection = reflection

    def set_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thought_id": self.thought_id,
            "success": self.success,
            "status": self.status,
            "message": self.message,
            "confidence": self.confidence,
            "execution_time": self.execution_time,
            "intention": (
                self.intention.to_dict()
                if hasattr(self.intention, "to_dict")
                else self.intention
            ),
            "plan": self.plan,
            "decision": self.decision,
            "result": self.result,
            "reflection": self.reflection,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_thought(cls, thought: Any) -> "BrainResponse":
        """
        Constrói uma BrainResponse a partir de um Thought finalizado.
        """
        response = cls()
        response.thought_id = thought.id
        response.status = thought.status
        response.confidence = thought.confidence
        response.intention = thought.intention
        response.plan = thought.plan
        response.decision = thought.decision
        response.result = thought.result
        response.execution_time = thought.execution_time
        response.metadata = dict(thought.metadata)
        response.success = (thought.status != "failed")

        if isinstance(thought.result, str):
            response.message = thought.result
        elif thought.result is not None:
            response.message = str(thought.result)
        else:
            response.message = ""

        return response

    def __repr__(self) -> str:
        return f"BrainResponse(status='{self.status}', success={self.success}, confidence={self.confidence:.2f})"