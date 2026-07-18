"""
=========================================
JARVIS CORE

Arquivo:
core/pipeline/pipeline_context.py

Descrição:
Contexto compartilhado da Pipeline
Cognitiva do Genesis Core.

Responsável por transportar o estado
de uma execução cognitiva entre etapas.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.models.thought import Thought



class PipelineContext:
    """
    Estado temporário de uma execução
    cognitiva.

    O Context mantém o ambiente.

    O Thought mantém o pensamento.
    """



    def __init__(
        self,
        message=None
    ):


        # ==============================================
        # Entrada original
        # ==============================================

        self.message = message



        # ==============================================
        # Pensamento cognitivo atual
        # ==============================================

        self.thought = Thought(
            message=message
        )



        # ==============================================
        # Dados auxiliares
        # ==============================================

        self.data = {}



        # ==============================================
        # Componentes conectados
        # ==============================================

        self.agent = None

        self.persona = None

        self.memory = None

        self.knowledge = None

        self.tools = []



        # ==============================================
        # Controle da execução
        # ==============================================

        self.metadata = {}

        self.errors = []

        self.history = []

        self.created_at = datetime.now()

        self.current_step = None



    # ==============================================
    # THOUGHT
    # ==============================================


    def set_thought(
        self,
        thought
    ):

        self.thought = thought



    def get_thought(
        self
    ):

        return self.thought



    def finish_thought(
        self
    ):

        if self.thought:

            self.thought.finish()



    # ==============================================
    # ETAPA ATUAL
    # ==============================================


    def update_step(
        self,
        step_name: str
    ):

        self.current_step = step_name



    # ==============================================
    # ERROS
    # ==============================================


    def add_error(
        self,
        error
    ):

        self.errors.append(
            error
        )



    # ==============================================
    # HISTÓRICO
    # ==============================================


    def add_history(
        self,
        event
    ):

        self.history.append(
            event
        )



    # ==============================================
    # DADOS AUXILIARES
    # ==============================================


    def set(
        self,
        key,
        value
    ):

        self.data[key] = value



    def get(
        self,
        key,
        default=None
    ):

        return self.data.get(
            key,
            default
        )



    # ==============================================
    # STATUS
    # ==============================================


    def has_errors(
        self
    ):

        return len(
            self.errors
        ) > 0



    # ==============================================
    # RESUMO
    # ==============================================


    def summary(
        self
    ):


        return {


            "message":
                self.message,


            "thought":
                (
                    self.thought.to_dict()
                    if self.thought
                    else None
                ),


            "data":
                self.data,


            "current_step":
                self.current_step,


            "history":
                self.history,


            "errors":
                len(
                    self.errors
                )

        }