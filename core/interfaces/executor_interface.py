"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/executor_interface.py

Descrição:
Contrato base para executores de ações
do Genesis Core.

Responsável por transformar decisões
cognitivas em operações reais.

Fluxo:

Reasoner
   ↓
Executor
   ↓
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



class ExecutorInterface(ABC):
    """
    Interface base dos Executores.

    O Executor não possui inteligência
    decisória.

    Ele apenas recebe uma ação validada
    e tenta realizá-la no ambiente.
    """



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
        Executa uma ação planejada.

        Parameters
        ----------
        action:
            Ação produzida pelo Reasoner.

        context:
            Contexto cognitivo atual.

        Returns
        -------
        result:
            Resultado da operação.
        """

        raise NotImplementedError()



    # ==================================================
    # VALIDAÇÃO
    # ==================================================

    @abstractmethod
    def validate(
        self,
        action
    ):
        """
        Valida se a ação pode ocorrer.

        Deve verificar:

        - segurança
        - permissões
        - recursos
        - dependências
        - compatibilidade

        Returns
        -------
        bool
            True quando permitido.
        """

        raise NotImplementedError()



    # ==================================================
    # REVERSÃO
    # ==================================================

    @abstractmethod
    def rollback(
        self,
        action
    ):
        """
        Tenta desfazer uma operação.

        Utilizado em:

        - falhas
        - recuperação
        - manutenção da consistência

        Returns
        -------
        result:
            Resultado do rollback.
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
        do executor.

        Usado por:

        - Kernel
        - Diagnostics
        - Dashboard
        - Plugin Manager
        """

        raise NotImplementedError()



    # ==================================================
    # IDENTIDADE
    # ==================================================

    @abstractmethod
    def name(
        self
    ):
        """
        Retorna nome lógico
        do executor.

        Exemplo:

        browser.executor
        system.executor
        device.executor
        """

        raise NotImplementedError()