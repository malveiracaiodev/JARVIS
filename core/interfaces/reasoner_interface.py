"""
=========================================

GENESIS CORE

Arquivo:
core/interfaces/reasoner_interface.py

Descrição:
Contrato base para sistemas de raciocínio
cognitivo do Genesis Core.

Responsável por analisar planos,
avaliar alternativas e produzir decisões
armazenadas no Thought.

Fluxo:

Thought.plan
      |
      v
  Reasoner
      |
      v
Thought.decision
      |
      v
  Executor


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



class ReasonerInterface(
    ABC
):


    """
    Contrato dos Reasoners.

    O Reasoner representa a camada
    de escolha cognitiva.

    Ele:

    - analisa;
    - compara;
    - avalia;
    - decide.


    Ele NÃO:

    - executa;
    - controla ferramentas;
    - altera ambiente.
    """



    # ==================================================
    # RACIOCÍNIO PRINCIPAL
    # ==================================================


    @abstractmethod
    def reason(
        self,
        context
    ):

        """
        Executa ciclo de raciocínio.
        """

        raise NotImplementedError()



    # ==================================================
    # AVALIAÇÃO
    # ==================================================


    @abstractmethod
    def evaluate(
        self,
        option,
        context=None
    ):

        """
        Avalia uma possibilidade.
        """

        raise NotImplementedError()



    # ==================================================
    # DECISÃO
    # ==================================================


    @abstractmethod
    def decide(
        self,
        possibilities
    ):

        """
        Seleciona melhor alternativa.
        """

        raise NotImplementedError()



    # ==================================================
    # EXPLICAÇÃO
    # ==================================================


    @abstractmethod
    def explain(
        self,
        decision
    ):

        """
        Produz explicação da decisão.
        """

        raise NotImplementedError()



    # ==================================================
    # CONFIANÇA
    # ==================================================


    @abstractmethod
    def confidence(
        self,
        decision
    ):

        """
        Calcula confiança da decisão.

        Retorno:

        0.0 -> baixa

        1.0 -> alta
        """

        raise NotImplementedError()