"""
=========================================
GENESIS CORE

Arquivo:
core/interfaces/knowledge_interface.py

Descrição:
Contrato base para sistemas de conhecimento
do Genesis Core.

Define o comportamento esperado de módulos
responsáveis por armazenar, consultar,
atualizar e fornecer conhecimento.

Arquitetura:

Cognitive Pipeline
        |
        v
    Knowledge System


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


class KnowledgeInterface(ABC):
    """
    Interface base para sistemas
    de conhecimento.

    O Knowledge fornece informações
    estruturadas para os módulos cognitivos.

    Não decide.
    Não raciocina.
    Apenas disponibiliza conhecimento.
    """

    # ==================================================
    # INSERÇÃO
    # ==================================================

    @abstractmethod
    def add_knowledge(
        self,
        knowledge
    ):
        """
        Adiciona conhecimento.

        Parameters
        ----------
        knowledge:
            Conceito ou informação.

        Returns
        -------
        result:
            Resultado da operação.
        """
        raise NotImplementedError()

    # ==================================================
    # CONSULTA
    # ==================================================

    @abstractmethod
    def get_knowledge(
        self,
        query,
        context=None
    ):
        """
        Busca conhecimento.

        Parameters
        ----------
        query:
            Termo pesquisado.

        context:
            Contexto cognitivo atual.

        Returns
        -------
        knowledge:
            Dados encontrados.
        """
        raise NotImplementedError()

    # ==================================================
    # PESQUISA SEMÂNTICA
    # ==================================================

    @abstractmethod
    def search(
        self,
        query
    ):
        """
        Realiza pesquisa inteligente.

        Pode utilizar:

        - indexação
        - embeddings
        - vetores
        - banco local
        - APIs externas

        Returns
        -------
        results:
            Lista de conhecimentos relacionados.
        """
        raise NotImplementedError()

    # ==================================================
    # ATUALIZAÇÃO
    # ==================================================

    @abstractmethod
    def update_knowledge(
        self,
        knowledge_id,
        data
    ):
        """
        Atualiza conhecimento existente.
        """
        raise NotImplementedError()

    # ==================================================
    # REMOÇÃO
    # ==================================================

    @abstractmethod
    def remove_knowledge(
        self,
        knowledge_id
    ):
        """
        Remove conhecimento.
        """
        raise NotImplementedError()

    # ==================================================
    # EXISTÊNCIA
    # ==================================================

    @abstractmethod
    def exists(
        self,
        query
    ):
        """
        Verifica existência
        de conhecimento.

        Returns
        -------
        bool
        """
        raise NotImplementedError()

    # ==================================================
    # PERSISTÊNCIA
    # ==================================================

    @abstractmethod
    def save(
        self
    ):
        """
        Salva conhecimento persistente.

        Exemplos:

        - banco local
        - arquivo
        - vetor
        - cloud
        """
        raise NotImplementedError()

    # ==================================================
    # CARREGAMENTO
    # ==================================================

    @abstractmethod
    def load(
        self
    ):
        """
        Carrega conhecimento
        persistido.
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
        Retorna estado
        do sistema de conhecimento.
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
        Nome lógico do provedor.

        Exemplos:

        local.knowledge
        vector.knowledge
        web.knowledge
        """
        raise NotImplementedError()