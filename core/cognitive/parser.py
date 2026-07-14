"""
=========================================
JARVIS CORE

Arquivo:
core/cognitive/parser.py

Descrição:
Etapa de interpretação inicial da Pipeline
Cognitiva do Genesis Core.

Responsável por transformar entradas
brutas em estruturas compreensíveis.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from core.interfaces.parser_interface import ParserInterface

from core.pipeline.pipeline_step import PipelineStep



class Parser(
    PipelineStep,
    ParserInterface
):
    """
    Primeira etapa da Pipeline Cognitiva.

    Responsabilidades:

    - Receber entrada bruta
    - Estruturar dados
    - Atualizar PipelineContext

    Não interpreta intenção.
    Não planeja.
    Não executa.
    """



    def __init__(
        self
    ):

        super().__init__(
            "parser"
        )



    # ==================================================
    # PipelineStep
    # ==================================================


    def process(
        self,
        context
    ):
        """
        Executa processamento da etapa.
        """


        parsed = self.parse(
            context.message
        )


        context.data["parsed"] = parsed


        return context



    # ==================================================
    # ParserInterface
    # ==================================================


    def parse(
        self,
        input_data
    ):
        """
        Converte entrada bruta
        em estrutura cognitiva.
        """


        if not input_data:


            return {

                "type":
                "empty",

                "content":
                None

            }



        return {

            "type":
            "text",


            "content":
            str(
                input_data
            ).strip(),


            "metadata":
            {

                "source":
                "user"

            }

        }



    # ==================================================


    def supports(
        self,
        input_type
    ):
        """
        Verifica tipos suportados.
        """


        supported = [

            "text",

            "command",

            "voice"

        ]


        return input_type in supported