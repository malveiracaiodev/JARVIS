"""
=========================================
JARVIS CORE

Arquivo:
core/models/intention.py

Descrição:
Modelo de intenção cognitiva.

Representa a intenção extraída de uma
mensagem do usuário.

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


@dataclass
class Intention:
    """
    Representa uma intenção identificada
    pelo sistema cognitivo.

    Esta classe é apenas um modelo de dados.
    Não contém regras de negócio nem lógica
    de interpretação.
    """

    # Identificação
    id: str = field(default_factory=lambda: str(uuid4()))

    # Ação principal
    action: str = "unknown"

    # Alvo da ação
    target: str | None = None

    # Origem da intenção
    source: str = "user"

    # Agente responsável
    agent: str = "jarvis"

    # Texto original recebido
    message: str = ""

    # Parâmetros adicionais
    parameters: dict = field(default_factory=dict)

    # Metadados
    confidence: float = 0.0
    priority: int = 0

    # Controle temporal
    created_at: datetime = field(default_factory=datetime.now)

    # Estado
    status: str = "created"

    # Observações
    notes: list[str] = field(default_factory=list)

    # =====================================================

    def add_parameter(self, key: str, value):
        self.parameters[key] = value

    def get_parameter(self, key: str, default=None):
        return self.parameters.get(key, default)

    # =====================================================

    def add_note(self, note: str):
        self.notes.append(note)

    # =====================================================

    def set_status(self, status: str):
        self.status = status

    # =====================================================

    def is_valid(self) -> bool:
        """
        Verifica se a intenção possui
        uma ação definida.
        """
        return self.action != "unknown"

    # =====================================================

    def to_dict(self) -> dict:
        """
        Serializa a intenção.
        """
        return {
            "id": self.id,
            "action": self.action,
            "target": self.target,
            "source": self.source,
            "agent": self.agent,
            "message": self.message,
            "parameters": self.parameters,
            "confidence": self.confidence,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "notes": self.notes,
        }

    # =====================================================

    def __repr__(self):

        return (
            f"Intention("
            f"action='{self.action}', "
            f"target='{self.target}', "
            f"confidence={self.confidence:.2f})"
        )