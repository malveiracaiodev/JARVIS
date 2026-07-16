"""
=========================================
GENESIS CORE

Arquivo:
core/constants/priorities.py

Descrição:
Sistema de prioridades cognitivas
e operacionais do Genesis Core.

Utilizado por:

- TaskManager
- Planner
- Reasoner
- Runtime
- Agents
- EventBus

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from enum import IntEnum



class Priority(
    IntEnum
):

    """
    Níveis de prioridade do sistema.

    Quanto maior o valor,
    maior a urgência.
    """



    # ==================================================
    # SISTEMA
    # ==================================================


    LOWEST = 0


    LOW = 25


    NORMAL = 50


    HIGH = 75


    CRITICAL = 100



    # ==================================================
    # ALTA DISPONIBILIDADE
    # ==================================================


    EMERGENCY = 125



    # ==================================================
    # UTILIDADES
    # ==================================================


    def description(
        self
    ):

        descriptions = {


            Priority.LOWEST:
            "Sem urgência. Pode aguardar.",


            Priority.LOW:
            "Baixa prioridade operacional.",


            Priority.NORMAL:
            "Execução padrão.",


            Priority.HIGH:
            "Deve ser processado rapidamente.",


            Priority.CRITICAL:
            "Prioridade elevada. Requer atenção.",


            Priority.EMERGENCY:
            "Evento crítico do sistema."

        }


        return descriptions.get(
            self,
            "Prioridade desconhecida."
        )



    def is_urgent(
        self
    ):

        return self >= Priority.HIGH



    def is_critical(
        self
    ):

        return self >= Priority.CRITICAL



    @classmethod
    def from_value(
        cls,
        value
    ):

        """
        Converte número em prioridade.
        """

        for priority in cls:

            if priority.value == value:

                return priority


        return cls.NORMAL