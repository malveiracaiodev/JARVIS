"""
=========================================
JARVIS CORE

Arquivo:
command_interface.py

Descrição:
Interface de linha de comando do JARVIS.

Responsável pela comunicação entre
o usuário e o Kernel.

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


class CommandInterface(Module):
    """
    Interface de linha de comando.

    Recebe comandos do usuário e os
    encaminha ao Kernel.
    """

    def __init__(self, kernel):

        super().__init__(
            "Command Interface"
        )

        self.kernel = kernel

        self.logger = kernel.logger

        self.running = False

        self.commands = {

            "ajuda": self.help,
            "help": self.help,

            "quem é você": self.identity,
            "quem e voce": self.identity,
            "identidade": self.identity,

            "status": self.status,
            "diagnostico": self.status,
            "diagnóstico": self.status,

            "estado": self.state,

            "tarefas": self.tasks,

            "plugins": self.plugins,

            "memorias": self.memories,
            "memórias": self.memories,

            "limpar": self.clear,
            "clear": self.clear,

            "sair": self.exit,
            "exit": self.exit

        }

    # ======================================================
    # Interface
    # ======================================================

    def initialize(self):

        self.set_status(
            ModuleStatus.ONLINE
        )

    def shutdown(self):

        self.running = False

        self.set_status(
            ModuleStatus.OFFLINE
        )

    # ======================================================
    # Loop Principal
    # ======================================================

    def run(self):

        self.initialize()

        self.running = True

        print()
        print("========================================")
        print("JARVIS Command Interface")
        print("Digite 'ajuda' para listar comandos.")
        print("========================================")

        while self.running:

            try:

                command = input("\nSenhor > ")

                command = command.lower().strip()

                if not command:
                    continue

                action = self.commands.get(command)

                if action:

                    print()

                    action()

                else:

                    print()

                    print(
                        "Comando desconhecido."
                    )

            except KeyboardInterrupt:

                print()

                self.exit()

            except Exception as error:

                self.logger.error(
                    str(error)
                )

    # ======================================================
    # Comandos
    # ======================================================

    def help(self):

        print("Comandos disponíveis:\n")

        for command in sorted(self.commands.keys()):

            print(f" - {command}")

    def identity(self):

        print(
            self.kernel.identity.introduce()
        )

    def status(self):

        self.kernel.diagnostics.display()

    def state(self):

        print(
            self.kernel.state.get_state().value
        )

    def tasks(self):

        tasks = self.kernel.task_manager.list_tasks()

        if not tasks:

            print(
                "Nenhuma tarefa registrada."
            )

            return

        for task in tasks:

            print(task)

    def plugins(self):

        plugins = self.kernel.plugin_manager.list_plugins()

        if not plugins:

            print(
                "Nenhum plugin carregado."
            )

            return

        for plugin in plugins:

            print(plugin)

    def memories(self):

        memories = self.kernel.memory.memories

        print()

        print(
            f"Memórias: {len(memories)}"
        )

        print()

        for memory in memories:

            print(memory)

    def clear(self):

        print("\n" * 40)

    def exit(self):

        print()

        print(
            "Encerrando interface..."
        )

        self.shutdown()

        self.kernel.shutdown()