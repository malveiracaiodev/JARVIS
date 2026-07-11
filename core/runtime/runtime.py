"""
=========================================
JARVIS CORE

Arquivo:
runtime.py

Descrição:
Motor de execução do sistema.

Responsável por:
- Ciclo principal
- Gerenciamento de tarefas
- Execução de processos
- Comunicação entre componentes

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


import time
import threading
from datetime import datetime



class Runtime:


    """
    Sistema responsável pela execução
    contínua do JARVIS.
    """



    def __init__(self):


        self.running = False


        self.tasks = []


        self.thread = None


        self.start_time = None



    # ---------------------------------
    # Iniciar Runtime
    # ---------------------------------

    def start(self):


        if self.running:

            return



        self.running = True


        self.start_time = datetime.now()



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )


        self.thread.start()



        print(
            "[RUNTIME] Sistema iniciado"
        )



    # ---------------------------------
    # Loop principal
    # ---------------------------------

    def loop(self):


        while self.running:



            self.process_tasks()



            time.sleep(
                0.1
            )



    # ---------------------------------
    # Adicionar tarefa
    # ---------------------------------

    def add_task(
            self,
            task
    ):


        self.tasks.append(
            task
        )


        print(
            "[RUNTIME] "
            "Nova tarefa adicionada"
        )



    # ---------------------------------
    # Executar tarefas
    # ---------------------------------

    def process_tasks(self):


        if len(self.tasks) == 0:

            return



        task = self.tasks.pop(
            0
        )



        try:


            task()



        except Exception as error:


            print(
                "[RUNTIME] ERRO:",
                error
            )



    # ---------------------------------
    # Parar sistema
    # ---------------------------------

    def stop(self):


        self.running = False



        print(
            "[RUNTIME] Sistema parado"
        )



    # ---------------------------------
    # Status
    # ---------------------------------

    def status(self):


        return {


            "running":

            self.running,


            "tasks":

            len(
                self.tasks
            ),


            "started":

            self.start_time

        }