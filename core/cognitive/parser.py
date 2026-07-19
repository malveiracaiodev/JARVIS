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
IV - Thought Engine

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


from core.pipeline.pipeline_context import (
    PipelineContext
)



class Parser(
    PipelineStep,
    ParserInterface
):


    """
    Primeira etapa cognitiva.

    Responsabilidades:

    - interpretar entrada;
    - identificar tipo;
    - estruturar dados.

    Não raciocina.
    Não planeja.
    Não executa.
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


    def module_name(
        self
    ):

        return self.name



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
    # PROCESSAMENTO
    # ==================================================


    def process(
        self,
        context: PipelineContext
    ) -> PipelineContext:


        thought = context.thought



        if thought is None:


            context.add_error(

                "Parser recebeu Context sem Thought."

            )


            self.errors += 1


            return context



        try:


            thought.thinking()



            parsed = self.parse(

                thought.message

            )



            context.set(

                "parsed",

                parsed

            )



            thought.set_metadata(

                "parsed",

                parsed

            )



            thought.add_history(

                "parser_completed"

            )



            context.add_history(

                {

                    "event":

                        "parser_completed",


                    "timestamp":

                        datetime.now().isoformat()

                }

            )



            self.processed += 1



        except Exception as error:


            self.errors += 1



            error_data = {


                "type":

                    "error",


                "content":

                    None,


                "error":

                    str(error)

            }



            context.add_error(

                error_data

            )


            context.set(

                "parsed",

                error_data

            )


            self.log_error(

                str(error)

            )



        return context



    # ==================================================
    # INTERPRETAÇÃO
    # ==================================================


    def parse(
        self,
        input_data,
        context=None
    ):


        timestamp = datetime.now().isoformat()



        if not input_data:


            return {


                "type":

                    "empty",


                "content":

                    None,


                "intent":

                    "empty",


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



            "intent":

                self.detect_intent(

                    content

                ),



            "confidence":

                self.confidence(

                    input_data

                ),



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




    def detect_intent(
        self,
        text
    ):


        text = text.lower()



        if "teste" in text:

            return "system_test"



        if (

            "olá" in text

            or

            "ola" in text

            or

            "oi" in text

        ):

            return "greeting"



        if "jarvis" in text:

            return "jarvis_command"



        return "unknown"



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
    # DIAGNÓSTICO
    # ==================================================


    def diagnostics(
        self
    ):


        return {


            "name":

                self.name,


            "processed":

                self.processed,


            "errors":

                self.errors,


            "pipeline_status":

                self.status

        }



    def info(
        self
    ):


        return self.diagnostics()



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