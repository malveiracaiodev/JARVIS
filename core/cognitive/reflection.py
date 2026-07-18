"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/reflection.py

Descrição:
Módulo de reflexão cognitiva do Genesis Core.

Responsável por analisar o ciclo completo
do Thought após execução, avaliando:

- intenção;
- planejamento;
- decisão;
- execução;
- aprendizado.

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

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
    Camada final do ciclo cognitivo.

    Responsável por:

    - avaliar resultado;
    - gerar feedback;
    - extrair aprendizado;
    - registrar experiência.

    Não executa.
    Não decide.
    Apenas aprende.
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
    # PIPELINE MARK IV
    # ==================================================


    def process(
        self,
        context
    ):


        try:


            thought = context.thought



            if thought is None:


                context.add_error(
                    "Nenhum Thought disponível para reflexão."
                )


                return context



            reflection = self.analyze(
                thought
            )



            thought.set_metadata(
                "reflection",
                reflection
            )



            lesson = self.extract_lesson(
                reflection
            )



            thought.set_metadata(
                "lesson",
                lesson
            )



            self.reflections += 1



            self.history.append(
                reflection
            )



            return context



        except Exception as error:


            self.failures += 1


            self.log_error(
                str(error)
            )



            if context.thought:


                context.thought.set_metadata(

                    "reflection",

                    {

                        "success":
                            False,


                        "error":
                            str(error)

                    }

                )



            return context



    # ==================================================
    # ANÁLISE DO THOUGHT
    # ==================================================


    def analyze(
        self,
        thought
    ):


        result = thought.result



        success = False


        if result:


            success = result.get(
                "success",
                False
            )



        quality = (
            1.0
            if success
            else 0.0
        )



        if success:


            evaluation = (
                "Ciclo cognitivo concluído "
                "com sucesso."
            )


            improvement = (
                "Estratégia eficiente registrada."
            )



        else:


            self.failures += 1


            evaluation = (
                "Ciclo cognitivo apresentou falhas."
            )


            improvement = (
                "Reavaliar intenção, "
                "plano ou recursos."
            )



        return {


            "id":
                str(uuid.uuid4()),



            "thought_id":
                thought.id,



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



            "cognition":

                {


                    "intention":
                        thought.intention,



                    "plan":
                        thought.plan,



                    "decision":
                        thought.decision



                },



            "execution":
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


        if not reflection:


            return None



        return {


            "type":
                "experience",



            "success":
                reflection.get(
                    "success"
                ),



            "quality":
                reflection.get(
                    "quality"
                ),



            "lesson":
                reflection.get(
                    "improvement"
                ),



            "created_at":
                datetime.now()
                .isoformat()

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



        if not reflection.get(
            "success",
            False
        ):


            return [


                "Reavaliar intenção.",


                "Recalcular planejamento.",


                "Buscar nova estratégia."


            ]



        return [


            "Registrar estratégia bem sucedida.",


            "Reutilizar padrões eficientes."


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