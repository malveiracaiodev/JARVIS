"""
=========================================
GENESIS CORE

Arquivo:
core/interfaces/planner_interface.py

Descrição:
Contrato base para sistemas de
planejamento cognitivo do Genesis Core.

Responsável por transformar intenções
armazenadas no Thought em planos
estruturados.

Fluxo:

Thought
   |
   v
Planner
   |
   v
Thought.plan
   |
   v
Reasoner


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



class PlannerInterface(ABC):

    """
    Contrato dos Planners.

    O Planner cria caminhos.

    Ele não escolhe caminhos.

    Ele não executa ações.

    Responsabilidades:

    - transformar intenção em plano;
    - decompor objetivos;
    - organizar etapas;
    - preparar raciocínio.
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
        Cria uma estrutura de plano.

        Parameters
        ----------

        intention:

            Objetivo identificado
            pelo sistema.


        context:

            PipelineContext atual.


        Returns
        -------

        plan:

            Estrutura planejável.
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
        Verifica consistência
        de um plano.

        Deve avaliar:

        - estrutura;
        - dependências;
        - recursos;
        - segurança.

        Returns:

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
        Melhora um plano existente.

        Pode alterar:

        - ordem dos passos;
        - quantidade de etapas;
        - eficiência;
        - custo.
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
        Divide objetivos complexos.

        Exemplo:

        "Configurar ambiente"

        torna-se:

        [
            instalar recursos,
            configurar sistema,
            validar execução
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

        Usado em:

        - interrupção humana;
        - falha;
        - segurança.
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

        planner.strategy

        planner.ai
        """

        raise NotImplementedError()