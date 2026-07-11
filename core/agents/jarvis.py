"""
=========================================
JARVIS CORE

Arquivo:
jarvis.py

Descrição:
Agente principal do sistema.

Responsável por:
- Assistência técnica
- Operações
- Controle do sistema

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.agents.agent import Agent



class JarvisAgent(Agent):


    """
    Agente operacional do JARVIS.
    """



    def __init__(self):


        super().__init__(

            name="JARVIS",

            personality="technical"

        )



    # ---------------------------------
    # Processamento de comandos
    # ---------------------------------

    def think(

            self,

            message

    ):


        message = message.lower()



        if "status" in message:


            return (

                "Todos os sistemas estão "
                "aguardando diagnóstico."

            )



        if "ajuda" in message:


            return (

                "Estou pronto para auxiliar "
                "nas operações."

            )



        return (

            "Comando recebido. "
            "Processando informação."

        )