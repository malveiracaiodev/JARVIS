"""
=========================================
JARVIS CORE

Arquivo:
command_interface.py

Descrição:
Interface de console (CLI) assíncrona e não-bloqueante para o JARVIS.
Gerencia interações via terminal rodando em thread isolada.

Arquitetura:
Genesis Core

Mark:
III - Intelligence (Patch 3.3 - Non-Blocking CLI)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
import unicodedata
from core.base.module import Module, ModuleStatus


class CommandInterface(Module):
    """
    Interface de linha de comando thread-safe e assíncrona.
    Conecta a entrada de console diretamente às rotinas centrais do Kernel.
    """

    def __init__(self, kernel):
        super().__init__("core.command_interface")
        self.version = "3.0"
        self.kernel = kernel
        self.logger = getattr(kernel, "logger", None)
        self.running = False
        self._cli_thread = None
        self._lock = threading.RLock()

        # Mapeamento unificado de aliases normatizados
        self.commands = {
            "ajuda": self.help,
            "help": self.help,
            "quem e voce": self.identity,
            "identidade": self.identity,
            "status": self.status,
            "diagnostico": self.status,
            "estado": self.state,
            "tarefas": self.tasks,
            "plugins": self.plugins,
            "memorias": self.memories,
            "limpar": self.clear,
            "clear": self.clear,
            "sair": self.exit,
            "exit": self.exit
        }

    def _normalize(self, text):
        """Remove acentos e padroniza a string em caixa baixa."""
        if not text:
            return ""
        text = unicodedata.normalize("NFD", text)
        text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
        return text.lower().strip()

    # ======================================================
    # Ciclo de Vida do Módulo
    # ======================================================

    def initialize(self):
        with self._lock:
            if self.is_online():
                return
            self.set_status(ModuleStatus.INITIALIZING)
            self.set_status(ModuleStatus.ONLINE)
            self.success("Interface de comandos inicializada.")

    def shutdown(self):
        with self._lock:
            if self.is_offline():
                return
            self.running = False
            self.set_status(ModuleStatus.OFFLINE)
            self.info("Interface de comandos desativada de forma graciosa.")

    # ======================================================
    # Thread Loop (Não bloqueia o Kernel)
    # ======================================================

    def start_interface(self):
        """Dispara a captura de linha de comando em uma thread dedicada."""
        with self._lock:
            self.initialize()
            if self.running:
                return
            self.running = True
            self._cli_thread = threading.Thread(target=self._run_loop, name="JARVIS_CLI_Thread", daemon=True)
            self._cli_thread.start()

    def _run_loop(self):
        print("\n" + "=" * 40)
        print(" JARVIS - GENESIS CORE INTERFACE (Mark III)")
        print(" Terminal operacional ativo. Digite 'ajuda'.")
        print("=" * 40)

        while self.running:
            try:
                # O input() bloqueia apenas ESTA thread, deixando o core livre
                raw_input = input("\nSenhor > ")
                command = self._normalize(raw_input)

                if not command:
                    continue

                with self._lock:
                    action = self.commands.get(command)

                if action:
                    print()
                    action()
                else:
                    print(f"\n[!] Comando '{raw_input}' não catalogado no Core. Digite 'ajuda'.")

            except (KeyboardInterrupt, EOFError):
                print()
                self.exit()
                break
            except Exception as error:
                self.error(f"Erro na execução da linha de comando: {str(error)}")

    # ======================================================
    # Métodos Executores de Comandos
    # ======================================================

    def help(self):
        print("Comandos mapeados na árvore operacional:\n")
        with self._lock:
            cmds = sorted(list(self.commands.keys()))
        for command in cmds:
            print(f"  - {command}")

    def identity(self):
        if hasattr(self.kernel, "identity") and hasattr(self.kernel.identity, "introduce"):
            print(self.kernel.identity.introduce())
        else:
            print("JARVIS - Sistema de inteligência autônomo (Módulo de identidade ausente).")

    def status(self):
        if hasattr(self.kernel, "diagnostics") and hasattr(self.kernel.diagnostics, "display"):
            self.kernel.diagnostics.display()
        else:
            print("[Telemetria] Módulo de diagnóstico não acoplado ao Kernel.")

    def state(self):
        if hasattr(self.kernel, "state") and hasattr(self.kernel.state, "get_state"):
            state = self.kernel.state.get_state()
            print(f"Estado Atual do Core: {state.value if hasattr(state, 'value') else state}")
        else:
            print("Estado do Core: Operação Estável (Sem gerenciador de estado integrado).")

    def tasks(self):
        if hasattr(self.kernel, "task_manager") and hasattr(self.kernel.task_manager, "list_tasks"):
            tasks = self.kernel.task_manager.list_tasks()
            if not tasks:
                print("Nenhuma tarefa concorrente em execução no Engine.")
                return
            for task in tasks:
                print(f" -> {task}")
        else:
            print("Gerenciador de tarefas assíncronas indisponível.")

    def plugins(self):
        if hasattr(self.kernel, "plugin_manager") and hasattr(self.kernel.plugin_manager, "list_plugins"):
            plugins = self.kernel.plugin_manager.list_plugins()
            if not plugins:
                print("Nenhum plugin de extensão carregado em memória.")
                return
            for plugin in plugins:
                print(f" [Plugin] {plugin}")
        else:
            print("Subsistema de gerenciamento de plugins offline.")

    def memories(self):
        if hasattr(self.kernel, "memory") and hasattr(self.kernel.memory, "memories"):
            memories = self.kernel.memory.memories
            print(f"Volume de memórias ativas em cache: {len(memories)}")
            for memory in memories:
                print(f" - {memory}")
        else:
            print("Banco de memória persistente/episódica inacessível.")

    def clear(self):
        # Limpeza multiplataforma via escape codes ANSI padrão
        print("\033[H\033[J", end="")

    def exit(self):
        print("\nDesconectando interface e descarregando subsistemas...")
        self.shutdown()
        if hasattr(self.kernel, "shutdown"):
            # Invoca o desligamento centralizado do sistema em outra thread para evitar deadlock
            threading.Thread(target=self.kernel.shutdown, name="SystemShutdown", daemon=True).start()

    # ==========================================================
    # Encapsulamento de Logs de Interface
    # ==========================================================

    def info(self, message):
        if self.logger: self.logger.info(message)

    def success(self, message):
        if self.logger: self.logger.success(message)

    def error(self, message):
        if self.logger: self.logger.error(message)