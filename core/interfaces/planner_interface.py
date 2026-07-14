"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/planner_interface.py

Descrição:
Contrato base para sistemas de
planejamento cognitivo do Genesis Core.

Define o comportamento esperado de
qualquer componente responsável por
transformar intenções em planos.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class PlannerInterface(ABC):
    """
    Interface base para Planners.

    Um Planner transforma uma intenção
    ou objetivo em uma sequência de ações.
    """



    @abstractmethod
    def create_plan(
        self,
        intention
    ):
        """
        Cria um plano baseado em uma intenção.

        Parameters
        ----------
        intention:
            Objetivo identificado pelo sistema.

        Returns
        -------
        plan:
            Plano de execução.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def validate_plan(
        self,
        plan
    ):
        """
        Verifica se um plano é válido
        antes da execução.

        Parameters
        ----------
        plan:
            Plano criado.

        Returns
        -------
        bool
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def optimize_plan(
        self,
        plan
    ):
        """
        Melhora um plano existente.

        Pode envolver:

        - redução de passos
        - escolha de ferramentas
        - otimização de recursos
        """

        raise NotImplementedError()