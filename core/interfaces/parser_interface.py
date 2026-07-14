"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/parser_interface.py

Descrição:
Contrato base para interpretadores
de entrada do Genesis Core.

Define o comportamento esperado de
qualquer Parser responsável por
transformar dados brutos em estruturas
compreensíveis pelo sistema.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class ParserInterface(ABC):
    """
    Interface base para Parsers.

    Um Parser converte informações
    recebidas pelo sistema em dados
    estruturados.
    """



    @abstractmethod
    def parse(
        self,
        input_data
    ):
        """
        Processa e interpreta uma entrada.

        Parameters
        ----------
        input_data:
            Informação bruta recebida.

        Returns
        -------
        parsed_data:
            Informação estruturada.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def supports(
        self,
        input_type
    ):
        """
        Verifica se o parser suporta
        determinado tipo de entrada.

        Exemplos:

        text
        voice
        command
        json
        image
        """

        raise NotImplementedError()