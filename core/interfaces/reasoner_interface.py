"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/reasoner_interface.py

Descrição:
Contrato base para sistemas de raciocínio
cognitivo do Genesis Core.

Define o comportamento esperado de qualquer
componente responsável por analisar contexto,
avaliar possibilidades e gerar decisões.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class ReasonerInterface(ABC):
    """
    Interface base para Reasoners.

    Um Reasoner é responsável por avaliar
    informações, contexto e possibilidades
    para auxiliar tomadas de decisão.
    """



    @abstractmethod
    def reason(
        self,
        context
    ):
        """
        Executa um processo de raciocínio.

        Parameters
        ----------
        context:
            Contexto atual da execução cognitiva.

        Returns
        -------
        reasoning_result:
            Resultado do raciocínio.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def evaluate(
        self,
        option,
        context
    ):
        """
        Avalia uma possibilidade ou opção.

        Pode considerar:

        - contexto atual
        - objetivos
        - regras
        - conhecimento disponível
        - riscos

        Parameters
        ----------
        option:
            Opção a ser avaliada.

        context:
            Contexto cognitivo.

        Returns
        -------
        evaluation:
            Avaliação da opção.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def decide(
        self,
        possibilities
    ):
        """
        Escolhe uma decisão baseada
        nas possibilidades disponíveis.

        Parameters
        ----------
        possibilities:
            Lista de alternativas.

        Returns
        -------
        decision:
            Melhor decisão encontrada.
        """

        raise NotImplementedError()