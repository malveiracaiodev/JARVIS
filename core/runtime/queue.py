"""
=========================================
JARVIS CORE

Arquivo:
queue.py

Descrição:
Fila central de execução do JARVIS.

Responsável por:
- Armazenar tarefas
- Controlar prioridade
- Entregar tarefas aos workers
- Registrar histórico

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


import threading


from datetime import datetime





class TaskQueue:


    """
    Fila inteligente de tarefas.
    """



    def __init__(self):


        self.tasks = []


        self.history = []


        self.lock = threading.Lock()







    # ======================================================
    # Entrada
    # ======================================================


    def push(
        self,
        task
    ):


        with self.lock:


            task.status = (

                task.status.__class__
                .QUEUED

            )


            self.tasks.append(
                task
            )



            self.sort()



    # ======================================================
    # Prioridade
    # ======================================================


    def sort(self):


        self.tasks.sort(

            key=lambda task:

            task.priority,

            reverse=True

        )







    # ======================================================
    # Próxima tarefa
    # ======================================================


    def next(self):


        with self.lock:


            if not self.tasks:


                return None




            task = self.tasks.pop(
                0
            )



            return task







    # ======================================================
    # Finalização
    # ======================================================


    def complete(
        self,
        task,
        result=None
    ):


        task.result = result


        task.finished = datetime.now()


        self.history.append(
            task
        )







    def fail(
        self,
        task,
        error
    ):


        task.last_error = str(
            error
        )


        task.finished = datetime.now()



        self.history.append(
            task
        )







    # ======================================================
    # Consultas
    # ======================================================


    def pending(self):


        with self.lock:


            return list(
                self.tasks
            )







    def logs(self):


        return self.history







    def size(self):


        return len(
            self.tasks
        )