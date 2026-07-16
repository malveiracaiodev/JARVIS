"""Construcao da pipeline cognitiva do Genesis Core."""

from core.cognitive import Executor, Parser, Planner, Reasoner, Reflection
from core.pipeline.cognitive_pipeline import CognitivePipeline
from core.tools import SystemTestTool


class PipelineInitializer:
    """Monta a pipeline e conecta o Executor ao ToolManager central."""

    def __init__(self, logger=None, tool_manager=None):
        self.logger = logger
        self.tool_manager = tool_manager
        self.pipeline = None

    def build(self):
        if self.pipeline:
            self._log("info", "Pipeline ja inicializada.")
            return self.pipeline

        if not self.tool_manager:
            raise RuntimeError("Pipeline Cognitiva requer um ToolManager.")

        self._log("info", "Construindo Pipeline Cognitiva.")

        if "system_test" not in self.tool_manager.list_tools():
            self.tool_manager.register(SystemTestTool())
            self._log("info", "Ferramenta registrada: system_test")

        pipeline = CognitivePipeline()
        steps = [
            Parser(),
            Planner(),
            Reasoner(),
            Executor(tool_manager=self.tool_manager),
            Reflection(),
        ]

        for step in steps:
            pipeline.add_step(step)
            self._log("info", f"Etapa registrada: {step.name}")

        self.pipeline = pipeline
        self._log("success", "Pipeline Cognitiva construida.")
        return pipeline

    def get_pipeline(self):
        return self.pipeline

    def reset(self):
        self.pipeline = None

    def _log(self, level, message):
        if self.logger:
            method = getattr(self.logger, level, None)
            if method:
                method(message)
                return

        print(f"[PIPELINE:{level.upper()}] {message}")
