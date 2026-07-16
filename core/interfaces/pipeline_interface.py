"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/pipeline_interface.py

Descrição:
Contrato base para Pipelines Cognitivas
do Genesis Core.

Define o comportamento esperado de
qualquer orquestrador de processamento
cognitivo.

Fluxo:

Input
 |
Pipeline
 |
Steps Cognitivos
 |
Resultado


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



class PipelineInterface(ABC):
    """
    Interface base para pipelines.

    A Pipeline é responsável por
    coordenar etapas cognitivas.

    Ela não possui inteligência própria.

    Apenas orquestra:

    Parser
    Planner
    Reasoner
    Executor
    Reflection
    """



    # ==================================================
    # PROCESSAMENTO
    # ==================================================

    @abstractmethod
    def process(
        self,
        input_data,
        context=None
    ):
        """
        Executa o fluxo cognitivo.

        Parameters
        ----------
        input_data:
            Entrada inicial.

        context:
            PipelineContext atual.

        Returns
        -------
        result:
            Resultado final.
        """

        raise NotImplementedError()



    # ==================================================
    # ADICIONAR ETAPA
    # ==================================================

    @abstractmethod
    def add_step(
        self,
        step
    ):
        """
        Adiciona uma etapa cognitiva.

        Exemplos:

        Parser
        Planner
        Reasoner
        Executor
        Reflection
        """

        raise NotImplementedError()



    # ==================================================
    # REMOVER ETAPA
    # ==================================================

    @abstractmethod
    def remove_step(
        self,
        step_name
    ):
        """
        Remove uma etapa pelo nome.
        """

        raise NotImplementedError()



    # ==================================================
    # LISTAR ETAPAS
    # ==================================================

    @abstractmethod
    def steps(
        self
    ):
        """
        Retorna as etapas registradas
        na pipeline.

        Returns
        -------
        list
            Etapas ativas.
        """

        raise NotImplementedError()



    # ==================================================
    # RESET
    # ==================================================

    @abstractmethod
    def reset(
        self
    ):
        """
        Limpa estado temporário
        da pipeline.
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
        da pipeline.
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
        Nome lógico da pipeline.

        Exemplos:

        cognitive.pipeline
        voice.pipeline
        automation.pipeline
        """

        raise NotImplementedError()