"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/memory_interface.py

Descrição:
Contrato base para sistemas de memória
do Genesis Core.

Define o comportamento esperado dos módulos
responsáveis por armazenar, recuperar,
organizar e gerenciar experiências cognitivas.

Arquitetura:

Brain
 |
Memory System
 |
Cognitive Pipeline


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



class MemoryInterface(ABC):
    """
    Interface base para sistemas de memória.

    A memória mantém informações utilizadas
    pelo processo cognitivo.

    Responsabilidades:

    - armazenar experiências;
    - recuperar contexto;
    - fornecer histórico;
    - persistir informações.

    Não realiza raciocínio.
    Não toma decisões.
    """



    # ==================================================
    # ARMAZENAMENTO
    # ==================================================

    @abstractmethod
    def store(
        self,
        data,
        memory_type="short_term"
    ):
        """
        Armazena uma memória.

        Parameters
        ----------
        data:
            Informação registrada.

        memory_type:
            Tipo da memória.

            Exemplos:

            short_term
            working
            episodic
            long_term

        Returns
        -------
        result:
            Resultado da operação.
        """

        raise NotImplementedError()



    # ==================================================
    # RECUPERAÇÃO
    # ==================================================

    @abstractmethod
    def retrieve(
        self,
        query,
        context=None
    ):
        """
        Recupera memórias relacionadas.

        Parameters
        ----------
        query:
            Critério de busca.

        context:
            Contexto cognitivo atual.

        Returns
        -------
        memories:
            Memórias encontradas.
        """

        raise NotImplementedError()



    # ==================================================
    # BUSCA SEMÂNTICA
    # ==================================================

    @abstractmethod
    def search(
        self,
        query,
        limit=10
    ):
        """
        Busca memórias relevantes.

        Pode utilizar:

        - texto;
        - similaridade;
        - embeddings;
        - índices.

        Returns
        -------
        results:
            Memórias relevantes.
        """

        raise NotImplementedError()



    # ==================================================
    # REMOÇÃO TOTAL
    # ==================================================

    @abstractmethod
    def clear(
        self
    ):
        """
        Limpa memória temporária
        ou todo o armazenamento.

        Returns
        -------
        result:
            Estado da operação.
        """

        raise NotImplementedError()



    # ==================================================
    # REMOÇÃO ESPECÍFICA
    # ==================================================

    @abstractmethod
    def forget(
        self,
        memory_id
    ):
        """
        Remove uma memória específica.

        Usado para:

        - esquecimento;
        - correção;
        - manutenção.

        Parameters
        ----------
        memory_id:
            Identificador da memória.

        Returns
        -------
        result:
            Resultado da operação.
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
        Persiste memórias.

        Exemplos:

        - arquivo local;
        - banco;
        - vetor;
        - cloud.
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
        Recupera memórias persistidas.
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
        do sistema de memória.
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
        do sistema.

        Exemplos:

        memory.local
        memory.vector
        memory.episodic
        """

        raise NotImplementedError()