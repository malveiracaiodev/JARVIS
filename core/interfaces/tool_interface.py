"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/tool_interface.py

Descrição:
Contrato base para ferramentas
executáveis do Genesis Core.

Tools representam capacidades
externas utilizadas pelo Executor.

Fluxo:

Reasoner
   |
Executor
   |
Tool
   |
Ambiente


Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import (
    ABC,
    abstractmethod
)



class ToolInterface(
    ABC
):
    """
    Interface base para Tools.

    Uma Tool representa uma capacidade
    específica do sistema.

    Exemplos:

    - abrir aplicativos;
    - acessar arquivos;
    - controlar dispositivos;
    - consultar APIs.

    A Tool executa.

    Ela não decide quando executar.
    """



    # ==================================================
    # IDENTIDADE
    # ==================================================

    @abstractmethod
    def name(
        self
    ):
        """
        Retorna nome lógico
        da ferramenta.

        Exemplos:

        browser.open
        filesystem.read
        bluetooth.connect
        """

        raise NotImplementedError()



    # ==================================================
    # DESCRIÇÃO
    # ==================================================

    @abstractmethod
    def description(
        self
    ):
        """
        Retorna descrição
        da capacidade da ferramenta.

        Usado por:

        - Planner;
        - Reasoner;
        - Plugin Manager.
        """

        raise NotImplementedError()



    # ==================================================
    # COMPATIBILIDADE
    # ==================================================

    @abstractmethod
    def validate(
        self,
        action
    ):
        """
        Verifica se a ferramenta
        suporta determinada ação.

        Parameters
        ----------
        action:
            Operação solicitada.

        Returns
        -------
        bool
            True se suportado.
        """

        raise NotImplementedError()



    # ==================================================
    # EXECUÇÃO
    # ==================================================

    @abstractmethod
    def execute(
        self,
        action,
        context=None
    ):
        """
        Executa uma operação.

        Parameters
        ----------
        action:
            Ação recebida.

        context:
            Contexto cognitivo atual.

        Returns
        -------
        result:
            Resultado da operação.
        """

        raise NotImplementedError()



    # ==================================================
    # PERMISSÕES
    # ==================================================

    @abstractmethod
    def permissions(
        self
    ):
        """
        Retorna permissões necessárias.

        Exemplos:

        filesystem.read
        network.access
        device.control
        """

        raise NotImplementedError()



    # ==================================================
    # STATUS
    # ==================================================

    @abstractmethod
    def status(
        self
    ):
        """
        Retorna estado operacional
        da ferramenta.
        """

        raise NotImplementedError()