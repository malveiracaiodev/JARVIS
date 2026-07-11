"""
=========================================
JARVIS CORE

Arquivo:
runtime.py

Descrição:
Gerenciador de execução do JARVIS.

Responsável por:
- Controlar workers
- Administrar fila
- Executar tarefas em background

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


import threading


from core.base.module import (
    Module,
    ModuleStatus
)






class Runtime(Module):


    """
    Núcleo de execução do JARVIS.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None,
        task_queue=None,
        worker=None
    ):


        super().__init__(
            "core.runtime"
        )


        self.version = "2.0"


        self.logger = logger


        self.event_bus = event_bus


        self.queue = task_queue


        self.worker = worker



        self.running = False


        self.thread = None







    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )



        self.running = True



        if self.worker:


            self.worker.start()





        self.set_status(
            ModuleStatus.ONLINE
        )



        self.log_success(
            "Runtime iniciado"
        )







    def shutdown(self):


        self.running = False



        if self.worker:


            self.worker.stop()





        self.set_status(
            ModuleStatus.OFFLINE
        )



        self.log_info(
            "Runtime encerrado"
        )








    # ==========================================================
    # Tarefas
    # ==========================================================


    def submit(
        self,
        task
    ):


        if not self.queue:


            self.log_error(
                "Fila de tarefas inexistente"
            )


            return False




        self.queue.push(
            task
        )



        self.log_info(
            f"Tarefa enviada: {task.name}"
        )



        return True







    # ==========================================================
    # Estado
    # ==========================================================


    def is_running(self):


        return self.running







    # ==========================================================
    # Logs
    # ==========================================================


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