"""
=========================================
JARVIS CORE

Arquivo:
core/interfaces/brain_interface.py

Descrição:
Contrato base para o controlador cognitivo
principal do Genesis Core.

O Brain é o ponto de entrada da Matrix
Cognitiva, responsável por coordenar o
pipeline de pensamento.

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
    Interface base do Brain.

    O Brain não contém inteligência de negócio.

    Sua responsabilidade é:

    - receber estímulos;
    - encaminhar para o Cognitive Pipeline;
    - controlar memória cognitiva;
    - gerenciar estado interno.

    A inteligência está nos módulos:

    Parser
    Planner
    Reasoner
    Executor
    Reflection
    """



    # ==================================================
    # PROCESSAMENTO COGNITIVO
    # ==================================================

    @abstractmethod
    def process(
        self,
        input_data
    ):
        """
        Inicia um ciclo cognitivo.

        Fluxo:

        input
          ↓
        PipelineContext
          ↓
        CognitivePipeline
          ↓
        resultado


        Parameters
        ----------
        input_data:
            Entrada recebida pelo sistema.


        Returns
        -------
        result:
            Resultado final do processamento.
        """

        raise NotImplementedError()



    # ==================================================
    # APRENDIZADO
    # ==================================================

    @abstractmethod
    def learn(
        self,
        data
    ):
        """
        Registra aprendizado no sistema.

        O aprendizado pode representar:

        - novas informações;
        - experiências;
        - ajustes cognitivos;
        - atualização de memória.


        O Brain apenas encaminha.

        A implementação pertence ao sistema
        de memória/conhecimento.
        """

        raise NotImplementedError()



    # ==================================================
    # RESET
    # ==================================================

    @abstractmethod
    def reset(
        self
    ):
        """
        Limpa estados temporários
        do processo cognitivo.

        Exemplos:

        - contexto atual;
        - pensamentos temporários;
        - fila cognitiva;
        - estados internos.
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
        Retorna o estado atual
        do cérebro.

        Usado pelo Kernel,
        Diagnostics e Dashboard.
        """

        raise NotImplementedError()