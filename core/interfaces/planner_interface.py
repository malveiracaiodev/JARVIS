"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/planner_interface.py

Descrição:
Contrato base para sistemas de
planejamento cognitivo do Genesis Core.

Responsável por transformar intenções
em planos estruturados de ação.

Fluxo:

Intenção
   |
   v
Planner
   |
   v
Plano Cognitivo
   |
   v
Reasoner


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



class PlannerInterface(ABC):
    """
    Interface base para Planners.

    O Planner cria estratégias.

    Ele não executa ações.

    Responsabilidades:

    - decompor objetivos;
    - criar sequência de passos;
    - avaliar recursos;
    - preparar execução.
    """



    # ==================================================
    # CRIAÇÃO DE PLANO
    # ==================================================

    @abstractmethod
    def create_plan(
        self,
        intention,
        context=None
    ):
        """
        Cria um plano baseado
        em uma intenção.

        Parameters
        ----------
        intention:
            Objetivo identificado.

        context:
            Contexto cognitivo atual.

        Returns
        -------
        plan:
            Plano estruturado.
        """

        raise NotImplementedError()



    # ==================================================
    # VALIDAÇÃO
    # ==================================================

    @abstractmethod
    def validate_plan(
        self,
        plan
    ):
        """
        Verifica se o plano
        pode ser executado.

        Considera:

        - dependências;
        - recursos;
        - segurança;
        - consistência.

        Returns
        -------
        bool
        """

        raise NotImplementedError()



    # ==================================================
    # OTIMIZAÇÃO
    # ==================================================

    @abstractmethod
    def optimize_plan(
        self,
        plan
    ):
        """
        Otimiza um plano.

        Pode melhorar:

        - quantidade de passos;
        - ordem das ações;
        - recursos utilizados;
        - tempo de execução.
        """

        raise NotImplementedError()



    # ==================================================
    # DECOMPOSIÇÃO
    # ==================================================

    @abstractmethod
    def decompose(
        self,
        goal
    ):
        """
        Divide um objetivo complexo
        em subtarefas menores.

        Exemplo:

        "Preparar ambiente"

        vira:

        [
          abrir_editor,
          carregar_projeto,
          iniciar_servicos
        ]
        """

        raise NotImplementedError()



    # ==================================================
    # CANCELAMENTO
    # ==================================================

    @abstractmethod
    def cancel_plan(
        self,
        plan_id
    ):
        """
        Cancela um plano existente.

        Usado para:

        - segurança;
        - interrupção humana;
        - falhas.
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
        do Planner.
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
        Nome lógico do Planner.

        Exemplos:

        planner.basic
        planner.ai
        planner.strategy
        """

        raise NotImplementedError()