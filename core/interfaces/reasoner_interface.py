"""
=========================================
GENESIS CORE

Arquivo:
core/interfaces/reasoner_interface.py

Descrição:
Contrato base para sistemas de raciocínio
cognitivo do Genesis Core (Mark IV - Neural Lattice).

Responsável por analisar planos,
avaliar alternativas e produzir decisões
armazenadas no Thought, integradas ao 
fluxo da Neural Lattice.

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
IV - Thought Engine / Neural Lattice

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
    de escolha cognitiva dentro da Neural Lattice.

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
        Executa ciclo de raciocínio sobre o 
        contexto da Neural Lattice.
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
        Avalia uma possibilidade dentro do 
        espaço de estados da Lattice.
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
        Seleciona melhor alternativa baseada
        na lógica da Thought Engine.
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
        Produz explicação estruturada da 
        decisão para transparência da Lattice.
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
        Calcula nível de confiança da decisão.

        Retorno:

        0.0 -> baixa

        1.0 -> alta
        """
        raise NotImplementedError()