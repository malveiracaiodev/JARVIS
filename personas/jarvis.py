"""
=========================================
JARVIS CORE

Arquivo:
core/agents/jarvis.py

Descrição:
Agente principal de suporte técnico
e operações do Genesis Core.

Responsável por:
- Operações técnicas
- Diagnóstico do sistema
- Coordenação de tarefas
- Comunicação operacional

Arquitetura:
Genesis Core

Mark:
III - Matrix (Agent Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


from core.agents.agent import Agent





class JarvisAgent(Agent):
    """
    Agente operacional técnico central.
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
                "JARVIS"
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
                "jarvis"
            )


        return {


            "name":
                "JARVIS",


            "personality":
                {

                    "tone":
                        "educado",

                    "style":
                        "assistente técnico"

                }

        }





    # ==================================================
    # PROCESSAMENTO
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



        if "status" in cmd:


            return (

                "Executando diagnóstico operacional. "
                "Os módulos centrais estão aguardando "
                "telemetria e novas tarefas."

            )



        if "ajuda" in cmd:


            return (

                "Estou disponível para coordenar "
                "diagnósticos, gerenciar tarefas, "
                "executar ferramentas autorizadas "
                "e auxiliar nas operações do Genesis Core."

            )



        if "quem é você" in cmd or "quem e voce" in cmd:


            return (

                "Eu sou JARVIS, "
                "agente operacional do Genesis Core."

            )



        return (

            "Comando recebido. "
            "Analisando intenção e preparando execução."

        )





    # ==================================================
    # CAPACIDADES
    # ==================================================


    def capabilities(self):


        return [

            "system_monitoring",

            "task_management",

            "technical_assistance",

            "tool_execution",

            "diagnostics"

        ]