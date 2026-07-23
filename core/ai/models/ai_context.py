"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_context.py

Descrição:
Contexto cognitivo temporário utilizado
pela camada de Inteligência Artificial.

Responsável por transportar informações
entre:

- AIManager
- Thought Engine
- Providers
- Personas
- Memória

Não representa memória permanente.

É um estado de trabalho da IA.

Arquitetura:

Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from __future__ import annotations


from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from typing import Any



@dataclass(slots=True)
class AIContext:
    """
    Contexto de execução de uma interação IA.
    """


    # =====================================================
    # IDENTIDADE
    # =====================================================


    id: str = field(
        default_factory=lambda: str(uuid4())
    )


    user: str = "Caio"


    persona: str = "jarvis"



    # =====================================================
    # CONVERSAÇÃO
    # =====================================================


    system_prompt: str | None = None


    conversation_id: str = field(
        default_factory=lambda: str(uuid4())
    )


    messages: list[dict[str, Any]] = field(
        default_factory=list
    )



    # =====================================================
    # MEMÓRIA
    # =====================================================


    memories: list[dict[str, Any]] = field(
        default_factory=list
    )


    knowledge: dict[str, Any] = field(
        default_factory=dict
    )



    # =====================================================
    # CONTROLE DE GERAÇÃO
    # =====================================================


    model: str | None = None


    temperature: float = 0.7


    max_tokens: int | None = None



    # =====================================================
    # ROTEAMENTO
    # =====================================================


    route: str = "chat"


    intent: str | None = None


    confidence: float = 0.0



    # =====================================================
    # METADADOS
    # =====================================================


    metadata: dict[str, Any] = field(
        default_factory=dict
    )


    created_at: datetime = field(
        default_factory=datetime.now
    )



    # =====================================================
    # MENSAGENS
    # =====================================================


    def add_message(
        self,
        role: str,
        content: str
    ) -> None:
        """
        Adiciona mensagem ao contexto.
        """


        self.messages.append({

            "role":
                role,

            "content":
                content,

            "timestamp":
                datetime.now().isoformat()

        })




    def add_memory(
        self,
        memory: dict[str, Any]
    ) -> None:
        """
        Adiciona memória temporária.
        """


        self.memories.append(
            memory
        )




    # =====================================================
    # LIMPEZA
    # =====================================================


    def clear_messages(self) -> None:


        self.messages.clear()




    def clear_memory(self) -> None:


        self.memories.clear()




    # =====================================================
    # EXPORTAÇÃO
    # =====================================================


    def to_dict(
        self
    ) -> dict[str, Any]:


        return {


            "id":
                self.id,


            "conversation_id":
                self.conversation_id,


            "user":
                self.user,


            "persona":
                self.persona,


            "route":
                self.route,


            "intent":
                self.intent,


            "confidence":
                self.confidence,


            "model":
                self.model,


            "temperature":
                self.temperature,


            "max_tokens":
                self.max_tokens,


            "messages":
                list(self.messages),


            "memories":
                list(self.memories),


            "knowledge":
                dict(self.knowledge),


            "metadata":
                dict(self.metadata),


            "created_at":
                self.created_at.isoformat()

        }



    # =====================================================
    # DEBUG
    # =====================================================


    def __repr__(self):

        return (

            "AIContext("

            f"persona='{self.persona}', "

            f"route='{self.route}', "

            f"messages={len(self.messages)}"

            ")"

        )