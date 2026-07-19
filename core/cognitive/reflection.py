"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/reflection.py

Descrição:
Módulo final de reflexão cognitiva.

Responsável por avaliar o ciclo completo
de um Thought após execução.

Analisa:

- intenção;
- plano;
- decisão;
- execução;
- resultado;
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


from core.pipeline.pipeline_context import (
    PipelineContext
)



class Reflection(
    PipelineStep
):

    """
    Última etapa da Thought Engine.

    Responsável por transformar uma
    execução em experiência cognitiva.

    Não executa.
    Não decide.

    Aprende com o resultado.
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
        context: PipelineContext
    ):


        try:


            thought = context.thought


            if thought is None:


                context.add_error(
                    "Reflection recebeu Context sem Thought."
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


            context.set(
                "reflection",
                reflection
            )


            context.add_history(

                {
                    "step":
                        "reflection",

                    "status":
                        "completed",

                    "timestamp":
                        datetime.now().isoformat()
                }

            )


            self.reflections += 1


            self.history.append(
                reflection
            )



            # ==========================================
            # FINALIZA THOUGHT
            # ==========================================

            if reflection["success"]:

                thought.confidence = (
                    reflection["quality"]
                )


                thought.completed()


            else:

                thought.failed()



            return context



        except Exception as error:


            self.failures += 1


            self.log_error(
                str(error)
            )


            if context.thought:


                context.thought.set_metadata(

                    "reflection_error",

                    str(error)

                )


                context.thought.failed()



            context.add_error(
                str(error)
            )


            return context



    # ==================================================
    # ANÁLISE
    # ==================================================


    def analyze(
        self,
        thought
    ):


        result = thought.result



        success = False



        if isinstance(
            result,
            dict
        ):


            success = result.get(
                "success",
                False
            )


        elif result is not None:


            success = True



        quality = (

            1.0

            if success

            else 0.0

        )



        if success:


            evaluation = (
                "Execução cognitiva concluída."
            )


            improvement = (
                "Estratégia registrada como eficiente."
            )


        else:


            evaluation = (
                "Execução apresentou falhas."
            )


            improvement = (
                "Reavaliar intenção, "
                "planejamento ou ferramentas."
            )



        return {


            "id":
                str(uuid.uuid4()),



            "thought_id":
                thought.id,



            "timestamp":
                datetime.now().isoformat(),



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
    # APRENDIZADO
    # ==================================================


    def extract_lesson(
        self,
        reflection
    ):


        return {


            "id":
                str(uuid.uuid4()),



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
                datetime.now().isoformat()

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
                datetime.now().isoformat()

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

                "Criar novo plano.",

                "Buscar outra estratégia."

            ]



        return [

            "Registrar padrão eficiente.",

            "Reutilizar estratégia."

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
    # STATUS
    # ==================================================


    def info(
        self
    ):


        return {


            "name":
                self.name,


            "reflections":
                self.reflections,


            "failures":
                self.failures,


            "history":
                len(
                    self.history
                )

        }