"""
=========================================
JARVIS CORE

Arquivo:
core/models/thought.py

Descrição:
Modelo central de pensamento cognitivo.

Representa um ciclo completo de raciocínio
do JARVIS, desde a entrada até a conclusão.

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
from uuid import uuid4


from core.models.intention import Intention



@dataclass
class Thought:
    """
    Unidade central de processamento cognitivo.

    O Thought acompanha toda a jornada:

    Entrada
       |
       v
    Interpretação
       |
       v
    Planejamento
       |
       v
    Decisão
       |
       v
    Execução
       |
       v
    Resultado
    """



    # =====================================================
    # IDENTIDADE
    # =====================================================


    id: str = field(
        default_factory=lambda: str(uuid4())
    )


    created_at: datetime = field(
        default_factory=datetime.now
    )


    updated_at: datetime = field(
        default_factory=datetime.now
    )



    # =====================================================
    # ORIGEM
    # =====================================================


    message: str = ""


    agent: str = "jarvis"


    source: str = "user"



    # =====================================================
    # ESTADO COGNITIVO
    # =====================================================


    intention: Intention | None = None


    plan: object = None


    decision: object = None


    result: object = None



    # =====================================================
    # ESTADO
    # =====================================================


    status: str = "created"


    confidence: float = 0.0


    priority: int = 0



    # =====================================================
    # MEMÓRIA TEMPORÁRIA
    # =====================================================


    metadata: dict = field(
        default_factory=dict
    )


    notes: list[str] = field(
        default_factory=list
    )


    tags: list[str] = field(
        default_factory=list
    )



    # =====================================================
    # FINALIZAÇÃO
    # =====================================================


    finished_at: datetime | None = None


    execution_time: float = 0.0



    # =====================================================
    # CONTROLE TEMPORAL
    # =====================================================


    def touch(
        self
    ):

        self.updated_at = datetime.now()



    # =====================================================
    # STATUS
    # =====================================================


    def set_status(
        self,
        status: str
    ):

        self.status = status

        self.touch()



    def processing(
        self
    ):

        self.set_status(
            "processing"
        )



    def completed(
        self
    ):

        self.finish()



    # =====================================================
    # COGNIÇÃO
    # =====================================================


    def set_intention(
        self,
        intention: Intention
    ):

        self.intention = intention

        self.touch()



    def set_plan(
        self,
        plan
    ):

        self.plan = plan

        self.touch()



    def set_decision(
        self,
        decision
    ):

        self.decision = decision

        self.touch()



    def set_result(
        self,
        result
    ):

        self.result = result

        self.touch()



    # =====================================================
    # METADADOS
    # =====================================================


    def set_metadata(
        self,
        key: str,
        value
    ):

        self.metadata[key] = value

        self.touch()



    def add_metadata(
        self,
        key: str,
        value
    ):
        """
        Alias para compatibilidade
        com módulos cognitivos.
        """

        self.set_metadata(
            key,
            value
        )



    def get_metadata(
        self,
        key,
        default=None
    ):

        return self.metadata.get(
            key,
            default
        )



    # =====================================================
    # ANOTAÇÕES
    # =====================================================


    def add_tag(
        self,
        tag: str
    ):

        if tag not in self.tags:

            self.tags.append(
                tag
            )

            self.touch()



    def add_note(
        self,
        note: str
    ):

        self.notes.append(
            note
        )

        self.touch()



    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def finish(
        self
    ):

        self.finished_at = datetime.now()

        self.status = "completed"

        self.touch()


        delta = (
            self.finished_at
            -
            self.created_at
        )


        self.execution_time = (
            delta.total_seconds()
        )



    def failed(
        self
    ):

        self.status = "failed"

        self.touch()



    def is_finished(
        self
    ):

        return (
            self.finished_at is not None
        )



    # =====================================================
    # SERIALIZAÇÃO
    # =====================================================


    def to_dict(
        self
    ):

        return {


            "id":
                self.id,


            "message":
                self.message,


            "agent":
                self.agent,


            "source":
                self.source,


            "status":
                self.status,


            "confidence":
                self.confidence,


            "priority":
                self.priority,


            "execution_time":
                self.execution_time,


            "created_at":
                self.created_at.isoformat(),


            "updated_at":
                self.updated_at.isoformat(),


            "finished_at":
                (
                    self.finished_at.isoformat()
                    if self.finished_at
                    else None
                ),


            "intention":
                (
                    self.intention.to_dict()
                    if self.intention
                    else None
                ),


            "plan":
                self.plan,


            "decision":
                self.decision,


            "result":
                self.result,


            "metadata":
                self.metadata,


            "tags":
                self.tags,


            "notes":
                self.notes

        }



    # =====================================================
    # REPRESENTAÇÃO
    # =====================================================


    def __repr__(
        self
    ):

        return (

            f"Thought("
            f"id={self.id[:8]}, "
            f"status='{self.status}', "
            f"confidence={self.confidence:.2f}"
            f")"

        )