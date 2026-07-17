"""
=========================================
JARVIS CORE

Arquivo:
core/services/task_manager.py

Descrição:
Gerenciador central de tarefas do Genesis Core.

Responsável por:
- Criar tarefas
- Controlar ciclo de execução
- Gerenciar estados
- Integrar com Runtime
- Monitorar resultados

Arquitetura:
Genesis Core

Mark:
III - Matrix (Task Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import copy
import threading
import uuid


from datetime import datetime
from enum import Enum



from core.base.module import (
    Module,
    ModuleStatus
)





class TaskStatus(Enum):

    CREATED = "CREATED"

    QUEUED = "QUEUED"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"

    DISABLED = "DISABLED"






class Task:
    """
    Unidade de execução do Genesis Core.
    """



    def __init__(
        self,
        name,
        function,
        priority=1
    ):

        self.id = str(
            uuid.uuid4()
        )


        self.name = name

        self.function = function

        self.priority = priority


        self.status = (
            TaskStatus.CREATED
        )


        self.created = datetime.now()

        self.started = None

        self.last_run = None

        self.finished = None


        self.executions = 0


        self.duration = 0


        self.last_error = None





    def execute(self):


        start = datetime.now()


        try:


            self.status = (
                TaskStatus.RUNNING
            )


            self.started = start


            self.last_error = None



            result = (
                self.function()
            )



            finish = datetime.now()



            self.status = (
                TaskStatus.COMPLETED
            )


            self.executions += 1


            self.last_run = finish


            self.finished = finish



            self.duration = (
                finish - start
            ).total_seconds()



            return result



        except Exception as error:


            self.status = (
                TaskStatus.FAILED
            )


            self.last_error = (
                str(error)
            )


            raise







class TaskManager(Module):

    """
    Controlador de tarefas do Genesis Core.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None,
        runtime=None
    ):


        super().__init__(
            "core.task_manager"
        )


        self.version = "3.0"


        self.logger = logger

        self.event_bus = event_bus

        self.runtime = runtime


        self.tasks = {}


        self._lock = threading.RLock()





    # ======================================================
    # CICLO DE VIDA
    # ======================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log_success(
            "Task Manager Mark III ONLINE."
        )





    def shutdown(self):


        with self._lock:


            self.tasks.clear()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Task Manager encerrado."
        )





    # ======================================================
    # REGISTRO
    # ======================================================


    def register(
        self,
        task
    ):


        with self._lock:


            self.tasks[
                task.name
            ] = task



        self.emit(
            "TASK_CREATED",
            {
                "id":
                    task.id,

                "name":
                    task.name
            }
        )


        self.log_info(
            f"Tarefa registrada: {task.name}"
        )





    def remove(
        self,
        name
    ):


        with self._lock:


            if name in self.tasks:


                task = self.tasks.pop(
                    name
                )


                self.emit(
                    "TASK_REMOVED",
                    {
                        "id":
                            task.id,

                        "name":
                            name
                    }
                )





    # ======================================================
    # EXECUÇÃO
    # ======================================================


    def execute(
        self,
        name
    ):


        with self._lock:


            task = self.tasks.get(
                name
            )



        if not task:


            self.log_error(
                f"Tarefa inexistente: {name}"
            )


            return False




        if task.status == TaskStatus.DISABLED:


            return False





        task.status = (
            TaskStatus.QUEUED
        )



        self.emit(
            "TASK_QUEUED",
            {
                "id":
                    task.id,

                "name":
                    task.name
            }
        )





        if self.runtime:


            accepted = (
                self.runtime.submit(
                    task
                )
            )


            if not accepted:


                task.status = (
                    TaskStatus.FAILED
                )


            return accepted





        thread = threading.Thread(
            target=self._run_task_safely,
            args=(task,),
            daemon=True
        )


        thread.start()


        return True






    def _run_task_safely(
        self,
        task
    ):


        try:


            task.execute()



            self.emit(
                "TASK_COMPLETED",
                {
                    "id":
                        task.id,

                    "name":
                        task.name
                }
            )



        except Exception as error:


            self.emit(
                "TASK_FAILED",
                {
                    "id":
                        task.id,

                    "name":
                        task.name,

                    "error":
                        str(error)
                }
            )





    # ======================================================
    # CONSULTA
    # ======================================================


    def get(
        self,
        name
    ):


        with self._lock:


            return self.tasks.get(
                name
            )





    def list_tasks(self):


        with self._lock:


            return list(
                self.tasks.keys()
            )





    def report(self):


        with self._lock:


            return copy.deepcopy(

                {

                    name: {

                        "id":
                            task.id,

                        "status":
                            task.status.value,

                        "executions":
                            task.executions,

                        "duration":
                            task.duration,

                        "last_error":
                            task.last_error,

                        "last_run":
                            (
                                task.last_run.isoformat()
                                if task.last_run
                                else None
                            )

                    }

                    for name, task
                    in self.tasks.items()

                }

            )





    # ======================================================
    # EVENTOS
    # ======================================================


    def emit(
        self,
        event,
        data=None
    ):


        if self.event_bus:


            try:


                self.event_bus.emit(
                    event,
                    data
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