"""
=========================================
JARVIS CORE

Arquivo:
core/agents/rafiki.py

Descrição:
Agente de aconselhamento, reflexão
estratégica e apoio analítico.

Responsável por:
- Reflexão de decisões
- Análise de problemas
- Apoio estratégico
- Orientação conversacional

Arquitetura:
Genesis Core

Mark:
III - Matrix (Agent Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


from core.agents.agent import Agent





class RafikiAgent(Agent):
    """
    Agente analítico focado em reflexão
    e aconselhamento estratégico.
    """



    def __init__(
        self,
        identity_manager=None
    ):


        self.identity_manager = (
            identity_manager
        )


        identity = self.load_identity()



        super().__init__(

            name=identity.get(
                "name",
                "RAFIKI"
            ),

            personality=identity.get(
                "personality",
                {}

            )

        )





    # ==================================================
    # IDENTIDADE
    # ==================================================


    def load_identity(self):


        if self.identity_manager:


            return self.identity_manager.get_agent_identity(
                "rafiki"
            )



        return {


            "name":
                "RAFIKI",


            "personality":
                {

                    "tone":
                        "acolhedor",

                    "style":
                        "conselheiro"

                }

        }





    # ==================================================
    # PROCESSAMENTO COGNITIVO
    # ==================================================


    def think(
        self,
        message
    ):


        cmd = (

            str(message)
            .lower()
            .strip()

        )



        if (
            "decisão" in cmd
            or
            "decisao" in cmd
            or
            "decidir" in cmd
        ):


            return (

                "Uma decisão estratégica precisa "
                "considerar objetivos, limitações, "
                "riscos e consequências futuras. "
                "Vamos organizar as variáveis antes "
                "de escolher um caminho."

            )





        if "problema" in cmd:


            return (

                "Um problema visível geralmente "
                "é consequência de uma causa mais "
                "profunda. Vamos identificar onde "
                "o fluxo começou a se desviar."

            )





        if "conselho" in cmd:


            return (

                "Para encontrar clareza, precisamos "
                "separar urgência de importância. "
                "Qual resultado você deseja construir "
                "a longo prazo?"

            )





        if (
            "quem é você" in cmd
            or
            "quem e voce" in cmd
        ):


            return (

                "Eu sou Rafiki, agente de reflexão "
                "e análise estratégica do Genesis Core."

            )





        return (

            "Reflexão registrada. "
            "Analisando alternativas considerando "
            "consistência, impacto e objetivos futuros."

        )





    # ==================================================
    # CAPACIDADES
    # ==================================================


    def capabilities(self):


        return [

            "strategic_reflection",

            "decision_support",

            "problem_analysis",

            "long_term_planning"

        ]