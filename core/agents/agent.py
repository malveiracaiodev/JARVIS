"""
=========================================
JARVIS CORE

Arquivo:
agent.py

Descrição:
Classe base para agentes inteligentes.

Arquitetura:
Genesis Core

Mark:
II - Evolution
=========================================
"""


from datetime import datetime



class Agent:



    def __init__(

            self,

            name,

            personality="default"

    ):


        self.name = name


        self.personality = personality


        self.status = "created"


        self.memory = []


        self.mind = None


        self.created = datetime.now()



    # ---------------------------------
    # Conectar mente
    # ---------------------------------

    def connect_mind(

            self,

            mind

    ):


        self.mind = mind



        print(

            f"[AGENT] {self.name} conectado ao Mind"

        )



    # ---------------------------------
    # Inicializar
    # ---------------------------------

    def start(self):


        self.status = "online"



        print(

            f"[AGENT] {self.name} ONLINE"

        )



    # ---------------------------------
    # Receber mensagem
    # ---------------------------------

    def receive(

            self,

            message

    ):


        self.memory.append({

            "message":

            message,


            "time":

            str(datetime.now())

        })


        if self.mind:


            return self.mind.think(

                message

            )



        return self.think(

            message

        )



    # ---------------------------------
    # Pensamento padrão
    # ---------------------------------

    def think(

            self,

            message

    ):


        return (

            f"{self.name}: "

            "Ainda estou aprendendo."

        )



    # ---------------------------------
    # Fala
    # ---------------------------------

    def speak(

            self,

            text

    ):


        print(

            f"{self.name}: {text}"

        )



    # ---------------------------------
    # Encerrar
    # ---------------------------------

    def stop(self):


        self.status = "offline"


        print(

            f"[AGENT] {self.name} OFFLINE"

        )