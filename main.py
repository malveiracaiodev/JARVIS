"""
=========================================
JARVIS CORE

Arquivo:
main.py

Descrição:
Ponto de entrada do JARVIS.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""

from core.kernel import Kernel


def main():
    """
    Ponto de entrada da aplicação.
    """

    jarvis = Kernel()
    jarvis.boot()


if __name__ == "__main__":
    main()