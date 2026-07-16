"""
=========================================
GENESIS CORE

Arquivo:
core/cognitive/reasoner.py

Descrição:
Motor de raciocínio cognitivo do Genesis.

Responsável por analisar contexto,
avaliar alternativas e produzir decisões.

Não executa ações.

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


from core.interfaces.reasoner_interface import (
    ReasonerInterface
)


from core.pipeline.pipeline_step import (
    PipelineStep
)



class Reasoner(
    PipelineStep,
    ReasonerInterface
):

    """
    Núcleo de decisão cognitiva.

    Recebe planos.

    Analisa possibilidades.

    Produz decisões.

    Não executa.
    """



    def __init__(
        self,
        logger=None,
        memory=None
    ):


        super().__init__(
            "reasoner"
        )


        self.logger = logger

        self.memory = memory


        self.decisions = 0

        self.errors = 0


        self.history = []



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def name(
        self
    ):

        return "reasoner"



    # ==================================================
    # STATUS
    # ==================================================


    def status(
        self
    ):

        return {

            "name":
            self.name(),

            "decisions":
            self.decisions,

            "errors":
            self.errors

        }



    # ==================================================
    # PIPELINE
    # ==================================================


    def process(
        self,
        context
    ):


        try:


            parsed = context.data.get(
                "parsed",
                {}
            )


            plan = context.data.get(
                "plan",
                {}
            )



            reasoning_context = {


                "input":
                parsed.get(
                    "content"
                ),


                "plan":
                plan

            }



            result = self.reason(
                reasoning_context
            )



            context.data[
                "reasoning"
            ] = result



        except Exception as error:


            self.errors += 1


            context.data[
                "reasoning"
            ] = {

                "decision":
                None,

                "confidence":
                0,

                "error":
                str(error)

            }



            self.log_error(
                str(error)
            )



        return context



    # ==================================================
    # RACIOCÍNIO
    # ==================================================


    def reason(
        self,
        context
    ):


        plan = context.get(
            "plan"
        )


        if not plan:


            return {

                "decision":
                None,

                "confidence":
                0,

                "analysis":
                "Nenhum plano disponível."

            }



        options = self.generate_options(
            plan
        )


        decision = self.decide(
            options
        )


        result = {


            "id":
            str(uuid.uuid4()),


            "timestamp":
            datetime.now()
            .isoformat(),


            "alternatives":
            options,


            "decision":
            decision,


            "confidence":
            self.confidence(
                decision
            )


        }


        self.decisions += 1


        self.history.append(
            result
        )


        return result



    # ==================================================
    # OPÇÕES
    # ==================================================


    def generate_options(
        self,
        plan
    ):


        return [

            {

                "strategy":
                "execute_plan",

                "plan":
                plan,

                "score":
                1.0

            }

        ]



    # ==================================================
    # AVALIAÇÃO
    # ==================================================


    def evaluate(
        self,
        option,
        context=None
    ):


        if not option:


            return {

                "valid":
                False,

                "score":
                0

            }



        return {

            "option":
            option,

            "score":
            option.get(
                "score",
                0
            ),

            "valid":
            True

        }



    # ==================================================
    # DECISÃO
    # ==================================================


    def decide(
        self,
        possibilities
    ):


        if not possibilities:

            return None



        return sorted(

            possibilities,

            key=lambda x:
            x.get(
                "score",
                0
            ),

            reverse=True

        )[0]



    # ==================================================
    # CONFIANÇA
    # ==================================================


    def confidence(
        self,
        decision
    ):


        if not decision:

            return 0


        return decision.get(
            "score",
            0
        )



    # ==================================================
    # EXPLICAÇÃO
    # ==================================================


    def explain(
        self,
        decision
    ):


        if not decision:

            return "Nenhuma decisão tomada."


        return (
            "Decisão selecionada baseada "
            "na maior pontuação disponível."
        )



    # ==================================================
    # COMPATIBILIDADE
    # ==================================================


    def evaluate_options(
        self,
        options,
        context=None
    ):

        return [

            self.evaluate(
                option,
                context
            )

            for option in options

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