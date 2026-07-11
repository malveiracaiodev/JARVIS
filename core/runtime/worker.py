"""
=========================================
JARVIS CORE

Arquivo:
worker.py

Descrição:
Executor de tarefas do Runtime.

Responsável por:
- Consumir fila
- Executar Tasks
- Registrar resultados

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


import threading
import time




class Worker:


    """
    Trabalhador do Runtime.
    """



    def __init__(
        self,
        queue,
        logger=None,
        event_bus=None
    ):


        self.queue = queue


        self.logger = logger


        self.event_bus = event_bus



        self.running = False


        self.thread = None







    # ======================================================
    # Inicialização
    # ======================================================


    def start(self):


        if self.running:


            return



        self.running = True



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )



        self.thread.start()



        self.log_success(
            "Worker iniciado"
        )







    # ======================================================
    # Loop principal
    # ======================================================


    def loop(self):


        while self.running:



            task = self.queue.next()



            if task:


                self.execute(
                    task
                )


            else:


                time.sleep(
                    0.5
                )








    # ======================================================
    # Execução
    # ======================================================


    def execute(
        self,
        task
    ):


        try:


            self.log_info(
                f"Executando tarefa: {task.name}"
            )



            self.emit(
                "TASK_STARTED",
                task.name
            )



            result = task.execute()



            self.queue.complete(

                task,

                result

            )



            self.emit(
                "TASK_COMPLETED",
                task.name
            )



            self.log_success(

                f"Tarefa concluída: {task.name}"

            )






        except Exception as error:



            self.queue.fail(

                task,

                error

            )



            self.emit(

                "TASK_FAILED",

                {

                    "task":
                    task.name,

                    "error":
                    str(error)

                }

            )



            self.log_error(

                f"Falha na tarefa {task.name}: {error}"

            )









    # ======================================================
    # Encerramento
    # ======================================================


    def stop(self):


        self.running = False



        if self.thread:


            self.thread.join(
                timeout=2
            )



        self.log_info(
            "Worker encerrado"
        )







    # ======================================================
    # Auxiliares
    # ======================================================


    def emit(
        self,
        event,
        data
    ):


        if self.event_bus:


            self.event_bus.emit(
                event,
                data
            )







    def log_info(
        self,
        message
    ):


        if self.logger:


            self.logger.info(
                message
            )







    def log_success(
        self,
        message
    ):


        if self.logger:


            self.logger.success(
                message
            )







    def log_error(
        self,
        message
    ):


        if self.logger:


            self.logger.error(
                message
            )