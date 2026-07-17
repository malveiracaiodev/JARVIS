"""
=========================================
JARVIS CORE

Arquivo:
core/services/runtime.py

Descrição:
Gerenciador central de execução do Genesis Core.

Responsável por:
- Controlar workers
- Administrar execução assíncrona
- Encaminhar tarefas
- Monitorar ciclo operacional

Arquitetura:
Genesis Core

Mark:
III - Matrix (Execution Layer)

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
    Núcleo responsável pela execução
    de tarefas do Genesis Core.
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


        self.version = "3.0"


        self.logger = logger

        self.event_bus = event_bus

        self.queue = task_queue

        self.worker = worker



        self.running = False


        self._lock = threading.RLock()



    # ======================================================
    # CICLO DE VIDA
    # ======================================================


    def initialize(self):

        with self._lock:


            if self.running:

                self.log_info(
                    "Runtime já está ativo."
                )

                return



            self.set_status(
                ModuleStatus.INITIALIZING
            )



            try:


                if self.worker:


                    self.worker.start()



                self.running = True



                self.set_status(
                    ModuleStatus.ONLINE
                )



                self.emit(
                    "RUNTIME_STARTED"
                )



                self.log_success(
                    "Runtime Mark III ONLINE."
                )



            except Exception as error:


                self.running = False


                self.set_error(
                    str(error)
                )


                self.log_error(
                    f"Falha iniciando Runtime: {error}"
                )





    def shutdown(self):

        with self._lock:


            if not self.running:

                return



            self.running = False



            try:


                if self.worker:

                    self.worker.stop()



            except Exception as error:


                self.log_error(
                    f"Erro parando worker: {error}"
                )



            self.emit(
                "RUNTIME_STOPPED"
            )



            self.set_status(
                ModuleStatus.OFFLINE
            )


            self.log_info(
                "Runtime encerrado."
            )



    # ======================================================
    # EXECUÇÃO DE TAREFAS
    # ======================================================


    def submit(
        self,
        task
    ):


        with self._lock:


            if not self.running:


                self.log_error(
                    "Runtime offline. "
                    "Tarefa rejeitada."
                )


                return False



            if not self.queue:


                self.log_error(
                    "Fila de tarefas inexistente."
                )


                return False



            try:


                self.queue.push(
                    task
                )



                task_name = getattr(
                    task,
                    "name",
                    str(task)
                )



                self.log_info(
                    f"Tarefa enviada: {task_name}"
                )



                self.emit(
                    "TASK_SUBMITTED",
                    task
                )



                return True



            except Exception as error:


                self.log_error(
                    f"Erro enviando tarefa: {error}"
                )


                return False





    # ======================================================
    # ESTADO
    # ======================================================


    def is_running(
        self
    ):


        with self._lock:

            return self.running




    def status(
        self
    ):


        return {

            "running":
                self.running,

            "worker":
                self.worker is not None,

            "queue":
                self.queue is not None

        }





    # ======================================================
    # EVENTOS
    # ======================================================


    def emit(
        self,
        event,
        *args
    ):


        if self.event_bus:


            try:

                self.event_bus.emit(
                    event,
                    *args
                )


            except Exception:

                pass





    # ======================================================
    # LOG
    # ======================================================


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