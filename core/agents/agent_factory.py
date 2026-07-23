"""
=========================================
GENESIS CORE

Arquivo:
core/agents/agent_factory.py

Descrição:

Fábrica responsável pela criação dinâmica
de agentes cognitivos Genesis.

Responsável por:

- Criar GenesisAgent
- Integrar Personas
- Resolver identidades
- Configurar capacidades
- Preparar agentes para Mind/Memory/Tools

Arquitetura:

identity.json
      |
      v
PersonaFactory
      |
      v
AgentFactory
      |
      v
GenesisAgent


Mark:
V - Evolution
=========================================
"""


from typing import Optional, Dict, Any


from core.agents.genesis_agent import GenesisAgent

from personas.persona_factory import PersonaFactory




class AgentFactory:
    """
    Criador oficial de agentes Genesis.

    A Factory não conhece agentes específicos.

    Ela cria agentes através da identidade
    configurada das Personas.
    """


    def __init__(
        self,
        persona_factory=None
    ):


        self.persona_factory = (

            persona_factory

            or

            PersonaFactory()

        )



    # =========================================
    # CRIAÇÃO
    # =========================================


    def create(
        self,
        name: str
    ) -> GenesisAgent:
        """
        Cria um agente Genesis baseado
        em uma persona existente.
        """


        name = name.lower()



        persona = self.persona_factory.create(
            name
        )


        if not persona:

            raise RuntimeError(
                f"Não foi possível criar persona: {name}"
            )



        agent = GenesisAgent(

            name=persona.name,

            persona=persona,

            description=getattr(
                persona,
                "description",
                ""
            ),

            capabilities=getattr(
                persona,
                "capabilities",
                []
            ),

            profile={

                "type":
                    "genesis_agent",

                "persona":
                    name,

                "version":
                    "5.0"

            }

        )



        return agent



    # =========================================
    # LISTAGEM
    # =========================================


    def available(
        self
    ):

        return (
            self.persona_factory.available()
        )



    # =========================================
    # CRIAÇÃO EM LOTE
    # =========================================


    def create_all(
        self
    ) -> Dict[str, GenesisAgent]:
        """
        Cria todos os agentes disponíveis.
        """


        agents = {}



        for name in self.available():


            try:

                agents[name] = self.create(
                    name
                )


            except Exception as error:


                print(
                    f"[AGENT FACTORY] Erro criando {name}: {error}"
                )



        return agents



    # =========================================
    # IDENTIDADE
    # =========================================


    def identity(
        self
    ):

        return (
            self.persona_factory
            .get_system_identity()
        )