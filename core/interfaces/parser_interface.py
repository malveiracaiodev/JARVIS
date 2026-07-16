"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/parser_interface.py

Descrição:
Contrato base para interpretadores
de entrada do Genesis Core.

Responsável por transformar dados
brutos recebidos do ambiente em
estruturas cognitivamente utilizáveis.

Fluxo:

Entrada bruta
      |
      v
    Parser
      |
      v
PipelineContext


Arquitetura:
Genesis Core

Mark:
III - Intelligence

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
    Interface base para Parsers.

    O Parser não decide.

    Ele apenas:

    - interpreta;
    - organiza;
    - classifica;
    - prepara dados.

    A inteligência fica nos módulos:

    Planner
    Reasoner
    Brain
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
        Converte entrada bruta
        em estrutura cognitiva.

        Parameters
        ----------
        input_data:
            Informação recebida.

        context:
            Contexto atual do sistema.

        Returns
        -------
        parsed_data:
            Dados estruturados.
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
        Verifica suporte ao tipo
        de entrada.

        Exemplos:

        text
        voice
        command
        json
        image
        sensor
        api
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
        Retorna nível de confiança
        da interpretação.

        Exemplo:

        0.95
        0.70
        0.40

        Usado pelo Reasoner para
        decidir se deve perguntar
        confirmação.
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
        Retorna nome lógico
        do parser.

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
        do parser.
        """

        raise NotImplementedError()