"""
=========================================
GENESIS CORE

Arquivo:
core/agents/genesis_agent.py

Descrição:
Agente inteligente base do Genesis Core (Mark IV - Neural Lattice).

Responsável por unir:
- Agent
- Persona
- Response Engine
- Memory
- Tools
- Neural Lattice Cognitive Pipeline

Arquitetura:
User
 |
Agent
 |
Persona
 |
Thought Engine / Neural Lattice
 |
Response Engine
 |
Tools

Mark:
IV - Neural Lattice

Autor:
Caio Vitor Malveira
=========================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from core.agents.agent import Agent
from core.runtime.component_state import ComponentState


class GenesisAgent(Agent):
    """
    Agente inteligente universal otimizado para o padrão Mark IV (Neural Lattice).

    Todos os agentes do Genesis (Jarvis, Rafiki, Vision, Programmer, etc.)
    devem herdar desta classe.
    """

    def __init__(
        self,
        name: str,
        persona: Optional[Any] = None,
        description: str = "",
        capabilities: Optional[List[str]] = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            capabilities=capabilities or []
        )

        # =====================================
        # PERSONALIDADE
        # =====================================
        self.persona = persona

        # =====================================
        # INTELIGÊNCIA / NEURAL LATTICE
        # =====================================
        self.response_engine: Optional[Any] = None
        self.pipeline: Optional[Any] = None
        self.tools: Optional[Any] = None
        self.knowledge: Optional[Any] = None

        # =====================================
        # ESTADO
        # =====================================
        self.last_response: Optional[Dict[str, Any]] = None
        self.lattice_state: ComponentState = ComponentState.OFFLINE

    # =========================================
        # CONEXÕES
    # =========================================

    def connect_persona(self, persona: Any) -> None:
        """Conecta ou atualiza a persona do agente."""
        self.persona = persona

    def connect_response_engine(self, engine: Any) -> None:
        """Conecta o motor de resposta e o propaga para a persona."""
        self.response_engine = engine
        if self.persona and hasattr(self.persona, "connect_response_engine"):
            self.persona.connect_response_engine(engine)

    def connect_tools(self, tools: Any) -> None:
        """Conecta o gerenciador de ferramentas (ToolManager)."""
        self.tools = tools
        if self.persona and hasattr(self.persona, "connect_tools"):
            self.persona.connect_tools(tools)

    def connect_memory(self, memory: Any) -> None:
        """Conecta o sistema de memória persistente."""
        super().connect_memory(memory)
        if self.persona and hasattr(self.persona, "connect_memory"):
            self.persona.connect_memory(memory)

    def connect_pipeline(self, pipeline: Any) -> None:
        """Conecta o Thought Engine / Cognitive Pipeline da Neural Lattice."""
        self.pipeline = pipeline
        self.lattice_state = ComponentState.ONLINE

    # =========================================
    # PROCESSAMENTO
    # =========================================

    def think(self, message: str) -> Union[str, Dict[str, Any]]:
        """
        Processa a mensagem do usuário através da Neural Lattice.

        Fluxo inteligente:
        - Se o Pipeline cognitivo estiver ativo, delega o fluxo completo (Parser -> Planner -> Reasoner -> Executor -> Reflection).
        - Se não, recorre ao motor tradicional via Persona/Response Engine.
        """
        if not self.persona:
            return f"{self.name}: Persona não configurada na Neural Lattice."

        try:
            response: Any = None

            # 1. Fluxo Cognitivo Avançado via Pipeline (Thought Engine)
            if self.pipeline and hasattr(self.pipeline, "run"):
                thought_result = self.pipeline.run(message, agent=self.name)
                # Extrai a resposta formatada ou o resultado da execução se disponível
                response = thought_result.get("result") or thought_result

            # 2. Fluxo Padrão via Response Engine / Persona
            elif self.response_engine and hasattr(self.persona, "respond"):
                response = self.persona.respond(message)

            else:
                response = f"{self.name}: Processando informação na malha neural."

            # Registra o histórico da última interação
            self.last_response = {
                "message": message,
                "response": response,
                "time": datetime.now().isoformat()
            }

            # Armazena na memória persistente de forma segura
            if hasattr(self, "remember"):
                self.remember(self.last_response)

            return response

        except Exception as e:
            error_msg = f"Erro no agente da Lattice {self.name}: {e}"
            return error_msg

    # =========================================
    # EXECUÇÃO DE FERRAMENTAS
    # =========================================

    def use_tool(self, tool: str, data: Optional[Any] = None) -> Any:
        """Executa uma ferramenta de forma segura através do ToolManager conectado."""
        if not self.tools:
            return "ToolManager não conectado à Neural Lattice."

        if hasattr(self.tools, "execute"):
            return self.tools.execute(tool, data)

        return None

    # =========================================
    # INFORMAÇÕES
    # =========================================

    def info(self) -> Dict[str, Any]:
        """Retorna o dicionário de status e metadados atualizados do agente."""
        data = super().info()

        data.update({
            "persona": self.persona.name if self.persona and hasattr(self.persona, "name") else str(self.persona),
            "response_engine": self.response_engine is not None,
            "tools": self.tools is not None,
            "pipeline": self.pipeline is not None,
            "lattice_state": str(self.lattice_state)
        })

        return data