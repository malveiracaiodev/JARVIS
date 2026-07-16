"""
=========================================
GENESIS CORE

Arquivo:
core/managers/tool_manager.py

Descrição:
Gerenciador central de ferramentas do
Genesis Core.

Responsável por registrar, localizar,
validar e executar ferramentas do
sistema.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""

import threading

from core.base.module import Module, ModuleStatus
from core.interfaces.tool_interface import ToolInterface


class ToolManager(Module):
    """
    Gerenciador central das ferramentas
    executáveis do Genesis Core.

    Responsabilidades:

    - Registrar ferramentas
    - Remover ferramentas
    - Localizar ferramentas
    - Executar ferramentas
    - Centralizar capacidades do sistema

    O ToolManager é o único responsável
    por conhecer as Tools registradas.
    """

    def __init__(
        self,
        logger=None
    ):
        super().__init__("core.tool_manager")

        self.logger = logger

        self._tools = {}

        self._lock = threading.RLock()

    # ==================================================
    # Ciclo de vida
    # ==================================================

    def initialize(self):

        self.set_status(
            ModuleStatus.INITIALIZING
        )

        self.set_status(
            ModuleStatus.ONLINE
        )

        self._success(
            "Tool Manager ativado."
        )

    def shutdown(self):

        self.clear()

        self.set_status(
            ModuleStatus.OFFLINE
        )

        self._info(
            "Tool Manager encerrado."
        )

    # ==================================================
    # Registro
    # ==================================================

    def register(
        self,
        tool
    ):
        """
        Registra ou atualiza uma
        ferramenta.
        """

        if not isinstance(
            tool,
            ToolInterface
        ):
            raise TypeError(
                "A ferramenta deve implementar ToolInterface."
            )

        name = tool.name()

        if not name:

            raise ValueError(
                "A ferramenta precisa possuir um nome."
            )

        with self._lock:

            self._tools[name] = tool

        self._info(
            f"Ferramenta registrada: {name}"
        )

    def unregister(
        self,
        name
    ):
        """
        Remove uma ferramenta.
        """

        with self._lock:

            tool = self._tools.pop(
                name,
                None
            )

        if tool:

            self._info(
                f"Ferramenta removida: {name}"
            )

        return tool

    def clear(
        self
    ):
        """
        Remove todas as ferramentas.
        """

        with self._lock:

            self._tools.clear()

    # ==================================================
    # Consulta
    # ==================================================

    def find(
        self,
        action
    ):
        """
        Localiza uma ferramenta
        compatível com a ação.
        """

        with self._lock:

            tools = list(
                self._tools.values()
            )

        for tool in tools:

            try:

                if tool.validate(
                    action
                ):

                    return tool

            except Exception as error:

                self._error(
                    f"Falha ao validar "
                    f"{tool.name()}: {error}"
                )

        return None

    def has(
        self,
        action
    ):
        """
        Verifica se existe uma
        ferramenta compatível.
        """

        return self.find(
            action
        ) is not None

    def execute(
        self,
        action
    ):
        """
        Executa uma ação utilizando
        a primeira ferramenta
        compatível encontrada.
        """

        if not action:

            return {

                "success": False,

                "message":
                "Nenhuma ação fornecida."

            }

        tool = self.find(
            action
        )

        if tool is None:

            return {

                "success": False,

                "message":
                "Nenhuma ferramenta compatível encontrada."

            }

        try:

            result = tool.execute(
                action
            )

            return {

                "success": True,

                "tool":
                tool.name(),

                "result":
                result

            }

        except Exception as error:

            self._error(
                f"Erro executando "
                f"{tool.name()}: {error}"
            )

            return {

                "success": False,

                "error":
                str(error)

            }

    # ==================================================
    # Informações
    # ==================================================

    def get_all(
        self
    ):
        """
        Retorna uma cópia do catálogo
        de ferramentas.
        """

        with self._lock:

            return dict(
                self._tools
            )

    def list_tools(
        self
    ):
        """
        Lista todas as ferramentas
        registradas.
        """

        with self._lock:

            return list(
                self._tools.keys()
            )

    # ==================================================
    # Logging
    # ==================================================

    def _info(
        self,
        message
    ):
        if self.logger:

            self.logger.info(
                message
            )

    def _success(
        self,
        message
    ):
        if self.logger:

            self.logger.success(
                message
            )

    def _error(
        self,
        message
    ):
        if self.logger:

            self.logger.error(
                message
            )