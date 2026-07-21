"""
=========================================
GENESIS CORE - COGNITIVE INTENTION

Arquivo: core/models/intention.py
Descrição: Modelo de intenção cognitiva extraída.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List, Optional

@dataclass
class Intention:
    """
    Representa uma intenção identificada pelo sistema cognitivo.
    Dicionário puro de dados sem lógica acoplada de negócios.
    """
    # Identificação
    id: str = field(default_factory=lambda: str(uuid4()))

    # Ação principal
    action: str = "unknown"
    target: Optional[str] = None

    # Origem e atribuição
    source: str = "user"
    agent: str = "jarvis"
    message: str = ""

    # Parâmetros e metadados
    parameters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    priority: int = 0

    # Controle temporal e estado
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "created"
    notes: List[str] = field(default_factory=list)

    # Métodos
    def add_parameter(self, key: str, value: Any) -> None:
        self.parameters[key] = value

    def get_parameter(self, key: str, default: Any = None) -> Any:
        return self.parameters.get(key, default)

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def set_status(self, status: str) -> None:
        self.status = status

    def is_valid(self) -> bool:
        """Verifica se a intenção possui uma ação definida."""
        return self.action != "unknown"

    def to_dict(self) -> Dict[str, Any]:
        """Serializa a intenção."""
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

    def __repr__(self) -> str:
        return f"Intention(action='{self.action}', target='{self.target}', confidence={self.confidence:.2f})"