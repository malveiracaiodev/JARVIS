"""
=========================================
GENESIS CORE

Arquivo:
core/intelligence/response_engine.py

Descrição:
Motor responsável pela geração de respostas
do Genesis Core.

Responsabilidades:

- Construção de respostas cognitivas.
- Aplicação de personalidade.
- Preparação para LLM.
- Controle de confiança.
- Histórico conversacional.

Arquitetura:

Thought
    ↓
Reasoner
    ↓
Response Engine
    ↓
Persona
    ↓
User

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
import threading


class ResponseEngine:
    """
    Núcleo responsável por transformar
    processamento cognitivo em comunicação.
    """

    def __init__(self):
        self.name = "Response Engine"
        self.version = "2.0"
        self.enabled = True
        self.history = []
        self._lock = threading.RLock()

    # ==================================================
    # INFORMAÇÕES
    # ==================================================

    def get_name(self):
        return self.name

    def get_status(self):
        return "ONLINE" if self.enabled else "OFFLINE"

    # ==================================================
    # GERAÇÃO
    # ==================================================

    def generate(
        self,
        message,
        personality=None,
        context=None,
        thought=None
    ):
        with self._lock:
            if not self.enabled:
                return self._error(
                    "Response Engine offline."
                )

            style = self.get_personality_style(
                personality
            )

            response = self.compose(
                message,
                style,
                context,
                thought
            )

            result = {
                "response":
                    response,
                "engine":
                    self.name,
                "version":
                    self.version,
                "timestamp":
                    datetime.now()
                    .isoformat(),
                "confidence":
                    self.calculate_confidence(
                        thought,
                        context
                    )
            }

            self.history.append(
                result
            )

            return result

    # ==================================================
    # COMPOSIÇÃO
    # ==================================================

    def compose(
        self,
        message,
        style,
        context=None,
        thought=None
    ):
        response = []

        if style:
            response.append(
                style
            )

        if thought:
            response.append(
                str(thought)
            )
        else:
            response.append(
                "Analisando sua solicitação."
            )

        response.append(
            message
        )

        return "\n\n".join(
            response
        )

    # ==================================================
    # PERSONALIDADE
    # ==================================================

    def get_personality_style(
        self,
        personality
    ):
        if personality is None:
            return (
                "Genesis Core em modo neutro."
            )

        if hasattr(
            personality,
            "tone"
        ):
            return (
                f"Tom: "
                f"{personality.tone}"
            )

        if isinstance(
            personality,
            dict
        ):
            return (
                f"Tom: "
                f"{personality.get('tone','neutro')}"
            )

        return str(
            personality
        )

    # ==================================================
    # CONFIANÇA
    # ==================================================

    def calculate_confidence(
        self,
        thought=None,
        context=None
    ):
        confidence = 0.5

        if thought:
            confidence += 0.2

        if context:
            confidence += 0.1

        return min(
            confidence,
            1.0
        )

    # ==================================================
    # HISTÓRICO
    # ==================================================

    def get_history(self):
        with self._lock:
            return self.history.copy()

    def clear_history(self):
        with self._lock:
            self.history.clear()

    # ==================================================
    # FUTURA IA
    # ==================================================

    def connect_model(
        self,
        model
    ):
        """
        Futuro ponto de conexão:

        GPT
        Gemini
        Ollama
        Modelo local
        """
        self.model = model

    # ==================================================
    # ERROS
    # ==================================================

    def _error(
        self,
        message
    ):
        return {
            "response":
                message,
            "engine":
                self.name,
            "confidence":
                0.0
        }