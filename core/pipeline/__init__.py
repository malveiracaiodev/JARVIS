"""
=========================================
GENESIS CORE - COGNITIVE PIPELINE PACKAGE

Arquivo: core/pipeline/__init__.py
Descrição: Exposição dos componentes da Pipeline Cognitiva.
Mark: V - Evolution / Thought Engine
Autor: Caio Vitor Malveira
=========================================
"""

from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.pipeline_step import PipelineStep

# Conforme especificação, CognitivePipeline e PipelineInitializer não são auto-importados para evitar ciclos.
__all__ = ["PipelineContext", "PipelineStep"]