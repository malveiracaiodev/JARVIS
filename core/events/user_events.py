"""
=========================================
GENESIS CORE - USER INTERACTION EVENTS

Arquivo: core/events/user_events.py
Descrição: Eventos de interação, sessões e perfil do usuário humano.
Mark: IV - Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserEvents:
    """
    Barramento de eventos do usuário. Mapeia mudanças da entidade humana.
    """

    # Perfil
    CREATED: str = "user.created"
    LOADED: str = "user.loaded"
    UPDATED: str = "user.updated"
    SAVED: str = "user.saved"
    DELETED: str = "user.deleted"

    # Sessão
    SESSION_STARTED: str = "user.session.started"
    SESSION_ENDED: str = "user.session.ended"
    LOGIN: str = "user.login"
    LOGOUT: str = "user.logout"

    # Interação
    INPUT_RECEIVED: str = "user.input.received"
    COMMAND_SENT: str = "user.command.sent"
    REQUEST_CREATED: str = "user.request.created"
    RESPONSE_RECEIVED: str = "user.response.received"

    # Preferências
    PREFERENCE_CREATED: str = "user.preference.created"
    PREFERENCE_UPDATED: str = "user.preference.updated"
    PREFERENCE_REMOVED: str = "user.preference.removed"

    # Aprendizado
    BEHAVIOR_LEARNED: str = "user.behavior.learned"
    CONTEXT_UPDATED: str = "user.context.updated"
    FEEDBACK_GIVEN: str = "user.feedback.given"

    # Permissões
    PERMISSION_GRANTED: str = "user.permission.granted"
    PERMISSION_REVOKED: str = "user.permission.revoked"

    # Segurança
    AUTHENTICATION_FAILED: str = "user.authentication.failed"
    SECURITY_ALERT: str = "user.security.alert"