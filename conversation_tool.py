"""
=========================================
GENESIS CORE

Arquivo:
conversation_tool.py

Descrição:
Tool de conversação corrigida para extrair 
o texto correto do comando e garantir a 
resposta limpa e humanizada da persona.

Arquitetura:
Genesis Core

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

from core.interfaces.tool_interface import ToolInterface
from core.runtime.component_state import ComponentState
from personas.persona_factory import PersonaFactory

class ConversationTool(ToolInterface):
    """
    Tool principal para gerenciar os diálogos do JARV.IS 
    com autonomia, identidade e personalidade dinâmicas.
    """
    def __init__(self):
        self._name = "conversation"
        self._description = "Gerencia conversas e respostas autônomas do JARV.IS."
        self.version = "1.0"
        self._status = ComponentState.ONLINE
        
        try:
            self.persona = PersonaFactory.get_persona("jarvis")
        except Exception:
            self.persona = None

    def name(self) -> str:
        return self._name

    def description(self) -> str:
        return self._description

    def permissions(self) -> list:
        return ["execute"]

    def status(self):
        return self._status

    def validate(self, action) -> bool:
        return True

    def execute(self, action, context=None):
        text = ""
        if isinstance(action, dict):
            text = action.get("command", action.get("input", action.get("prompt", action.get("message", ""))))
            if not text and context and hasattr(context, "thought"):
                text = getattr(context.thought, "message", "")
        else:
            text = str(action)

        if not text and context and isinstance(context, dict):
            text = context.get("prompt", context.get("message", ""))

        if not text or text.strip() == "":
            text = "Olá"

        # Tenta invocar a persona diretamente
        if self.persona:
            for method_name in ["generate_response", "respond", "think", "process"]:
                if hasattr(self.persona, method_name):
                    try:
                        method = getattr(self.persona, method_name)
                        result = method(text)
                        if result:
                            return str(result)
                    except Exception:
                        continue

        return f"Sistemas operando e processando diretriz com autonomia: '{text}'. Aguardando novas instruções, Senhor."