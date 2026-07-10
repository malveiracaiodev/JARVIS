"""
=========================================
JARVIS CORE

Arquivo:
user_events.py

Descrição:
Eventos relacionados ao usuário.

Mark:
I - Heartbeat
=========================================
"""


class UserEvents:
    """
    Eventos do usuário.
    """


    COMMAND_RECEIVED = (
        "user.command.received"
    )


    MESSAGE_SENT = (
        "user.message.sent"
    )


    PROFILE_UPDATED = (
        "user.profile.updated"
    )