"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/executor_interface.py

Descrição:
Contrato base para executores de ações
do Genesis Core.

Define o comportamento esperado de qualquer
componente responsável por transformar
planos e decisões em ações executáveis.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class ExecutorInterface(ABC):
    """
    Interface base para Executores.

    Um Executor transforma uma ação planejada
    em uma operação real dentro do ambiente.
    """



    @abstractmethod
    def execute(
        self,
        action
    ):
        """
        Executa uma ação.

        Parameters
        ----------
        action:
            Ação definida pelo sistema.

        Returns
        -------
        result:
            Resultado da execução.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def validate(
        self,
        action
    ):
        """
        Verifica se uma ação pode ser executada.

        Pode considerar:

        - permissões
        - recursos disponíveis
        - segurança
        - compatibilidade

        Parameters
        ----------
        action:
            Ação a ser validada.

        Returns
        -------
        bool
            True caso seja executável.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def rollback(
        self,
        action
    ):
        """
        Reverte uma ação quando possível.

        Usado para:

        - recuperação de falhas
        - segurança
        - consistência do sistema

        Parameters
        ----------
        action:
            Ação que precisa ser revertida.

        Returns
        -------
        result:
            Resultado da reversão.
        """

        raise NotImplementedError()