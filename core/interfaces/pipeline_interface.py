"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/pipeline_interface.py

Descrição:
Contrato base para Pipelines Cognitivas
do Genesis Core.

Define o comportamento esperado de
qualquer pipeline do sistema.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class PipelineInterface(ABC):
    """
    Interface base para pipelines.

    Qualquer pipeline do Genesis Core
    deve implementar este contrato.
    """


    @abstractmethod
    def process(self, input_data):
        """
        Processa uma entrada.

        Parameters
        ----------
        input_data:
            Dados recebidos pela pipeline.

        Returns
        -------
        resultado:
            Resultado do processamento.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def add_step(self, step):
        """
        Adiciona uma etapa na pipeline.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def remove_step(self, step_name):
        """
        Remove uma etapa da pipeline.
        """

        raise NotImplementedError()