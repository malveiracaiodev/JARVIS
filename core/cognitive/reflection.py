"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/reflection.py

Descrição:
Módulo de reflexão cognitiva do Genesis Core.

Responsável por analisar resultados,
avaliar desempenho e gerar feedback
para evolução futura.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


import uuid

from datetime import datetime


from core.pipeline.pipeline_step import (
    PipelineStep
)



class Reflection(
    PipelineStep
):

    """
    Camada de avaliação cognitiva.

    Observa resultados.

    Gera conhecimento.

    Não executa.
    Não altera memória diretamente.
    """



    def __init__(
        self,
        logger=None,
        memory=None
    ):


        super().__init__(
            "reflection"
        )


        self.logger = logger

        self.memory = memory


        self.reflections = 0

        self.failures = 0


        self.history = []



    # ==================================================
    # PIPELINE
    # ==================================================


    def process(
        self,
        context
    ):


        try:


            execution = context.data.get(
                "execution",
                {}
            )


            reasoning = context.data.get(
                "reasoning",
                {}
            )



            reflection = self.analyze(

                execution,

                reasoning

            )



            context.data[
                "reflection"
            ] = reflection



            self.reflections += 1


            self.history.append(
                reflection
            )



        except Exception as error:


            self.failures += 1


            context.data[
                "reflection"
            ] = {


                "success":
                False,


                "error":
                str(error)

            }



            self.log_error(
                str(error)
            )



        return context



    # ==================================================
    # ANÁLISE
    # ==================================================


    def analyze(
        self,
        result,
        reasoning=None
    ):


        if not result:


            return {

                "id":
                str(uuid.uuid4()),


                "success":
                False,


                "analysis":
                "Nenhum resultado disponível.",


                "timestamp":
                datetime.now()
                .isoformat()

            }



        success = result.get(
            "success",
            False
        )



        if success:


            evaluation = (
                "Execução concluída."
            )


            quality = 1.0


            improvement = (

                "Estratégia considerada eficiente."

            )



        else:


            self.failures += 1


            evaluation = (

                "Execução apresentou falhas."

            )


            quality = 0.0


            improvement = (

                "Reavaliar estratégia e recursos."

            )



        return {


            "id":
            str(uuid.uuid4()),


            "timestamp":
            datetime.now()
            .isoformat(),


            "success":
            success,


            "quality":
            quality,


            "evaluation":
            evaluation,


            "improvement":
            improvement,


            "reasoning":
            reasoning,


            "original_result":
            result

        }



    # ==================================================
    # COMPARAÇÃO
    # ==================================================


    def compare(
        self,
        expected,
        actual
    ):


        return {


            "expected":
            expected,


            "actual":
            actual,


            "match":
            expected == actual,


            "timestamp":
            datetime.now()
            .isoformat()

        }



    # ==================================================
    # APRENDIZADO
    # ==================================================


    def extract_lesson(
        self,
        reflection
    ):

        """
        Extrai experiência para futura memória.

        Futuramente enviado ao MemoryManager.
        """


        if not reflection:

            return None



        return {


            "type":
            "experience",


            "success":
            reflection.get(
                "success"
            ),


            "lesson":
            reflection.get(
                "improvement"
            )

        }



    # ==================================================
    # MELHORIAS
    # ==================================================


    def suggest_improvement(
        self,
        reflection
    ):


        if not reflection:

            return []



        suggestions = []



        if not reflection.get(
            "success",
            False
        ):


            suggestions.append(

                "Reavaliar plano cognitivo."

            )


            suggestions.append(

                "Buscar alternativa de execução."

            )


        else:


            suggestions.append(

                "Registrar estratégia bem sucedida."

            )


            suggestions.append(

                "Priorizar abordagem semelhante no futuro."

            )



        return suggestions



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


    def info(self):


        return {


            "name":
            "reflection",


            "reflections":
            self.reflections,


            "failures":
            self.failures,


            "history":
            len(
                self.history
            )

        }