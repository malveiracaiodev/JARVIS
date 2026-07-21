"""
=========================================
GENESIS CORE

Arquivo:
core/agents/agent.py

Descrição:
Classe base universal para agentes
inteligentes do Genesis Core.

Responsável por:
- Ciclo de vida
- Identidade
- Memória local
- Comunicação
- Integração cognitiva

A inteligência é delegada para:
- ResponseEngine
- PersonalityEngine
- Mind
- ToolManager

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from core.base.module import (
    Module,
    ModuleStatus
)


class Agent(Module):
    """
    Classe base de agentes do Genesis Core.

    Exemplos:
    - Jarvis
    - Rafiki
    - Vision
    - Programmer
    """

    def __init__(
        self,
        name: str,
        personality: Optional[Dict[str, Any]] = None,
        description: str = "",
        capabilities: Optional[List[str]] = None
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            version="3.1",
            tags=[
                "agent",
                "cognitive"
            ],
            capabilities=capabilities or []
        )

        # =========================================
        # IDENTIDADE
        # =========================================
        self.personality: Dict[str, Any] = personality or {}
        self.identity: Dict[str, Any] = {}

        # =========================================
        # MEMÓRIA
        # =========================================
        self.memory: deque = deque(maxlen=500)

        # =========================================
        # SISTEMAS CONECTADOS
        # =========================================
        self.mind: Optional[Any] = None
        self.memory_manager: Optional[Any] = None
        self.event_bus: Optional[Any] = None

        # Inteligência compartilhada
        self.response_engine: Optional[Any] = None
        self.personality_engine: Optional[Any] = None
        self.tool_manager: Optional[Any] = None
        self.research_engine: Optional[Any] = None

        # =========================================
        # CONTROLE
        # =========================================
        self._agent_lock = threading.RLock()

    # =========================================
    # CICLO DE VIDA
    # =========================================

    def initialize(self) -> None:
        """Inicializa o agente de forma segura utilizando bloqueio de thread."""
        with self._agent_lock:
            self.set_status(ModuleStatus.INITIALIZING)
            self.on_start()
            self.set_status(ModuleStatus.ONLINE)

    def shutdown(self) -> None:
        """Encerra o agente de forma segura."""
        with self._agent_lock:
            self.on_stop()
            self.set_status(ModuleStatus.OFFLINE)

    # =========================================
    # CONEXÕES
    # =========================================

    def connect_mind(self, mind: Any) -> None:
        """Conecta o módulo Mind ao agente."""
        self.mind = mind

    def connect_memory(self, memory: Any) -> None:
        """Conecta o gerenciador de memória persistente ao agente."""
        self.memory_manager = memory

    def connect_event_bus(self, event_bus: Any) -> None:
        """Conecta o barramento de eventos (EventBus)."""
        self.event_bus = event_bus

    def connect_intelligence(
        self,
        response_engine: Optional[Any] = None,
        personality_engine: Optional[Any] = None,
        research_engine: Optional[Any] = None
    ) -> None:
        """Configura os motores de inteligência e resposta compartilhados."""
        if response_engine is not None:
            self.response_engine = response_engine
        if personality_engine is not None:
            self.personality_engine = personality_engine
        if research_engine is not None:
            self.research_engine = research_engine

    def connect_tools(self, tool_manager: Any) -> None:
        """Conecta o gerenciador de ferramentas ao agente."""
        self.tool_manager = tool_manager

    # =========================================
    # RECEBER MENSAGEM
    # =========================================

    def receive(self, message: Any) -> Union[str, Any]:
        """Processa a recepção de uma mensagem, gravando histórico e acionando pensamento."""
        with self._agent_lock:
            self.remember({
                "type": "input",
                "content": message
            })

            try:
                self.on_message(message)
                return self.think(message)

            except Exception as error:
                error_str = str(error)
                self.set_error(error_str)
                return f"Erro cognitivo: {error_str}"

    # =========================================
    # PENSAMENTO
    # =========================================

    def think(self, message: Any) -> Union[str, Any]:
        """
        Gera a linha de raciocínio ou resposta.
        Delegado primariamente ao ResponseEngine se conectado.
        """
        if self.response_engine and hasattr(self.response_engine, "generate"):
            return self.response_engine.generate(
                message,
                persona=self.personality,
                agent=self.name
            )

        return f"{self.name}: Núcleo cognitivo ativo."

    # =========================================
    # EXECUÇÃO
    # =========================================

    def execute(self, command: Any) -> Any:
        """Executa um comando ou ferramenta através do ToolManager conectado."""
        if self.tool_manager and hasattr(self.tool_manager, "execute"):
            return self.tool_manager.execute(command)

        return None

    # =========================================
    # MEMÓRIA
    # =========================================

    def remember(self, data: Any) -> None:
        """Armazena um registro no deque de memória local do agente."""
        with self._agent_lock:
            self.memory.append({
                "data": data,
                "time": datetime.now().isoformat()
            })

    def recall(self) -> List[Dict[str, Any]]:
        """Retorna uma cópia da lista de memórias locais armazenadas."""
        with self._agent_lock:
            return list(self.memory)

    # =========================================
    # EVENTOS
    # =========================================

    def on_start(self) -> None:
        """Hook executado na inicialização do agente."""
        pass

    def on_stop(self) -> None:
        """Hook executado no encerramento do agente."""
        pass

    def on_message(self, message: Any) -> None:
        """Hook executado ao receber mensagens."""
        pass

    # =========================================
    # SAÍDA
    # =========================================

    def speak(self, text: str) -> None:
        """Exibe a fala formatada do agente na saída padrão."""
        print(f"[{self.name.upper()}] -> {text}")

    # =========================================
    # INFORMAÇÕES
    # =========================================

    def info(self) -> Dict[str, Any]:
        """Retorna um dicionário atualizado com os metadados de status e saúde do agente."""
        data = super().info()

        with self._agent_lock:
            memory_len = len(self.memory)

        data.update({
            "personality": self.personality,
            "memory_size": memory_len,
            "mind_connected": self.mind is not None,
            "response_engine": self.response_engine is not None
        })

        return data