"""
=========================================
GENESIS CORE

Arquivo:
core/models/brain_response.py

Descrição:
Modelo de resposta cognitiva do Brain.

Representa a saída oficial do Brain após
o processamento completo de um Thought.

Responsabilidade:
- Transportar a resposta cognitiva
- Servir de ponte entre Brain e Personality
- Não executa lógica

Arquitetura:
Genesis Core

Mark:
IV - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class BrainResponse:
    """
    Resposta produzida pelo Brain.

    É a saída oficial da cognição antes da
    Personality Engine transformar em linguagem
    natural.
    """

    # ==================================================
    # Identificação
    # ==================================================

    thought_id: str = ""

    created_at: datetime = field(default_factory=datetime.now)

    # ==================================================
    # Resultado Cognitivo
    # ==================================================

    success: bool = True

    status: str = "completed"

    message: str = ""

    confidence: float = 0.0

    # ==================================================
    # Componentes Cognitivos
    # ==================================================

    intention: Any = None

    plan: Any = None

    decision: Any = None

    result: Any = None

    reflection: Any = None

    # ==================================================
    # Execução
    # ==================================================

    execution_time: float = 0.0

    # ==================================================
    # Informações Extras
    # ==================================================

    metadata: dict = field(default_factory=dict)

    # ==================================================
    # Métodos
    # ==================================================

    def set_message(self, message: str):

        self.message = message

    # --------------------------------------------------

    def set_result(self, result: Any):

        self.result = result

    # --------------------------------------------------

    def set_reflection(self, reflection: Any):

        self.reflection = reflection

    # --------------------------------------------------

    def set_metadata(self, key: str, value: Any):

        self.metadata[key] = value

    # --------------------------------------------------

    def get_metadata(self, key: str, default=None):

        return self.metadata.get(key, default)

    # --------------------------------------------------

    def to_dict(self):

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

    # --------------------------------------------------

    @classmethod
    def from_thought(cls, thought):
        """
        Constrói uma BrainResponse a partir
        de um Thought finalizado.
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

        response.success = (
            thought.status != "failed"
        )

        if isinstance(thought.result, str):

            response.message = thought.result

        elif thought.result is not None:

            response.message = str(thought.result)

        else:

            response.message = ""

        return response

    # --------------------------------------------------

    def __repr__(self):

        return (

            f"BrainResponse("
            f"status='{self.status}', "
            f"success={self.success}, "
            f"confidence={self.confidence:.2f}"
            f")"

        )