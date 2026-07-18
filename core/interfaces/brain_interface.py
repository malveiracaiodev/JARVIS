"""
=========================================
GENESIS CORE

Arquivo:
core/interfaces/brain_interface.py

Descrição:
Contrato base para o controlador cognitivo
principal do Genesis Core.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class BrainInterface(ABC):
    """
    Interface base do Brain.

    Responsável por definir o contrato
    cognitivo do núcleo mental.

    O Brain:

    - recebe estímulos;
    - encaminha para Pipeline Cognitiva;
    - controla memória cognitiva;
    - gerencia estado interno.

    Não executa infraestrutura.
    """


    # ==================================================
    # PROCESSAMENTO COGNITIVO
    # ==================================================

    @abstractmethod
    def process(
        self,
        input_data
    ):
        """
        Executa um ciclo cognitivo.
        """

        raise NotImplementedError()



    # ==================================================
    # APRENDIZADO
    # ==================================================

    @abstractmethod
    def learn(
        self,
        data
    ):
        """
        Registra aprendizado cognitivo.
        """

        raise NotImplementedError()



    # ==================================================
    # RESET
    # ==================================================

    @abstractmethod
    def reset(
        self
    ):
        """
        Limpa estados temporários.
        """

        raise NotImplementedError()



    # ==================================================
    # ESTADO COGNITIVO
    # ==================================================

    @abstractmethod
    def get_brain_status(
        self
    ):
        """
        Retorna o estado interno cognitivo.

        Exemplos:

        - OFFLINE
        - INITIALIZING
        - ONLINE
        - THINKING
        - ERROR
        """

        raise NotImplementedError()