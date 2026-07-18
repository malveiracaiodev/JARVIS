"""
=========================================
GENESIS CORE

Arquivo:
core/interfaces/parser_interface.py

Descrição:
Contrato base para interpretadores
de entrada do Genesis Core.

Responsável por transformar dados
brutos recebidos do ambiente em
informações cognitivas armazenáveis
no Thought.

Fluxo:

Entrada
   |
   v
Parser
   |
   v
Thought.metadata
   |
   v
Planner


Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import (
    ABC,
    abstractmethod
)



class ParserInterface(ABC):

    """
    Contrato dos Parsers.

    O Parser não pensa.

    Não decide.

    Não cria planos.

    Apenas transforma dados brutos
    em estruturas compreensíveis
    pelos módulos cognitivos.
    """



    # ==================================================
    # INTERPRETAÇÃO
    # ==================================================


    @abstractmethod
    def parse(
        self,
        input_data,
        context=None
    ):

        """
        Converte entrada bruta em
        estrutura cognitiva.

        Parameters
        ----------

        input_data:

            Informação recebida
            pelo sistema.


        context:

            Contexto atual da execução.


        Returns
        -------

        parsed_data:

            Estrutura interpretada.
        """

        raise NotImplementedError()



    # ==================================================
    # COMPATIBILIDADE
    # ==================================================


    @abstractmethod
    def supports(
        self,
        input_type
    ):

        """
        Verifica tipos de entrada
        suportados.

        Exemplos:

        text

        voice

        command

        image

        file

        sensor
        """

        raise NotImplementedError()



    # ==================================================
    # CONFIANÇA
    # ==================================================


    @abstractmethod
    def confidence(
        self,
        input_data
    ):

        """
        Retorna confiança da
        interpretação realizada.

        Usado futuramente pelo
        Reasoner para decidir:

        - continuar;
        - solicitar confirmação;
        - buscar informação.
        """

        raise NotImplementedError()



    # ==================================================
    # IDENTIDADE
    # ==================================================


    @abstractmethod
    def name(
        self
    ):

        """
        Nome lógico do Parser.

        Exemplos:

        parser.text

        parser.voice

        parser.image
        """

        raise NotImplementedError()



    # ==================================================
    # STATUS
    # ==================================================


    @abstractmethod
    def status(
        self
    ):

        """
        Retorna estado operacional
        do Parser.
        """

        raise NotImplementedError()