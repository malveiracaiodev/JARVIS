"""
=========================================
GENESIS CORE

Arquivo:
core/constants/thought_status.py

Descrição:
Estados do ciclo de vida cognitivo
de pensamentos e processos internos.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from enum import Enum



class ThoughtStatus(
    str,
    Enum
):

    """
    Máquina de estados cognitiva.

    Representa o ciclo de vida
    de um pensamento Genesis.
    """



    # ==================================================
    # INICIALIZAÇÃO
    # ==================================================


    CREATED = "created"



    # ==================================================
    # PROCESSAMENTO COGNITIVO
    # ==================================================


    ANALYZING = "analyzing"


    PLANNING = "planning"


    REASONING = "reasoning"



    # ==================================================
    # EXECUÇÃO
    # ==================================================


    EXECUTING = "executing"


    WAITING = "waiting"



    # ==================================================
    # APRENDIZADO
    # ==================================================


    REFLECTING = "reflecting"


    LEARNING = "learning"



    # ==================================================
    # FINALIZAÇÃO
    # ==================================================


    COMPLETED = "completed"



    PARTIAL = "partial"



    FAILED = "failed"



    CANCELLED = "cancelled"



    EXPIRED = "expired"



    # ==================================================
    # UTILIDADES
    # ==================================================


    def is_finished(
        self
    ):

        """
        Verifica se o pensamento
        encerrou seu ciclo.
        """

        return self in [

            ThoughtStatus.COMPLETED,

            ThoughtStatus.FAILED,

            ThoughtStatus.CANCELLED,

            ThoughtStatus.EXPIRED

        ]



    def is_processing(
        self
    ):

        """
        Estados ativos de processamento.
        """

        return self in [

            ThoughtStatus.ANALYZING,

            ThoughtStatus.PLANNING,

            ThoughtStatus.REASONING,

            ThoughtStatus.EXECUTING,

            ThoughtStatus.REFLECTING,

            ThoughtStatus.LEARNING

        ]



    def is_error(
        self
    ):

        return self in [

            ThoughtStatus.FAILED

        ]



    @classmethod
    def active_states(
        cls
    ):

        """
        Retorna estados que representam
        atividade cognitiva.
        """

        return [

            cls.ANALYZING,

            cls.PLANNING,

            cls.REASONING,

            cls.EXECUTING,

            cls.REFLECTING,

            cls.LEARNING

        ]