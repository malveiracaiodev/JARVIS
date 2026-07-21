"""
=========================================
GENESIS CORE - THOUGHT CORE ENGINE

Arquivo: core/models/thought.py
Descrição: Modelo central de pensamento cognitivo.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List, Optional
from core.models.intention import Intention

@dataclass
class Thought:
    """
    Unidade central de processamento cognitivo (Pipeline de Raciocínio).
    """
    # Identidade
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    # Origem
    message: str = ""
    agent: str = "jarvis"
    source: str = "user"

    # Contexto de Entrada
    context: Dict[str, Any] = field(default_factory=dict)

    # Estado Cognitivo
    intention: Optional[Intention] = None
    plan: Optional[Any] = None
    decision: Optional[Any] = None
    action: Optional[Any] = None
    result: Optional[Any] = None

    # Estado Operacional
    status: str = "created"
    confidence: float = 0.0
    priority: int = 0

    # Memória Temporária
    metadata: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    history: List[Dict[str, str]] = field(default_factory=list)

    # Métricas
    execution_time: float = 0.0

    # Métodos de Controle Temporal e de Status
    def touch(self) -> None:
        self.updated_at = datetime.now()

    def set_status(self, status: str) -> None:
        self.status = status
        self.touch()

    def processing(self) -> None:
        if self.started_at is None:
            self.started_at = datetime.now()
        self.set_status("processing")

    def thinking(self) -> None:
        self.set_status("thinking")

    def executing(self) -> None:
        self.set_status("executing")

    def reflecting(self) -> None:
        self.set_status("reflecting")

    # Mutadores Cognitivos
    def set_intention(self, intention: Intention) -> None:
        self.intention = intention
        self.touch()

    def set_plan(self, plan: Any) -> None:
        self.plan = plan
        self.touch()

    def set_decision(self, decision: Any) -> None:
        self.decision = decision
        self.touch()

    def set_action(self, action: Any) -> None:
        self.action = action
        self.touch()

    def set_result(self, result: Any) -> None:
        self.result = result
        self.touch()

    # Rastreabilidade e Histórico
    def add_history(self, event: str) -> None:
        self.history.append({
            "event": event,
            "timestamp": datetime.now().isoformat()
        })
        self.touch()

    # Metadados e Anotações
    def set_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value
        self.touch()

    def add_metadata(self, key: str, value: Any) -> None:
        self.set_metadata(key, value)

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            self.touch()

    def add_note(self, note: str) -> None:
        self.notes.append(note)
        self.touch()

    # Finalização de Ciclos
    def completed(self) -> None:
        self.finish()

    def finish(self) -> None:
        self.finished_at = datetime.now()
        self.status = "completed"
        self._calculate_execution_time()
        self.touch()

    def failed(self) -> None:
        self.finished_at = datetime.now()
        self.status = "failed"
        self._calculate_execution_time()
        self.touch()

    def _calculate_execution_time(self) -> None:
        if self.started_at and self.finished_at:
            self.execution_time = (self.finished_at - self.started_at).total_seconds()

    def is_finished(self) -> bool:
        return self.finished_at is not None

    # Serialização Estrita
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "message": self.message,
            "agent": self.agent,
            "source": self.source,
            "status": self.status,
            "confidence": self.confidence,
            "priority": self.priority,
            "execution_time": self.execution_time,
            "context": self.context,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "updated_at": self.updated_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "intention": self.intention.to_dict() if self.intention else None,
            "plan": self.plan,
            "decision": self.decision,
            "action": self.action,
            "result": self.result,
            "metadata": self.metadata,
            "history": self.history,
            "tags": self.tags,
            "notes": self.notes
        }

    def __repr__(self) -> str:
        return f"Thought(id={self.id[:8]}, status='{self.status}', confidence={self.confidence:.2f})"