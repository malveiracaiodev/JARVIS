"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/brain_interface.py

Descrição:
Contrato base para módulos cognitivos
do Genesis Core.

Define o comportamento esperado de
qualquer sistema responsável por
processamento inteligente.

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
    Interface base para cérebros
    do Genesis Core.

    O Brain é responsável por iniciar
    processos cognitivos, mas não deve
    conter regras de negócio.
    """



    @abstractmethod
    def process(
        self,
        input_data
    ):
        """
        Processa uma entrada cognitiva.

        Parameters
        ----------
        input_data:
            Informação recebida pelo cérebro.

        Returns
        -------
        resultado:
            Resultado do processamento.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def learn(
        self,
        data
    ):
        """
        Adiciona aprendizado ao sistema.

        Pode representar:
        - atualização de conhecimento
        - adaptação
        - incorporação de informação

        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def reset(
        self
    ):
        """
        Reinicia o estado cognitivo
        temporário do cérebro.
        """

        raise NotImplementedError()