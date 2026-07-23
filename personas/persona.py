"""
=========================================
GENESIS CORE

Arquivo:
personas/persona.py

Descrição:
Classe base universal de identidade
cognitiva do Genesis Core.

Responsável por:

- Identidade
- Personalidade
- Regras
- Contexto
- Memória
- Capacidades

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""


from datetime import datetime
from typing import Any
import json



class Persona:


    def __init__(
        self,
        name: str,
        role: str,
        description: str = "",
        tone: str = "neutral",
        traits=None,
        rules=None,
        capabilities=None,
        system_prompt: str = "",
        metadata=None
    ):


        # ==============================
        # IDENTIDADE
        # ==============================

        self.name = name

        self.role = role

        self.description = description


        # ==============================
        # PERSONALIDADE
        # ==============================

        self.tone = tone

        self.traits = traits or []

        self.rules = rules or []


        # ==============================
        # IA CONTEXTO
        # ==============================

        self.system_prompt = system_prompt


        # ==============================
        # CAPACIDADES
        # ==============================

        self.capabilities = capabilities or []


        # ==============================
        # METADATA
        # ==============================

        self.metadata = metadata or {

            "version": "1.0",

            "type": "persona"

        }


        # ==============================
        # SERVIÇOS
        # ==============================

        self.memory = None

        self.tools = None

        self.ai_manager = None



        # ==============================
        # ESTADO
        # ==============================

        self.created_at = (
            datetime.now()
            .isoformat()
        )



    # ==================================
    # CONEXÕES
    # ==================================


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



    def connect_ai(
        self,
        manager
    ):

        self.ai_manager = manager



    # ==================================
    # IDENTIDADE
    # ==================================


    def identity(self):

        return {

            "name":
                self.name,


            "role":
                self.role,


            "description":
                self.description,


            "metadata":
                self.metadata

        }



    # ==================================
    # CONTEXTO PARA IA
    # ==================================


    def build_context(
        self,
        message: str
    ):


        return {


            "persona":

                self.name,



            "system_prompt":

                self.system_prompt,



            "role":

                self.role,



            "tone":

                self.tone,



            "traits":

                self.traits,



            "rules":

                self.rules,



            "capabilities":

                self.capabilities,



            "message":

                message

        }



    # ==================================
    # CAPACIDADES
    # ==================================


    def can_use(
        self,
        capability: str
    ):

        return capability in self.capabilities



    # ==================================
    # MEMÓRIA
    # ==================================


    def remember(
        self,
        data: Any
    ):


        if not self.memory:

            return False



        return self.memory.store(

            {

                "persona":

                    self.name,


                "data":

                    data,


                "timestamp":

                    datetime.now()
                    .isoformat()

            },


            memory_type="long_term"

        )



    # ==================================
    # SERIALIZAÇÃO
    # ==================================


    def to_dict(self):

        return {


            "name":

                self.name,


            "role":

                self.role,


            "description":

                self.description,


            "system_prompt":

                self.system_prompt,


            "tone":

                self.tone,


            "traits":

                self.traits,


            "rules":

                self.rules,


            "capabilities":

                self.capabilities,


            "metadata":

                self.metadata,


            "created_at":

                self.created_at

        }



    def save(
        self,
        path
    ):


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



    def info(self):

        return self.to_dict()



    def __str__(self):

        return (
            f"{self.name} - {self.role}"
        )