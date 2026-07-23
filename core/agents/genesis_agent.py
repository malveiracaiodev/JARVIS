"""
=========================================
GENESIS CORE

Arquivo:
core/agents/genesis_agent.py

Descrição:

Agente cognitivo base do Genesis Core.

Responsabilidades:

- Identidade cognitiva
- Persona
- Perfil
- Construção de contexto
- Delegação ao Mind
- Registro das interações

O processamento cognitivo pertence ao Mind.

Arquitetura:

Agent
    │
GenesisAgent
    │
Mind
    │
Thought Engine
    │
AIManager

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from core.agents.agent import Agent


class GenesisAgent(Agent):
    """
    Agente cognitivo padrão do Genesis.

    Todos os agentes especializados devem
    herdar desta classe.
    """

    def __init__(
        self,
        name: str,
        persona=None,
        description: str = "",
        capabilities=None,
        profile: Optional[Dict[str, Any]] = None
    ):

        super().__init__(
            name=name,
            description=description,
            capabilities=capabilities or []
        )

        # =====================================
        # PERSONA
        # =====================================

        self.persona = persona

        # =====================================
        # PERFIL COGNITIVO
        # =====================================

        self.profile = profile or {

            "type": "general",

            "reasoning": "adaptive",

            "version": "5.0"

        }

        # =====================================
        # ESTADO
        # =====================================

        self.last_thought = None

    # ==================================================
    # PERSONA
    # ==================================================

    def connect_persona(self, persona):

        self.persona = persona

    # ==================================================
    # CONTEXTO
    # ==================================================

    def build_context(
        self,
        message: Any
    ) -> Dict[str, Any]:

        context = {

            "agent": self.name,

            "profile": self.profile,

            "message": message

        }

        if self.persona:

            context["persona"] = (

                self.persona.build_context(
                    message
                )

            )

        return context

    # ==================================================
    # PENSAMENTO
    # ==================================================

    def think(
        self,
        message: Any
    ):

        if not self.active:

            return {

                "status": "inactive",

                "agent": self.name

            }

        context = self.build_context(message)

        if self.mind:

            result = self.mind.process(

                message=message,

                agent=self,

                context=context

            )

        else:

            result = {

                "status": "mind_offline",

                "context": context

            }

        self.last_thought = result

        self.remember({

            "input": message,

            "output": result

        })

        if (

            self.memory_manager

            and

            hasattr(
                self.memory_manager,
                "store"
            )

        ):

            self.memory_manager.store(

                {

                    "agent": self.name,

                    "input": message,

                    "output": result

                },

                memory_type="short_term"

            )

        return result

    # ==================================================
    # FERRAMENTAS
    # ==================================================

    def use_tool(
        self,
        tool: str,
        data: Any = None
    ):

        return self.execute(
            tool,
            data
        )

    # ==================================================
    # STATUS
    # ==================================================

    def info(self):

        data = super().info()

        data.update({

            "persona":

                getattr(
                    self.persona,
                    "name",
                    None
                ),

            "profile":
                self.profile,

            "last_thought":
                self.last_thought is not None

        })

        return data