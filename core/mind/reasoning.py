"""
=========================================
JARVIS CORE

Arquivo:
reasoning.py

Descrição:
Sistema de raciocínio e análise.

Responsável por:
- Interpretar informações
- Avaliar situações
- Criar planos
- Tomar decisões
- Coordenar estratégias

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime


class Reasoning:
    """
    Motor de raciocínio do JARVIS.

    Recebe informações do Brain e
    produz uma resposta lógica.
    """

    def __init__(self):

        self.name = "Reasoning Engine"

        self.version = "Mark II"

        self.status = "offline"

        self.history = []

    # ==========================================================
    # Ciclo de vida
    # ==========================================================

    def initialize(self):

        self.status = "online"

        print("[REASONING] Motor iniciado")

    def shutdown(self):

        self.status = "offline"

        print("[REASONING] Motor encerrado")

    # ==========================================================
    # Processamento
    # ==========================================================

    def analyze(
        self,
        input_text,
        context=None
    ):

        analysis = {

            "timestamp": datetime.now().isoformat(),

            "input": input_text,

            "context": context

        }

        self.history.append(analysis)

        return self.generate_response(
            input_text,
            context
        )

    # ==========================================================
    # Geração de resposta
    # ==========================================================

    def generate_response(
        self,
        input_text,
        context
    ):

        text = input_text.lower()

        # -------------------------
        # Organização
        # -------------------------

        if "como" in text:

            return (
                "Vou analisar o problema considerando o contexto, "
                "os objetivos disponíveis e possíveis estratégias."
            )

        # -------------------------
        # Decisão
        # -------------------------

        if (
            "devo" in text
            or "vale a pena" in text
            or "compensa" in text
        ):

            return (
                "Vou comparar vantagens, riscos e consequências "
                "antes de recomendar uma decisão."
            )

        # -------------------------
        # Planejamento
        # -------------------------

        if (
            "planejar" in text
            or "plano" in text
            or "organizar" in text
        ):

            plan = self.create_plan(input_text)

            return (
                "Plano inicial:\n\n- "
                + "\n- ".join(plan["steps"])
            )

        # -------------------------
        # Conhecimento
        # -------------------------

        if context:

            knowledge = context.get("knowledge")

            if knowledge:

                first = knowledge[0]

                return str(
                    first.get(
                        "information",
                        "Conhecimento encontrado."
                    )
                )

        # -------------------------
        # Padrão
        # -------------------------

        return (
            "Analisei sua solicitação. "
            "Ainda preciso de mais informações "
            "para produzir uma resposta mais completa."
        )

    # ==========================================================
    # Planejamento
    # ==========================================================

    def create_plan(
        self,
        objective
    ):

        return {

            "objective": objective,

            "steps": [

                "Entender o objetivo",

                "Levantar informações",

                "Definir estratégia",

                "Executar ações",

                "Avaliar resultados"

            ]

        }

    # ==========================================================
    # Diagnóstico
    # ==========================================================

    def last_analysis(self):

        if not self.history:

            return None

        return self.history[-1]

    def clear_history(self):

        self.history.clear()

    def status_report(self):

        return {

            "name": self.name,

            "version": self.version,

            "status": self.status,

            "analyses": len(self.history)

        }