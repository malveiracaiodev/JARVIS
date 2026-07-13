"""
=========================================
JARVIS CORE

Arquivo:
rafiki.py

Descrição:
Agente de aconselhamento, reflexão estratégica e apoio analítico.

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from core.agents.agent import Agent


class RafikiAgent(Agent):
    """
    Agente analítico focado em tomadas de decisão e mentoria de processos.
    """

    def __init__(self):
        super().__init__(
            name="RAFIKI",
            personality="advisor"
        )

    def think(self, message):
        cmd = message.lower().strip()

        if "decisão" in cmd or "decidir" in cmd:
            return "Uma escolha estratégica exige peso. Antes de avançarmos, listaremos as variáveis limitantes, os riscos de execução e o impacto colateral no Core."

        if "problema" in cmd:
            return "O ruído na execução geralmente é um sintoma, não a causa. Vamos mapear o ponto exato onde o fluxo divergiu do esperado."

        if "conselho" in cmd:
            return "Para obtermos clareza analítica, afaste as urgências imediatas. Qual é o objetivo de longo prazo deste módulo?"

        return "Reflexão capturada. Processando alternativas sob a perspectiva de arquitetura e consistência."