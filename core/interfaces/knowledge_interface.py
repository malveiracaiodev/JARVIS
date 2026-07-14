"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/knowledge_interface.py

Descrição:
Contrato base para sistemas de conhecimento
do Genesis Core.

Define o comportamento esperado de qualquer
componente responsável por armazenar,
consultar e fornecer conhecimento ao sistema.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


from abc import ABC, abstractmethod



class KnowledgeInterface(ABC):
    """
    Interface base para sistemas de conhecimento.

    O Knowledge é responsável por fornecer
    informações estruturadas utilizadas pelos
    módulos cognitivos.
    """



    @abstractmethod
    def add_knowledge(
        self,
        knowledge
    ):
        """
        Adiciona conhecimento ao sistema.

        Parameters
        ----------
        knowledge:
            Informação ou conceito a ser registrado.

        Returns
        -------
        result:
            Resultado da operação.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def get_knowledge(
        self,
        query
    ):
        """
        Recupera conhecimento baseado
        em uma consulta.

        Parameters
        ----------
        query:
            Termo ou contexto pesquisado.

        Returns
        -------
        knowledge:
            Informação encontrada.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def update_knowledge(
        self,
        knowledge_id,
        data
    ):
        """
        Atualiza uma informação existente.

        Parameters
        ----------
        knowledge_id:
            Identificador do conhecimento.

        data:
            Novos dados.

        Returns
        -------
        result:
            Resultado da atualização.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def remove_knowledge(
        self,
        knowledge_id
    ):
        """
        Remove uma informação da base
        de conhecimento.

        Parameters
        ----------
        knowledge_id:
            Identificador do conhecimento.

        Returns
        -------
        result:
            Resultado da remoção.
        """

        raise NotImplementedError()



    # ==================================================


    @abstractmethod
    def exists(
        self,
        query
    ):
        """
        Verifica se determinado conhecimento
        existe na base.

        Parameters
        ----------
        query:
            Informação procurada.

        Returns
        -------
        bool
            True caso exista.
        """

        raise NotImplementedError()