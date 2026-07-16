"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/reasoner_interface.py

Descrição:
Contrato base para sistemas de raciocínio
cognitivo do Genesis Core.

Responsável por analisar contexto,
avaliar possibilidades e gerar decisões.

Fluxo:

Contexto
   |
   v
Reasoner
   |
   v
Decisão Cognitiva
   |
   v
Executor


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



class ReasonerInterface(ABC):
    """
    Interface base para Reasoners.

    O Reasoner é responsável por:

    - analisar informações;
    - avaliar alternativas;
    - considerar riscos;
    - gerar decisões.

    Ele não executa ações.

    Ele apenas decide.
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

        Parameters
        ----------
        context:
            Contexto cognitivo atual.

        Pode conter:

        - entrada;
        - memória;
        - conhecimento;
        - objetivo;
        - plano.

        Returns
        -------
        reasoning_result:
            Resultado do raciocínio.
        """

        raise NotImplementedError()



    # ==================================================
    # AVALIAÇÃO DE OPÇÕES
    # ==================================================

    @abstractmethod
    def evaluate(
        self,
        option,
        context
    ):
        """
        Avalia uma possibilidade.

        Considera:

        - objetivo;
        - contexto;
        - regras;
        - conhecimento;
        - segurança;
        - custo.

        Returns
        -------
        evaluation:
            Resultado da avaliação.
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
        Seleciona uma decisão.

        Parameters
        ----------
        possibilities:
            Alternativas disponíveis.

        Returns
        -------
        decision:
            Decisão escolhida.
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
        Explica o motivo de uma decisão.

        Usado para:

        - transparência;
        - debugging;
        - aprendizado;
        - interação humana.

        Returns
        -------
        explanation:
            Justificativa.
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
        Retorna confiança
        da decisão tomada.

        Exemplo:

        0.95
        0.60
        0.30

        Usado para decidir:

        - executar;
        - pedir confirmação;
        - pesquisar mais.
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
        reasoner.ai
        reasoner.hybrid
        """

        raise NotImplementedError()