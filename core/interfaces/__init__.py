"""
=========================================
JARVIS CORE

Pacote:
interfaces

Descrição:
Interfaces de comunicação do JARVIS.

Responsável por disponibilizar os módulos
que permitem interação com o sistema.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""

from .command_interface import CommandInterface

__all__ = [
    "CommandInterface"
]