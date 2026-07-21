"""
=========================================
GENESIS CORE - TESTE DE INTEGRAÇÃO END-TO-END

Arquivo: test_pipeline_integration.py
Descrição: Testes de integração ponta a ponta da Pipeline Cognitiva completa (Mark V).
Mark: V - Evolution / Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

import unittest
from core.cognitive.thought_engine import ThoughtEngine
from core.pipeline.pipeline_initializer import PipelineInitializer


class MockLogger:
    """Mock do Logger para capturar logs durante os testes."""
    def __init__(self):
        self.logs = []

    def info(self, msg):
        self.logs.append(("info", msg))

    def success(self, msg):
        self.logs.append(("success", msg))

    def error(self, msg):
        self.logs.append(("error", msg))


class MockToolManager:
    """Mock do ToolManager."""
    def __init__(self):
        self.tools = {}

    def list_tools(self):
        return list(self.tools.keys())

    def register(self, tool):
        name = getattr(tool, "name", "system_test")
        self.tools[name] = tool


class MockMemoryProvider:
    """Mock do provedor de memória de longo prazo."""
    def __init__(self):
        self.saved_items = []

    def save(self, payload):
        self.saved_items.append(payload)


class TestPipelineIntegration(unittest.TestCase):
    """
    Suíte de testes de integração end-to-end da malha cognitiva Mark V.
    """

    def setUp(self):
        self.logger = MockLogger()
        self.tool_manager = MockToolManager()
        self.memory = MockMemoryProvider()

        # Inicializa e constrói a pipeline completa
        initializer = PipelineInitializer(
            logger=self.logger,
            tool_manager=self.tool_manager,
            memory=self.memory
        )
        self.pipeline = initializer.build()

        # Conecta a pipeline ao ThoughtEngine
        self.engine = ThoughtEngine(
            logger=self.logger,
            pipeline=self.pipeline
        )

    def test_full_cognitive_cycle_integration(self):
        """Valida o fluxo end-to-end de um pensamento passando por todas as etapas da malha."""
        thought = self.engine.think(
            message="Executar diagnóstico completo do sistema",
            agent="jarvis",
            source="user"
        )

        # 1. Valida se o pensamento foi concluído com sucesso
        self.assertTrue(thought.is_finished())
        self.assertEqual(self.engine.completed, 1)
        self.assertEqual(self.engine.failed_count, 0)

        # 2. Valida se a etapa de memória persistiu o thought corretamente
        self.assertGreaterEqual(len(self.memory.saved_items), 1)
        saved_payload = self.memory.saved_items[0]
        self.assertEqual(saved_payload["id"], thought.id)
        self.assertEqual(saved_payload["message"], "Executar diagnóstico completo do sistema")
        self.assertEqual(saved_payload["agent"], "jarvis")

        # 3. Valida se as métricas globais do engine refletem a execução
        metrics = self.engine.metrics()
        self.assertEqual(metrics["created"], 1)
        self.assertEqual(metrics["completed"], 1)
        self.assertEqual(metrics["success_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()