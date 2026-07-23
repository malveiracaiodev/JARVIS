"""
=========================================
GENESIS CORE

Arquivo:
core/ai/ai_router.py

Descrição:
Sistema de roteamento cognitivo da camada IA.

Responsável por decidir o fluxo:

Entrada
   |
   v
AIRouter
   |
   +--> Thought Engine
   |
   +--> Tool Execution
   |
   +--> Memory
   |
   +--> Provider IA


Arquitetura:
Genesis Core

Mark:
V - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from __future__ import annotations


from dataclasses import dataclass, field
from typing import Any





@dataclass(slots=True)
class RouteDecision:
    """
    Resultado de uma decisão de roteamento.
    """


    route: str

    confidence: float

    reason: str

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    def to_dict(self):

        return {

            "route":
                self.route,

            "confidence":
                self.confidence,

            "reason":
                self.reason,

            "metadata":
                self.metadata

        }





class AIRouter:
    """
    Roteador cognitivo do Genesis.

    Decide qual núcleo deve processar
    uma entrada.
    """



    VALID_ROUTES = {

        "chat",

        "mind",

        "command",

        "memory",

        "tool"

    }



    def __init__(self):


        self.rules = {


            "command": [

                "execute",

                "executar",

                "abrir",

                "fechar",

                "iniciar",

                "rodar",

                "criar arquivo",

                "apagar",

                "instalar"

            ],



            "mind": [

                "planeje",

                "analise",

                "pense",

                "decida",

                "estratégia",

                "estrategia",

                "resolva",

                "crie plano"

            ],



            "memory": [

                "lembra",

                "lembrar",

                "memória",

                "memoria",

                "recorde",

                "salve"

            ],



            "tool": [

                "pesquise",

                "procure",

                "busque",

                "execute ferramenta",

                "use ferramenta"

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



        self.priority = [

            "command",

            "tool",

            "memory",

            "mind",

            "chat"

        ]





    # =====================================================
    # ROUTE PRINCIPAL
    # =====================================================


    def route(
        self,
        prompt: str,
        context=None
    ) -> dict:


        if not prompt:


            return RouteDecision(

                route="chat",

                confidence=0.0,

                reason="empty_input"

            ).to_dict()



        text = (

            prompt

            .lower()

            .strip()

        )



        # contexto influencia decisão

        if context:


            if getattr(
                context,
                "intention",
                None
            ):


                return RouteDecision(

                    route=context.intention,

                    confidence=0.95,

                    reason="context_intention"

                ).to_dict()



        matches = {}



        for category, words in self.rules.items():


            score = 0



            for word in words:


                if word in text:

                    score += 1



            if score:


                matches[category] = score





        if matches:


            selected = max(

                matches,

                key=matches.get

            )



            confidence = min(

                0.5 +

                (
                    matches[selected]
                    *
                    0.15
                ),

                0.99

            )



            return RouteDecision(

                route=selected,

                confidence=confidence,

                reason="keyword_match",

                metadata={

                    "matches":
                        matches

                }

            ).to_dict()





        return RouteDecision(

            route="chat",

            confidence=0.5,

            reason="default"

        ).to_dict()





    # =====================================================
    # REGRAS DINÂMICAS
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





    def remove_rule(
        self,
        category: str,
        keyword: str
    ):


        if category in self.rules:


            if keyword.lower() in self.rules[category]:


                self.rules[category].remove(

                    keyword.lower()

                )





    # =====================================================
    # STATUS
    # =====================================================


    def status(self):


        return {


            "routes":

                list(
                    self.rules.keys()
                ),


            "rules":

                self.rules,


            "priority":

                self.priority

        }