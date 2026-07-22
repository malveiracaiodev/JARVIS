"""
=========================================
GENESIS CORE

Arquivo:
core/ai/ai_router.py

Descrição:
Sistema responsável pelo roteamento
das requisições de inteligência.

Decide se uma entrada deve:

- passar pelo provider IA
- ir para Thought Engine
- executar comando
- consultar memória

Arquitetura:
Genesis Core

Mark:
V - Evolution
=========================================
"""

from __future__ import annotations


class AIRouter:
    """
    Roteador cognitivo da camada IA.
    """


    def __init__(self):

        self.rules = {

            "command": [
                "execute",
                "executar",
                "abrir",
                "fechar",
                "iniciar",
                "rodar",
            ],


            "mind": [

                "planeje",
                "analise",
                "pense",
                "decida",
                "crie plano",
                "resolva"

            ],


            "chat": [

                "oi",
                "olá",
                "ola",
                "bom dia",
                "boa tarde",
                "boa noite"

            ]

        }



    # =====================================================
    # ROUTE
    # =====================================================


    def route(
        self,
        prompt: str
    ) -> dict:


        text = (
            prompt
            .lower()
            .strip()
        )


        for category, words in self.rules.items():


            for word in words:


                if word in text:


                    return {

                        "route": category,

                        "confidence": 0.9,

                        "reason":
                            f"matched:{word}"

                    }



        return {


            "route":
                "chat",


            "confidence":
                0.5,


            "reason":
                "default"


        }



    # =====================================================
    # REGISTRO DE REGRA
    # =====================================================


    def add_rule(
        self,
        category: str,
        keyword: str
    ):


        if category not in self.rules:

            self.rules[category] = []


        self.rules[category].append(
            keyword.lower()
        )



    # =====================================================
    # STATUS
    # =====================================================


    def status(
        self
    ) -> dict:


        return {

            "rules":
                self.rules,

            "categories":
                list(self.rules.keys())

        }