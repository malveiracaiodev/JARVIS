"""
=========================================
JARVIS CORE

Arquivo:
jarvis.py

Descrição:
Agente principal de suporte técnico e operações.

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from core.agents.agent import Agent


class JarvisAgent(Agent):
    """
    Agente operacional técnico central do ecossistema.
    """

    def __init__(self):
        super().__init__(
            name="JARVIS",
            personality="technical"
        )

    def think(self, message):
        cmd = message.lower().strip()

        if "status" in cmd:
            return "Todos os módulos centrais estão estabilizados e aguardando telemetria operacional."

        if "ajuda" in cmd:
            return "Estou à disposição para coordenar diagnósticos, gerenciar tarefas concorrentes e inspecionar o core."

        return "Comando operacional aceito. Integrando dados e preparando execução."