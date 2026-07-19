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
IV - Thought Engine

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


from core.pipeline.pipeline_context import (
    PipelineContext
)



class Reasoner(
    PipelineStep,
    ReasonerInterface
):


    """
    Núcleo de decisão cognitiva.

    Recebe planos.

    Avalia alternativas.

    Produz decisão.

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


    def module_name(
        self
    ):

        return self.name



    # ==================================================
    # STATUS
    # ==================================================


    def status(
        self
    ):


        return {


            "name":

                self.name,


            "decisions":

                self.decisions,


            "errors":

                self.errors

        }



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

                "Reasoner recebeu Context sem Thought."

            )


            self.errors += 1


            return context



        try:


            thought.thinking()



            parsed = thought.get_metadata(

                "parsed",

                {}

            )



            plan = thought.plan



            if plan is None:


                plan = thought.get_metadata(

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



            decision = result.get(

                "decision"

            )



            # ======================================
            # ATUALIZA CONTEXT
            # ======================================


            context.set(

                "reasoning",

                result

            )


            context.set(

                "decision",

                decision

            )



            # ======================================
            # ATUALIZA THOUGHT
            # ======================================


            thought.set_decision(

                decision

            )


            thought.set_metadata(

                "reasoning",

                result

            )


            thought.confidence = (

                result.get(

                    "confidence",

                    0

                )

            )



            thought.add_history(

                "reasoner_completed"

            )



            context.add_history(

                {

                    "event":

                        "reasoner_completed",

                    "timestamp":

                        datetime.now().isoformat()

                }

            )



        except Exception as error:


            self.errors += 1



            error_data = {


                "decision":

                    None,


                "confidence":

                    0,


                "error":

                    str(error)

            }



            context.add_error(

                error_data

            )


            context.set(

                "reasoning",

                error_data

            )


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

                str(

                    uuid.uuid4()

                ),



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



    # ==================================================
    # DIAGNÓSTICO
    # ==================================================


    def info(
        self
    ):


        return {


            "name":

                self.name,


            "decisions":

                self.decisions,


            "errors":

                self.errors,


            "history":

                len(

                    self.history

                )

        }