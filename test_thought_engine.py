"""
=========================================
GENESIS CORE - TESTE UNITÁRIO DO THOUGHT ENGINE

Arquivo: test_thought_engine.py
Descrição: Testes unitários para o controlador do ciclo cognitivo (Mark V).
Mark: V - Evolution / Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

import unittest
from core.cognitive.thought_engine import ThoughtEngine
from core.models.thought import Thought


class MockPipeline:
    """Mock da Pipeline Cognitiva para testes unitários."""
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def process(self, thought: Thought):
        if self.should_fail:
            raise RuntimeError("Erro simulado na pipeline.")
        
        class MockContext:
            def summary(self):
                return {"status": "success_mock"}
        return MockContext()


class MockEventBus:
    """Mock do EventBus para testes de emissão de eventos."""
    def __init__(self):
        self.events = []

    def emit(self, event_name, data):
        self.events.append((event_name, data))


class TestThoughtEngine(unittest.TestCase):
    """
    Suíte de testes unitários do ThoughtEngine.
    """

    def setUp(self):
        self.event_bus = MockEventBus()
        self.pipeline = MockPipeline()
        self.engine = ThoughtEngine(event_bus=self.event_bus, pipeline=self.pipeline)

    def test_thought_creation(self):
        """Valida se o thought é criado e registrado corretamente nos ativos."""
        thought = self.engine.create("Teste de criação", agent="jarvis", source="user")
        
        self.assertIsNotNone(thought)
        self.assertEqual(thought.message, "Teste de criação")
        self.assertEqual(len(self.engine.get_active()), 1)
        self.assertEqual(self.engine.created, 1)
        
        # Verifica se o evento foi emitido
        event_names = [e[0] for e in self.event_bus.events]
        self.assertIn("THOUGHT_CREATED", event_names)

    def test_think_success_cycle(self):
        """Valida o ciclo completo de pensamento com sucesso."""
        thought = self.engine.think("Executar ciclo de pensamento", agent="jarvis", source="user")

        self.assertTrue(thought.is_finished())
        self.assertEqual(self.engine.completed, 1)
        self.assertEqual(self.engine.failed_count, 0)
        self.assertEqual(len(self.engine.get_history()), 1)
        self.assertEqual(len(self.engine.get_active()), 0)

        # Verifica eventos do ciclo
        event_names = [e[0] for e in self.event_bus.events]
        self.assertIn("THOUGHT_CREATED", event_names)
        self.assertIn("THOUGHT_STARTED", event_names)
        self.assertIn("THOUGHT_COMPLETED", event_names)

    def test_think_pipeline_failure(self):
        """Valida o tratamento de falha quando a pipeline gera erro."""
        self.engine.pipeline = MockPipeline(should_fail=True)
        thought = self.engine.think("Falhar na pipeline", agent="jarvis", source="user")

        self.assertTrue(thought.is_finished())
        self.assertEqual(self.engine.completed, 0)
        self.assertEqual(self.engine.failed_count, 1)
        self.assertEqual(len(self.engine.get_history()), 1)

        event_names = [e[0] for e in self.event_bus.events]
        self.assertIn("THOUGHT_FAILED", event_names)

    def test_metrics_and_status(self):
        """Valida a geração de métricas e status do motor."""
        self.engine.think("Métrica teste 1")
        
        metrics = self.engine.metrics()
        self.assertEqual(metrics["created"], 1)
        self.assertEqual(metrics["completed"], 1)
        self.assertEqual(metrics["success_rate"], 1.0)

        status = self.engine.status()
        self.assertEqual(status["name"], "ThoughtEngine")
        self.assertTrue(status["pipeline"])


if __name__ == "__main__":
    unittest.main()