"""
=========================================
JARVIS CORE

Arquivo:
rafiki.py

Descrição:
Agente conselheiro do sistema.

Responsável por:
- Reflexão
- Conselhos
- Análise de decisões
- Apoio ao usuário

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from core.agents.agent import Agent



class RafikiAgent(Agent):


    """
    Agente de aconselhamento
    e reflexão.
    """



    def __init__(self):


        super().__init__(

            name="RAFIKI",

            personality="advisor"

        )



    # ---------------------------------
    # Processamento de pensamento
    # ---------------------------------

    def think(

            self,

            message

    ):


        message = message.lower()



        if "decisão" in message or "decidir" in message:


            return (

                "Antes de decidir, "
                "vamos analisar as consequências, "
                "os riscos e os seus objetivos."

            )



        if "problema" in message:


            return (

                "Vamos entender o problema "
                "antes de buscar uma solução."

            )



        if "conselho" in message:


            return (

                "Um bom conselho começa "
                "com uma visão clara da situação."

            )



        return (

            "Estou ouvindo. "
            "Vamos analisar isso juntos."

        )