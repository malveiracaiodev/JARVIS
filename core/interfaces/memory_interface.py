"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/memory_interface.py

Descrição:
Contrato base para sistemas de memória
do Genesis Core.

Define o comportamento esperado de qualquer
componente responsável por armazenar,
recuperar e gerenciar informações.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class MemoryInterface(ABC):
    """
    Interface base para sistemas de memória.

    A memória é responsável por manter
    informações persistentes ou temporárias
    utilizadas pelos módulos cognitivos.
    """



    @abstractmethod
    def store(
        self,
        data
    ):
        """
        Armazena uma informação na memória.

        Parameters
        ----------
        data:
            Informação a ser armazenada.

        Returns
        -------
        result:
            Resultado do armazenamento.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def retrieve(
        self,
        query
    ):
        """
        Recupera informações da memória.

        Parameters
        ----------
        query:
            Critério de busca.

        Returns
        -------
        memories:
            Memórias encontradas.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def search(
        self,
        query,
        limit=10
    ):
        """
        Pesquisa memórias relevantes.

        Pode utilizar:

        - busca textual
        - similaridade semântica
        - embeddings
        - índices

        Parameters
        ----------
        query:
            Termo ou contexto da busca.

        limit:
            Quantidade máxima de resultados.

        Returns
        -------
        results:
            Memórias relevantes.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def clear(
        self
    ):
        """
        Remove ou limpa memórias.

        Returns
        -------
        result:
            Estado da operação.
        """

        raise NotImplementedError()