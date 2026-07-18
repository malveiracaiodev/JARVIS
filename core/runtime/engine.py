"""
=========================================
JARVIS CORE

Arquivo:
engine.py

Descrição:
Motor e orquestrador principal de processamento
assíncrono paralelo e ciclo de vida do Kernel.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import os
import threading

from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)


from core.runtime.queue import (
    TaskQueue
)


from core.runtime.worker import (
    Worker
)



class Runtime(Module):

    """
    Gerenciador unificado de execução em background.

    Responsável por:

    • Gerenciar Workers
    • Receber tarefas assíncronas
    • Distribuir tarefas na fila
    • Coletar métricas
    • Controlar ciclo de vida

    Não conhece:

    - Brain
    - Pipeline
    - Agents
    - IA

    Apenas fornece infraestrutura.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None,
        worker_pool_size=None,
    ):


        super().__init__(
            "core.runtime"
        )



        self.version = (
            "Genesis Core Mark III"
        )



        self.logger = logger

        self.event_bus = event_bus



        # =====================================================
        # WORKERS
        # =====================================================


        if worker_pool_size is None:


            cpu = (
                os.cpu_count()
                or 2
            )


            self.worker_count = max(
                2,
                cpu
            )


        else:


            self.worker_count = max(
                1,
                worker_pool_size
            )



        # =====================================================
        # FILA
        # =====================================================


        self.queue = TaskQueue()


        self.workers = []


        self.start_time = None



        self._lock = threading.RLock()



        # =====================================================
        # MÉTRICAS
        # =====================================================
        #
        # IMPORTANTE:
        #
        # Não substitui as métricas
        # existentes do Module.
        #
        # Apenas adiciona métricas
        # específicas do Runtime.
        #
        # =====================================================


        self.metrics.update({

            "queued_tasks": 0,

            "processed_tasks": 0,

            "failed_tasks": 0,

            "running_tasks": 0,

            "queue_peak": 0,

        })



    # =====================================================
    # CICLO DE VIDA
    # =====================================================



    def initialize(
        self
    ):


        with self._lock:



            if (
                self.get_status()
                ==
                ModuleStatus.ONLINE
            ):

                self.info(
                    "Runtime já está ONLINE."
                )

                return True




            self.set_status(
                ModuleStatus.INITIALIZING
            )



            self.start_time = datetime.now()



            self.workers = [

                Worker(
                    queue=self.queue,
                    logger=self.logger,
                    event_bus=self.event_bus,
                    name=f"Worker-{index + 1}"
                )

                for index

                in range(
                    self.worker_count
                )

            ]



            for worker in self.workers:

                worker.start()



            self.set_status(
                ModuleStatus.ONLINE
            )



            self.success(
                f"Motor Runtime ONLINE com {self.worker_count} Workers."
            )



            self._emit(
                "runtime.started"
            )



        return True





    def start(
        self
    ):

        return self.initialize()





    def stop(
        self
    ):


        with self._lock:



            if (
                self.get_status()
                ==
                ModuleStatus.OFFLINE
            ):

                return True




            self.set_status(
                ModuleStatus.WARNING
            )



            for worker in self.workers:

                worker.stop()



            for worker in self.workers:

                worker.join()



            self.workers.clear()



            self.set_status(
                ModuleStatus.OFFLINE
            )



            self.info(
                "Runtime finalizado."
            )



            self._emit(
                "runtime.stopped"
            )



        return True





    def shutdown(
        self
    ):

        return self.stop()



    # =====================================================
    # FILA
    # =====================================================



    def add_task(
        self,
        task
    ):

        """
        Adiciona uma tarefa
        para execução assíncrona.
        """



        self.queue.push(
            task
        )



        self.metrics[
            "queued_tasks"
        ] += 1



        queue_size = (
            self.queue.size()
        )



        if (
            queue_size
            >
            self.metrics["queue_peak"]
        ):

            self.metrics[
                "queue_peak"
            ] = queue_size




        task_name = getattr(

            task,

            "name",

            task.__class__.__name__

        )



        self.info(
            f"Tarefa adicionada: {task_name}"
        )



        self._emit(
            "runtime.task.queued",
            task=task_name
        )



    # =====================================================
    # STATUS
    # =====================================================



    def status(
        self
    ):



        uptime = 0



        if self.start_time:


            uptime = (

                datetime.now()

                -

                self.start_time

            ).total_seconds()




        return {


            "name":

                self.name,


            "version":

                self.version,


            "status":

                self.get_status()
                .value,


            "workers":

                self.worker_count,


            "active_workers":

                len(
                    self.workers
                ),


            "pending_tasks":

                self.queue.size(),


            "uptime":

                round(
                    uptime,
                    2
                ),


            "metrics":

                self.metrics.copy()

        }




    # =====================================================
    # EVENTOS
    # =====================================================



    def _emit(
        self,
        event,
        **payload
    ):


        if not self.event_bus:

            return



        try:


            self.event_bus.emit(
                event,
                payload
            )


        except Exception as error:


            self.info(
                f"Falha evento {event}: {error}"
            )



    # =====================================================
    # LOGGING
    # =====================================================



    def info(
        self,
        message
    ):


        if self.logger:

            self.logger.info(
                message
            )



    def success(
        self,
        message
    ):


        if self.logger:

            self.logger.success(
                message
            )



    def warning(
        self,
        message
    ):


        if self.logger:

            self.logger.warning(
                message
            )



    def error(
        self,
        message
    ):


        if self.logger:

            self.logger.error(
                message
            )