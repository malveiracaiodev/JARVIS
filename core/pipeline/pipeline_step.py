"""
=========================================
GENESIS CORE

Arquivo:
core/pipeline/pipeline_step.py

Descrição:
Classe base para etapas da Pipeline
Cognitiva do Genesis Core.

Cada etapa trabalha exclusivamente
sobre o PipelineContext.

O Thought é transportado pelo Context
como unidade cognitiva central.

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


from core.pipeline.pipeline_context import (
    PipelineContext
)



class PipelineStep(
    ABC
):


    """
    Classe base das etapas cognitivas.

    Responsabilidade:

    Receber Context.

    Ler Thought.

    Atualizar Thought.

    Retornar Context.

    Não cria fluxo.
    Não controla outras etapas.
    """



    def __init__(
        self,
        name: str
    ):


        self.name = name



    # ==================================================
    # EXECUÇÃO PADRÃO MARK IV
    # ==================================================


    def execute(
        self,
        context: PipelineContext
    ) -> PipelineContext:


        return self.process(
            context
        )



    # ==================================================
    # PROCESSAMENTO
    # ==================================================


    @abstractmethod
    def process(
        self,
        context: PipelineContext
    ) -> PipelineContext:


        """
        Processa uma etapa cognitiva.

        Cada módulo deve:

        - acessar context.thought;
        - atualizar Thought;
        - retornar Context.
        """

        raise NotImplementedError()



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def get_name(
        self
    ):


        return self.name



    # ==================================================
    # REPRESENTAÇÃO
    # ==================================================


    def __repr__(
        self
    ):


        return (

            f"<PipelineStep:{self.name}>"

        )