"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/tool_interface.py

Descrição:
Contrato base para ferramentas
executáveis do Genesis Core.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class ToolInterface(
    ABC
):
    """
    Interface base de ferramentas.

    Toda ferramenta do JARVIS
    deve implementar este contrato.
    """



    @abstractmethod
    def name(
        self
    ):
        """
        Retorna nome da ferramenta.
        """

        raise NotImplementedError()



    # ==============================================


    @abstractmethod
    def validate(
        self,
        action
    ):
        """
        Verifica compatibilidade
        com uma ação.
        """

        raise NotImplementedError()



    # ==============================================


    @abstractmethod
    def execute(
        self,
        action
    ):
        """
        Executa uma ação.
        """

        raise NotImplementedError()