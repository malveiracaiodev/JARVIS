"""
=========================================
GENESIS CORE

Pacote:
core.pipeline

Descrição:
Exposição dos componentes da Pipeline Cognitiva.

Arquitetura:
Genesis Core

Mark:
IV - Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""


"""
IMPORTANTE:

Este arquivo NÃO deve importar:

- PipelineInitializer
- CognitivePipeline

automaticamente.

Motivo:

Evita ciclo:

cognitive
   |
 parser
   |
 pipeline
   |
 initializer
   |
 cognitive

A inicialização deve ser explícita.
"""


__all__ = []