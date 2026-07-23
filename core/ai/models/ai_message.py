"""
=========================================
GENESIS CORE

Arquivo:
core/ai/models/ai_message.py

Descrição:
Modelo oficial de mensagens da camada IA.

Responsável por padronizar a comunicação
entre o Genesis Core e qualquer Provider
de Inteligência Artificial.

Compatível com:

- Mock Provider
- Ollama
- OpenAI
- Gemini
- Claude
- DeepSeek
- Mistral
- Providers futuros

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
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class AIMessage:
    """
    Representa uma mensagem individual
    de uma conversa.

    Pode representar:

    - system
    - user
    - assistant
    - tool
    """

    # =====================================================
    # IDENTIDADE
    # =====================================================

    message_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    timestamp: datetime = field(
        default_factory=datetime.now
    )

    # =====================================================
    # CONTEÚDO
    # =====================================================

    role: str = "user"

    content: str = ""

    name: str | None = None

    # =====================================================
    # TOOL CALLING
    # =====================================================

    tool_name: str | None = None

    tool_call_id: str | None = None

    # =====================================================
    # MULTIMODAL
    # =====================================================

    attachments: list[Any] = field(
        default_factory=list
    )

    # =====================================================
    # CONTEXTO
    # =====================================================

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # ROLES
    # =====================================================

    VALID_ROLES = {

        "system",

        "user",

        "assistant",

        "tool"

    }

    # =====================================================
    # VALIDAÇÃO
    # =====================================================

    def __post_init__(self) -> None:
        """
        Valida a criação da mensagem.
        """

        self.role = self.role.lower().strip()

        if self.role not in self.VALID_ROLES:

            raise ValueError(

                f"Role inválido: {self.role}"

            )

        if not isinstance(
            self.content,
            str
        ):

            raise TypeError(

                "content deve ser string."

            )

    # =====================================================
    # UTILIDADES
    # =====================================================

    def is_user(self) -> bool:

        return self.role == "user"

    def is_system(self) -> bool:

        return self.role == "system"

    def is_assistant(self) -> bool:

        return self.role == "assistant"

    def is_tool(self) -> bool:

        return self.role == "tool"

    def has_attachments(self) -> bool:

        return bool(self.attachments)

    def add_attachment(
        self,
        attachment: Any
    ) -> None:

        self.attachments.append(
            attachment
        )

    def set_metadata(
        self,
        key: str,
        value: Any
    ) -> None:

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None
    ) -> Any:

        return self.metadata.get(
            key,
            default
        )

    # =====================================================
    # CONVERSÃO
    # =====================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Converte para formato aceito
        pelos Providers.
        """

        data = {

            "role": self.role,

            "content": self.content

        }

        if self.name:

            data["name"] = self.name

        return data

    def to_full_dict(self) -> dict[str, Any]:
        """
        Serialização completa.
        """

        return {

            "message_id": self.message_id,

            "timestamp": self.timestamp.isoformat(),

            "role": self.role,

            "content": self.content,

            "name": self.name,

            "tool_name": self.tool_name,

            "tool_call_id": self.tool_call_id,

            "attachments": self.attachments,

            "metadata": self.metadata

        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any]
    ) -> "AIMessage":
        """
        Constrói uma mensagem a partir
        de um dicionário.
        """

        return cls(

            role=data.get(
                "role",
                "user"
            ),

            content=data.get(
                "content",
                ""
            ),

            name=data.get(
                "name"
            ),

            tool_name=data.get(
                "tool_name"
            ),

            tool_call_id=data.get(
                "tool_call_id"
            ),

            attachments=data.get(
                "attachments",
                []
            ),

            metadata=data.get(
                "metadata",
                {}
            )

        )

    # =====================================================
    # DEBUG
    # =====================================================

    def __repr__(self) -> str:

        preview = self.content.replace(
            "\n",
            " "
        )

        if len(preview) > 40:

            preview = preview[:40] + "..."

        return (

            "AIMessage("

            f"id='{self.message_id[:8]}', "

            f"role='{self.role}', "

            f"content='{preview}'"

            ")"

        )