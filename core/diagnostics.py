"""
=========================================
JARVIS CORE

Arquivo:
diagnostics.py

Descrição:
Sistema de diagnóstico interno.

Responsável por reunir informações
sobre o estado do JARVIS.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


from core.base.module import (
    Module,
    ModuleStatus
)





class Diagnostics(Module):
    """
    Sistema de diagnóstico do JARVIS.
    """



    def __init__(
        self,
        kernel,
        logger
    ):

        super().__init__(
            "Diagnostics Core"
        )


        self.kernel = kernel

        self.logger = logger





    # ==========================================================
    # Inicialização
    # ==========================================================


    def initialize(self):

        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.logger.success(
            "Diagnostics Core iniciado"
        )





    # ==========================================================
    # Encerramento
    # ==========================================================


    def shutdown(self):

        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.logger.info(
            "Diagnostics Core encerrado"
        )





    # ==========================================================
    # Diagnóstico
    # ==========================================================


    def report(self):
        """
        Gera relatório do sistema.
        """


        modules = {}



        for module in self.kernel.modules:

            modules[module.name] = (
                module.status.name
            )



        report = {

            "kernel":
                self.kernel.get_status()
                .name,


            "modules":
                modules,


            "health":
                self.kernel.monitor.health,


            "memory":
                len(
                    self.kernel.memory.memories
                )

        }



        return report





    def display(self):
        """
        Exibe relatório no terminal.
        """


        report = self.report()



        print()

        print(
            "=" * 40
        )

        print(
            "       JARVIS DIAGNOSTICS"
        )

        print(
            "=" * 40
        )



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
            f"Health: {report['health']}%"
        )



        print(
            f"Memories: {report['memory']}"
        )



        print(
            "=" * 40
        )

        print()