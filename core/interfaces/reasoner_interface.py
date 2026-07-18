"""
=========================================
GENESIS CORE

Arquivo:
core/interfaces/reasoner_interface.py

Descrição:
Contrato base para sistemas de raciocínio
cognitivo do Genesis Core.

Responsável por analisar planos,
avaliar alternativas e produzir decisões
armazenadas no Thought.

Fluxo:

Thought.plan
      |
      v
  Reasoner
      |
      v
Thought.decision
      |
      v
  Executor


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



class ReasonerInterface(ABC):

    """
    Contrato dos Reasoners.

    O Reasoner representa a camada
    de escolha cognitiva.

    Ele:

    - analisa;
    - compara;
    - avalia;
    - decide.


    Ele NÃO:

    - executa;
    - controla ferramentas;
    - altera ambiente.
    """



    # ==================================================
    # RACIOCÍNIO PRINCIPAL
    # ==================================================


    @abstractmethod
    def reason(
        self,
        context
    ):

        """
        Executa ciclo de raciocínio.

        O contexto pode conter:

        - entrada interpretada;
        - plano;
        - memória;
        - conhecimento;
        - objetivos.


        Returns:

            Resultado cognitivo contendo:

            - alternativas;
            - decisão;
            - confiança.
        """

        raise NotImplementedError()



    # ==================================================
    # AVALIAÇÃO
    # ==================================================


    @abstractmethod
    def evaluate(
        self,
        option,
        context=None
    ):

        """
        Avalia uma possibilidade.

        Considera:

        - objetivo atual;
        - plano;
        - regras;
        - segurança;
        - conhecimento.


        Returns:

            avaliação da opção.
        """

        raise NotImplementedError()



    # ==================================================
    # DECISÃO
    # ==================================================


    @abstractmethod
    def decide(
        self,
        possibilities
    ):

        """
        Seleciona a melhor alternativa.

        Recebe possibilidades
        avaliadas e retorna
        uma decisão cognitiva.
        """

        raise NotImplementedError()



    # ==================================================
    # EXPLICAÇÃO
    # ==================================================


    @abstractmethod
    def explain(
        self,
        decision
    ):

        """
        Produz explicação da decisão.

        Usado para:

        - transparência;
        - depuração;
        - aprendizado;
        - interação humana.
        """

        raise NotImplementedError()



    # ==================================================
    # CONFIANÇA
    # ==================================================


    @abstractmethod
    def confidence(
        self,
        decision
    ):

        """
        Calcula confiança da decisão.

        Valores esperados:

        0.0 -> baixa confiança

        1.0 -> alta confiança


        Pode ser utilizado para:

        - executar;
        - pedir confirmação;
        - buscar conhecimento.
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
        do Reasoner.
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
        Nome lógico do Reasoner.

        Exemplos:

        reasoner.rule_based

        reasoner.hybrid

        reasoner.ai
        """

        raise NotImplementedError()