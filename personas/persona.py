"""
=========================================
GENESIS CORE

Arquivo:
personas/persona.py

Descrição:
Classe base universal para personalidades
do Genesis Core.

Responsável por:

- Identidade do agente
- Estilo de comunicação
- Regras comportamentais
- Preferências cognitivas
- Integração com Response Engine
- Preparação de contexto

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime
import json
import os



class Persona:

    """
    Classe base para qualquer personalidade
    existente no Genesis.

    Exemplos:

    - Jarvis
    - Rafiki
    - Futuras personas
    """


    def __init__(
        self,
        name,
        role,
        description="",
        tone="neutral",
        traits=None,
        rules=None,
        capabilities=None
    ):


        # ==========================================
        # IDENTIDADE
        # ==========================================

        self.name = name

        self.role = role

        self.description = description



        # ==========================================
        # COMPORTAMENTO
        # ==========================================

        self.tone = tone


        self.traits = traits or []


        self.rules = rules or []



        # ==========================================
        # ACESSOS
        # ==========================================

        self.capabilities = capabilities or []



        # ==========================================
        # CONEXÕES
        # ==========================================

        self.response_engine = None

        self.memory = None

        self.tools = None



        # ==========================================
        # ESTADO
        # ==========================================

        self.created_at = (
            datetime.now()
            .isoformat()
        )



    # ==================================================
    # CONEXÕES
    # ==================================================


    def connect_response_engine(
        self,
        engine
    ):

        self.response_engine = engine



    def connect_memory(
        self,
        memory
    ):

        self.memory = memory



    def connect_tools(
        self,
        tools
    ):

        self.tools = tools



    # ==================================================
    # IDENTIDADE
    # ==================================================


    def identity(self):

        return {

            "name":
                self.name,

            "role":
                self.role,

            "description":
                self.description,

            "tone":
                self.tone,

            "traits":
                self.traits

        }



    # ==================================================
    # CONTEXTO COGNITIVO
    # ==================================================


    def build_context(
        self,
        message
    ):

        """
        Cria o contexto enviado
        ao Response Engine.

        Cada persona pode sobrescrever.
        """


        return {


            "persona":
                self.name,


            "role":
                self.role,


            "tone":
                self.tone,


            "traits":
                self.traits,


            "rules":
                self.rules,


            "message":
                message

        }



    # ==================================================
    # PROCESSAMENTO
    # ==================================================


    def respond(
        self,
        message
    ):
        """
        Gera resposta utilizando o Response Engine conectado.
        Levanta exceção caso o motor não esteja acoplado.
        """
        if not self.response_engine:
            raise RuntimeError(
                f"Erro na Persona '{self.name}': "
                "Response Engine não foi conectado ao ciclo cognitivo."
            )

        context = self.build_context(
            message
        )

        return self.response_engine.generate(
            context
        )



    # ==================================================
    # FERRAMENTAS
    # ==================================================


    def can_use(
        self,
        capability
    ):

        return (
            capability
            in self.capabilities
        )



    # ==================================================
    # MEMÓRIA
    # ==================================================


    def remember(
        self,
        data
    ):

        if self.memory:

            self.memory.store(
                {
                    "persona":
                        self.name,

                    "data":
                        data,

                    "time":
                        datetime.now()
                        .isoformat()
                }
            )



    # ==================================================
    # SERIALIZAÇÃO
    # ==================================================


    def to_dict(self):

        return {

            "name":
                self.name,

            "role":
                self.role,

            "description":
                self.description,

            "tone":
                self.tone,

            "traits":
                self.traits,

            "rules":
                self.rules,

            "capabilities":
                self.capabilities,

            "created_at":
                self.created_at

        }



    def save(
        self,
        path
    ):

        """
        Salva configuração
        da persona em JSON.
        """


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.to_dict(),
                file,
                indent=4,
                ensure_ascii=False
            )



    # ==================================================
    # REPRESENTAÇÃO
    # ==================================================


    def __str__(self):

        return (
            f"{self.name} - "
            f"{self.role}"
        )



    def info(self):

        return self.to_dict()