"""
=========================================
JARVIS CORE

Arquivo:
core/cognitive/reasoner.py

Descrição:
Implementação do Reasoner Cognitivo
do Genesis Core.

Responsável por analisar contexto,
avaliar possibilidades e auxiliar
tomadas de decisão dentro da Pipeline.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from core.interfaces.reasoner_interface import ReasonerInterface

from core.pipeline.pipeline_step import PipelineStep



class Reasoner(
    PipelineStep,
    ReasonerInterface
):
    """
    Motor de raciocínio cognitivo.

    Responsabilidades:

    - Avaliar contexto
    - Gerar análise
    - Escolher decisões

    Não executa ações.
    Não altera sistemas externos.
    """



    def __init__(
        self
    ):

        super().__init__(
            "reasoner"
        )



    # ==================================================
    # ReasonerInterface
    # ==================================================


    def reason(
        self,
        context
    ):
        """
        Executa análise cognitiva
        sobre determinado contexto.
        """


        if not context:

            return {

                "decision": None,

                "confidence": 0,

                "analysis":
                "Nenhum contexto disponível."

            }



        plan = context.get(
            "plan"
        )


        if not plan:

            return {

                "decision": None,

                "confidence": 0,

                "analysis":
                "Nenhum plano encontrado."

            }



        return {

            "context":
            context,


            "analysis":
            "Plano analisado e considerado executável.",


            "decision":
            plan,


            "confidence":
            1.0

        }



    # ==================================================


    def evaluate(
        self,
        option,
        context
    ):
        """
        Avalia uma possibilidade.
        """


        if not option:

            return {

                "valid": False,

                "score": 0

            }



        return {

            "option":
            option,


            "context":
            context,


            "score":
            1.0,


            "reason":
            "Opção considerada válida."

        }



    # ==================================================


    def decide(
        self,
        possibilities
    ):
        """
        Escolhe melhor possibilidade.

        Primeira versão:

        seleciona primeira opção.

        Futuramente:

        - pesos cognitivos
        - memória
        - aprendizado
        - LLM
        """


        if not possibilities:

            return None



        return possibilities[0]



    # ==================================================
    # PipelineStep
    # ==================================================


    def process(
        self,
        context
    ):
        """
        Executa raciocínio dentro
        da Pipeline Cognitiva.
        """


        parsed = context.data.get(
            "parsed",
            {}
        )


        plan = context.data.get(
            "plan",
            {}
        )



        analysis_context = {

            "input":
            parsed.get(
                "content"
            ),


            "plan":
            plan

        }



        reasoning = self.reason(
            analysis_context
        )



        context.data["reasoning"] = reasoning



        return context