"""
=========================================
JARVIS CORE

Arquivo:
diagnostics.py

Descrição:
Sistema de diagnóstico interno.

Responsável por:
- Gerar relatórios do sistema
- Verificar componentes
- Exibir estado operacional

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime



from core.base.module import (
    Module,
    ModuleStatus
)





class Diagnostics(Module):


    """
    Sistema de diagnóstico
    do JARVIS.
    """



    def __init__(
        self,
        kernel=None,
        logger=None
    ):


        super().__init__(
            "core.diagnostics"
        )


        self.version = "2.0"


        self.kernel = kernel


        self.logger = logger



        self.history = []








    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log_success(
            "Diagnostics iniciado"
        )








    def shutdown(self):


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Diagnostics encerrado"
        )








    # ==========================================================
    # Relatório
    # ==========================================================


    def report(self):


        report = {


            "time":
            datetime.now().isoformat(),


            "kernel":
            None,


            "modules":
            {},


            "health":
            0,


            "memory":
            0,


            "state":
            "UNKNOWN",


            "tasks":
            0

        }



        if not self.kernel:


            return report





        # Kernel


        report["kernel"] = (

            self.kernel
            .get_status()
            .name

        )






        # Módulos


        for module in getattr(

            self.kernel,

            "modules",

            []

        ):


            report["modules"][

                module.name

            ] = module.status.name






        # Monitor


        monitor = getattr(

            self.kernel,

            "monitor",

            None

        )


        if monitor:


            report["health"] = (

                monitor.health

            )







        # Memória


        memory = getattr(

            self.kernel,

            "memory",

            None

        )


        if memory:


            report["memory"] = len(

                memory.memories

            )







        # Estado


        state = getattr(

            self.kernel,

            "state",

            None

        )


        if state:


            report["state"] = (

                state.get_state()
                .value

            )








        # Tasks


        tasks = getattr(

            self.kernel,

            "task_manager",

            None

        )


        if tasks:


            report["tasks"] = len(

                tasks.tasks

            )






        self.history.append(
            report
        )



        return report








    # ==========================================================
    # Histórico
    # ==========================================================


    def get_history(self):


        return self.history







    # ==========================================================
    # Exibição
    # ==========================================================


    def display(self):


        report = self.report()



        print()


        print("=" * 45)


        print(
            "          JARVIS DIAGNOSTICS"
        )


        print("=" * 45)



        print(
            f"Kernel: {report['kernel']}"
        )



        print()



        print(
            "Modules:"
        )


        for name, status in report["modules"].items():


            print(
                f" - {name}: {status}"
            )



        print()


        print(
            f"State: {report['state']}"
        )


        print(
            f"Health: {report['health']}%"
        )


        print(
            f"Memories: {report['memory']}"
        )


        print(
            f"Tasks: {report['tasks']}"
        )


        print("=" * 45)


        print()






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