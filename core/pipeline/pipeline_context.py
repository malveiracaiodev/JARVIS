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



class PipelineContext:
    """
    Estado temporário de uma execução
    cognitiva.

    Todas as etapas da pipeline recebem
    e retornam este objeto.
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
        # Dados produzidos pela cognição
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


    def update_step(
        self,
        step_name: str
    ):

        """
        Define etapa atual da pipeline.
        """


        self.current_step = step_name



    # ==============================================


    def add_error(
        self,
        error
    ):

        """
        Registra erro ocorrido.
        """


        self.errors.append(
            error
        )



    # ==============================================


    def add_history(
        self,
        event
    ):

        """
        Registra evento da execução.
        """


        self.history.append(
            event
        )



    # ==============================================


    def set(
        self,
        key,
        value
    ):

        """
        Armazena dado cognitivo.

        Exemplo:

        context.set(
            "plan",
            plano
        )
        """


        self.data[key] = value



    # ==============================================


    def get(
        self,
        key,
        default=None
    ):

        """
        Recupera dado cognitivo.
        """


        return self.data.get(
            key,
            default
        )



    # ==============================================


    def has_errors(
        self
    ):

        return len(
            self.errors
        ) > 0



    # ==============================================


    def summary(
        self
    ):

        """
        Retorna resumo atual
        da execução cognitiva.
        """


        return {

            "message":
            self.message,


            "data":
            self.data,


            "current_step":
            self.current_step,


            "history":
            self.history,


            "errors":
            len(self.errors)

        }