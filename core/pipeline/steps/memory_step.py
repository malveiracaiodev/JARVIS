"""
=========================================
GENESIS CORE - LONG-TERM MEMORY STEP

Arquivo: core/pipeline/steps/memory_step.py
Descrição: Etapa da Pipeline Cognitiva responsável por persistir o Thought na Memória de Longo Prazo (Mark V).
Mark: V - Evolution / Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from typing import Any, Optional
from core.pipeline.pipeline_step import PipelineStep
from core.pipeline.pipeline_context import PipelineContext


class MemoryIntegrationStep(PipelineStep):
    """
    Etapa da malha neural responsável por salvar o resultado do pensamento na memória de longo prazo.
    """
    def __init__(self, memory_provider: Optional[Any] = None, name: str = "memory_integration"):
        super().__init__(name)
        self.memory_provider = memory_provider

    def process(self, context: PipelineContext) -> PipelineContext:
        """
        Método padrão exigido pela PipelineStep da malha cognitiva.
        """
        return self.run(context)

    def run(self, context: PipelineContext) -> PipelineContext:
        """
        Executa a persistência do thought concluído/processado na memória de longo prazo.
        """
        thought = context.get_thought()
        if not thought:
            context.add_error("MemoryIntegrationStep: Nenhum Thought encontrado no contexto.")
            return context

        # Obtém o provedor de memória do contexto se não foi injetado diretamente no construtor
        memory = self.memory_provider or getattr(context, "memory", None)

        if not memory:
            return context

        try:
            memory_payload = {
                "id": thought.id,
                "message": thought.message,
                "agent": getattr(thought, "agent", "jarvis"),
                "source": getattr(thought, "source", "user"),
                "metadata": thought.metadata,
                "result": getattr(thought, "result", None)
            }

            if hasattr(memory, "save"):
                memory.save(memory_payload)
            elif hasattr(memory, "store"):
                memory.store(memory_payload)
            elif hasattr(memory, "add"):
                memory.add(memory_payload)
            else:
                context.add_error("MemoryIntegrationStep: Provedor de memória não possui método de salvamento compatível.")

        except Exception as error:
            context.add_error(f"MemoryIntegrationStep erro ao persistir na memória: {str(error)}")

        return context