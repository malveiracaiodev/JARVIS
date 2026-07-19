"""
=========================================

GENESIS CORE

Arquivo:
core/interfaces/executor_interface.py

Descrição:
Contrato base para executores cognitivos
do Genesis Core.

Transforma decisões armazenadas no
Thought em operações reais.

Fluxo:

Thought
   ↓
Reasoner
   ↓
Executor
   ↓
ToolManager
   ↓
Ambiente


Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira

=========================================
"""


from abc import (
    ABC,
    abstractmethod
)



class ExecutorInterface(
    ABC
):


    """
    Contrato dos executores.

    O Executor não possui inteligência.

    Ele não cria decisões.

    Ele apenas transforma uma decisão
    existente em ação executável.
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
        Executa uma ação cognitiva.

        Parameters
        ----------

        action:

            Decisão produzida pelo Reasoner.


        context:

            PipelineContext atual.


        Returns
        -------

        result:

            Resultado da execução.
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
        Verifica se uma ação
        pode ser executada.

        Considera:

        - ferramenta disponível;
        - permissões;
        - segurança;
        - dependências.
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
        """

        raise NotImplementedError()