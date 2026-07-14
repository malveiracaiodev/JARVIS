"""
=========================================
JARVIS CORE

Arquivo:
core/pipeline/pipeline_step.py

Descrição:
Classe base para etapas da Pipeline
Cognitiva do Genesis Core.

Responsável por padronizar execução
das etapas cognitivas.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class PipelineStep(
    ABC
):
    """
    Classe base de uma etapa cognitiva.

    Toda etapa deve implementar:

    process(context)

    A Pipeline chama:

    execute(context)

    que controla o ciclo da etapa.
    """



    def __init__(
        self,
        name: str
    ):

        self.name = name



    # ==================================================
    # Execução padrão da Pipeline
    # ==================================================


    def execute(
        self,
        context
    ):
        """
        Ponto único de entrada
        da Pipeline.

        Responsável por chamar
        o processamento real.
        """


        return self.process(
            context
        )



    # ==================================================
    # Processamento obrigatório
    # ==================================================


    @abstractmethod
    def process(
        self,
        context
    ):
        """
        Cada etapa deve implementar
        sua própria lógica.
        """


        raise NotImplementedError



    # ==================================================
    # Informações da etapa
    # ==================================================


    def get_name(
        self
    ):
        """
        Retorna nome da etapa.
        """


        return self.name



    # ==================================================
    # Representação
    # ==================================================


    def __repr__(
        self
    ):

        return (
            f"<PipelineStep:{self.name}>"
        )