"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/parser.py

Descrição:
Primeira etapa da Pipeline Cognitiva.

Responsável por transformar entradas
brutas em estruturas cognitivas.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.interfaces.parser_interface import (
    ParserInterface
)


from core.pipeline.pipeline_step import (
    PipelineStep
)



class Parser(
    PipelineStep,
    ParserInterface
):

    """
    Entrada inicial da inteligência.

    Não interpreta.
    Não raciocina.
    Não executa.

    Apenas estrutura informação.
    """



    def __init__(
        self,
        logger=None
    ):

        super().__init__(
            "parser"
        )


        self.logger = logger


        self.processed = 0

        self.errors = 0



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def name(
        self
    ):

        return "parser"



    # ==================================================
    # STATUS
    # ==================================================


    def status(
        self
    ):

        return {

            "name":
                self.name(),


            "processed":
                self.processed,


            "errors":
                self.errors

        }



    # ==================================================
    # CONFIANÇA
    # ==================================================


    def confidence(
        self,
        input_data
    ):


        if not input_data:

            return 0.0



        if self.errors > self.processed:

            return 0.2



        return 1.0



    # ==================================================
    # PIPELINE
    # ==================================================


    def process(
        self,
        context
    ):

        try:


            parsed = self.parse(
                context.message
            )


            context.data[
                "parsed"
            ] = parsed


            self.processed += 1



        except Exception as error:


            self.errors += 1


            context.data[
                "parsed"
            ] = {


                "type":
                    "error",


                "content":
                    None,


                "error":
                    str(error)

            }


            self.log_error(
                str(error)
            )



        return context



    # ==================================================
    # PARSER
    # ==================================================


    def parse(
        self,
        input_data,
        context=None
    ):


        timestamp = (
            datetime.now()
            .isoformat()
        )



        if not input_data:


            return {


                "type":
                    "empty",


                "content":
                    None,


                "metadata":
                {

                    "source":
                        "unknown",


                    "timestamp":
                        timestamp

                }

            }



        content = str(
            input_data
        ).strip()



        return {


            "type":
                self.detect_type(
                    input_data
                ),


            "content":
                content,


            "metadata":
            {

                "source":
                    "user",


                "timestamp":
                    timestamp,


                "length":
                    len(content)

            }

        }



    # ==================================================
    # DETECÇÃO
    # ==================================================


    def detect_type(
        self,
        data
    ):


        if isinstance(
            data,
            str
        ):

            return "text"



        return type(
            data
        ).__name__



    # ==================================================
    # SUPORTE
    # ==================================================


    def supports(
        self,
        input_type
    ):


        return input_type in [

            "text",

            "command",

            "voice",

            "image",

            "file"

        ]



    # ==================================================
    # LOG
    # ==================================================


    def log_error(
        self,
        message
    ):


        if self.logger:

            self.logger.error(
                message
            )



    # ==================================================
    # DIAGNÓSTICO
    # ==================================================


    def info(
        self
    ):


        return {


            "name":
                self.name(),


            "processed":
                self.processed,


            "errors":
                self.errors,


            "confidence":
                self.confidence(
                    None
                )

        }