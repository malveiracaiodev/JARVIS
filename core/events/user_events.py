"""
=========================================
JARVIS CORE

Arquivo:
user_events.py

Descrição:
Tópicos de eventos acionados por interações diretas e mutações do usuário.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserEvents:
    """
    Eventos de persistência, perfil e autenticação do usuário.
    """
    CREATED: str = "user.created"
    LOADED: str = "user.loaded"
    UPDATED: str = "user.updated"
    LOGIN: str = "user.login"
    LOGOUT: str = "user.logout"
    SAVED: str = "user.saved"