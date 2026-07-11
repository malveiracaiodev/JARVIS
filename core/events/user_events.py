"""
=========================================
JARVIS CORE

Arquivo:
user_events.py

Descrição:
Eventos relacionados ao usuário.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


class UserEvents:
    """
    Eventos do usuário.
    """

    CREATED = "user.created"

    LOADED = "user.loaded"

    UPDATED = "user.updated"

    LOGIN = "user.login"

    LOGOUT = "user.logout"

    SAVED = "user.saved"