"""
=========================================
GENESIS CORE - PIPELINE INITIALIZER

Arquivo: core/pipeline/pipeline_initializer.py
Descrição: Construtor estruturado e integrado da Pipeline Cognitiva com suporte completo à Memória de Longo Prazo e Malha Neural (Mark V).
Mark: V - Evolution / Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from typing import List, Any, Optional
from core.cognitive.parser import Parser
from core.cognitive.planner import Planner
from core.cognitive.reasoner import Reasoner
from core.cognitive.executor import Executor
from core.cognitive.reflection import Reflection
from core.pipeline.cognitive_pipeline import CognitivePipeline
from core.pipeline.steps.memory_step import MemoryIntegrationStep
from core.tools import SystemTestTool


class PipelineInitializer:
    """
    Montador da infraestrutura e injeção de dependências do fluxo Thought Engine (Mark V - Evolution).
    """
    def __init__(
        self,
        logger: Optional[Any] = None,
        tool_manager: Optional[Any] = None,
        memory: Optional[Any] = None
    ) -> None:
        self.logger: Optional[Any] = logger
        self.tool_manager: Optional[Any] = tool_manager
        self.memory: Optional[Any] = memory
        self.pipeline: Optional[CognitivePipeline] = None
        self.steps: List[Any] = []

    def build(self) -> CognitivePipeline:
        if self.pipeline:
            self._log("info", "Pipeline já inicializada.")
            return self.pipeline

        if self.tool_manager is None:
            raise RuntimeError("Pipeline Cognitiva requer ToolManager válido.")

        self._log("info", "Construindo Thought Engine (Mark V - Evolution) com Memória e Malha Neural.")
        self._register_default_tools()

        pipeline = CognitivePipeline()
        
        # Sequência oficial da malha cognitiva Mark V:
        # 1. Parser: Compreensão inicial do input
        # 2. Planner: Estratégia de decomposição
        # 3. Reasoner: Raciocínio contextualizado com injeção de memória
        # 4. Executor: Execução de ferramentas via ToolManager
        # 5. Reflection: Crítica e refinamento do resultado
        # 6. MemoryIntegrationStep: Persistência automática do pensamento finalizado na memória de longo prazo
        self.steps = [
            Parser(logger=self.logger),
            Planner(logger=self.logger),
            Reasoner(logger=self.logger, memory=self.memory),
            Executor(tool_manager=self.tool_manager, logger=self.logger),
            Reflection(logger=self.logger, memory=self.memory),
            MemoryIntegrationStep(memory_provider=self.memory)
        ]

        for step in self.steps:
            pipeline.add_step(step)
            self._log("info", f"Etapa registrada na malha: {self._step_name(step)}")

        pipeline.initialize()
        self.pipeline = pipeline
        self._log("success", "Thought Engine Mark V construída e integrada com sucesso.")
        return pipeline

    def _step_name(self, step: Any) -> str:
        name = getattr(step, "name", None)
        if callable(name):
            return name()
        if name:
            return str(name)
        return step.__class__.__name__.lower()

    def _register_default_tools(self) -> None:
        try:
            existing = self.tool_manager.list_tools()
        except Exception:
            existing = []

        if "system_test" not in existing:
            self.tool_manager.register(SystemTestTool())
            self._log("info", "Ferramenta registrada: system_test")

    def get_pipeline(self) -> Optional[CognitivePipeline]:
        return self.pipeline

    def get_steps(self) -> List[str]:
        return [self._step_name(step) for step in self.steps]

    def reset(self) -> None:
        if self.pipeline:
            self.pipeline.shutdown()
        self.pipeline = None
        self.steps.clear()

    def _log(self, level: str, message: str) -> None:
        if self.logger:
            method = getattr(self.logger, level, None)
            if callable(method):
                method(message)
                return
        print(f"[PIPELINE:{level.upper()}] {message}")