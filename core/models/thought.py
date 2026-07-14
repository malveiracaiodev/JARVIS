"""
=========================================
JARVIS CORE

Arquivo:
core/mind/models/thought.py

Descrição:
Modelo de pensamento cognitivo.

Representa um ciclo completo de raciocínio
do JARVIS, desde a entrada até a conclusão.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from core.models.intention import Intention


@dataclass
class Thought:
    """
    Representa um pensamento do JARVIS.

    Um Thought acompanha todo o fluxo cognitivo,
    desde a interpretação da mensagem até a
    execução da resposta.
    """

    # =====================================================
    # Identificação
    # =====================================================

    id: str = field(default_factory=lambda: str(uuid4()))

    created_at: datetime = field(default_factory=datetime.now)

    updated_at: datetime = field(default_factory=datetime.now)

    # =====================================================
    # Origem
    # =====================================================

    message: str = ""

    agent: str = "jarvis"

    source: str = "user"

    # =====================================================
    # Cognição
    # =====================================================

    intention: Intention | None = None

    plan = None

    decision = None

    result = None

    # =====================================================
    # Estado
    # =====================================================

    status: str = "created"

    confidence: float = 0.0

    priority: int = 0

    # =====================================================
    # Dados auxiliares
    # =====================================================

    metadata: dict = field(default_factory=dict)

    notes: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)

    # =====================================================
    # Controle
    # =====================================================

    finished_at: datetime | None = None

    execution_time: float = 0.0

    # =====================================================
    # Métodos
    # =====================================================

    def touch(self):
        """
        Atualiza o timestamp de modificação.
        """
        self.updated_at = datetime.now()

    # -----------------------------------------------------

    def set_status(self, status: str):
        self.status = status
        self.touch()

    # -----------------------------------------------------

    def set_intention(self, intention: Intention):
        self.intention = intention
        self.touch()

    # -----------------------------------------------------

    def set_plan(self, plan):
        self.plan = plan
        self.touch()

    # -----------------------------------------------------

    def set_decision(self, decision):
        self.decision = decision
        self.touch()

    # -----------------------------------------------------

    def set_result(self, result):
        self.result = result
        self.touch()

    # -----------------------------------------------------

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)

    # -----------------------------------------------------

    def add_note(self, note: str):
        self.notes.append(note)

    # -----------------------------------------------------

    def set_metadata(self, key: str, value):
        self.metadata[key] = value

    # -----------------------------------------------------

    def get_metadata(self, key: str, default=None):
        return self.metadata.get(key, default)

    # -----------------------------------------------------

    def finish(self):
        """
        Finaliza o pensamento.
        """
        self.finished_at = datetime.now()
        self.status = "completed"
        self.touch()

        delta = self.finished_at - self.created_at
        self.execution_time = delta.total_seconds()

    # -----------------------------------------------------

    def failed(self):
        """
        Marca o pensamento como falho.
        """
        self.status = "failed"
        self.touch()

    # -----------------------------------------------------

    def is_finished(self):

        return self.finished_at is not None

    # -----------------------------------------------------

    def to_dict(self):

        return {

            "id": self.id,

            "message": self.message,

            "agent": self.agent,

            "source": self.source,

            "status": self.status,

            "confidence": self.confidence,

            "priority": self.priority,

            "execution_time": self.execution_time,

            "created_at": self.created_at.isoformat(),

            "updated_at": self.updated_at.isoformat(),

            "finished_at": (
                self.finished_at.isoformat()
                if self.finished_at
                else None
            ),

            "tags": self.tags,

            "metadata": self.metadata,

            "notes": self.notes,

            "intention": (
                self.intention.to_dict()
                if self.intention
                else None
            )

        }

    # -----------------------------------------------------

    def __repr__(self):

        return (
            f"Thought("
            f"id={self.id[:8]}, "
            f"status='{self.status}', "
            f"confidence={self.confidence:.2f})"
        )