"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/pipeline_interface.py

Descrição:
Contrato base para Pipelines Cognitivas
do Genesis Core.

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



class PipelineInterface(
    ABC
):


    """
    Contrato base para pipelines.

    A Pipeline apenas coordena
    etapas cognitivas.

    Não possui inteligência própria.
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

        raise NotImplementedError()



    # ==================================================
    # ETAPAS
    # ==================================================


    @abstractmethod
    def add_step(
        self,
        step
    ):

        raise NotImplementedError()



    @abstractmethod
    def remove_step(
        self,
        step_name
    ):

        raise NotImplementedError()



    @abstractmethod
    def steps(
        self
    ):

        raise NotImplementedError()



    # ==================================================
    # CICLO
    # ==================================================


    @abstractmethod
    def reset(
        self
    ):

        raise NotImplementedError()



    # ==================================================
    # IDENTIDADE
    # ==================================================


    @property
    @abstractmethod
    def name(
        self
    ):

        raise NotImplementedError()



    # ==================================================
    # STATUS
    # ==================================================


    @property
    @abstractmethod
    def status(
        self
    ):

        raise NotImplementedError()