"""
=========================================
JARVIS CORE

Pacote:
core.cognitive

Descrição:
Exposição centralizada dos módulos
cognitivos do Genesis Core (Mark V - Evolution).

Esta camada reúne os componentes
especializados responsáveis pelo
processamento inteligente do sistema
integrado à memória de longo prazo.

Arquitetura:

                Brain
                  │
         Cognitive Pipeline
                  │
    ┌─────────────┼─────────────┐
    │             │             │
Parser         Planner       Reasoner
                  │
               Executor
                  │
             Reflection
                  │
               Memória

Arquitetura:
Genesis Core

Mark:
V - Evolution / Thought Engine

Autor:
Caio Vitor Malveira
=========================================
"""

# =====================================================
# INTERPRETAÇÃO
# =====================================================

from .parser import Parser


# =====================================================
# PLANEJAMENTO
# =====================================================

from .planner import Planner


# =====================================================
# RACIOCÍNIO
# =====================================================

from .reasoner import Reasoner


# =====================================================
# EXECUÇÃO
# =====================================================

from .executor import Executor


# =====================================================
# APRENDIZADO & REFLEXÃO
# =====================================================

from .reflection import Reflection


# =====================================================
# CONTROLE DO CICLO COGNITIVO
# =====================================================

from .thought_engine import ThoughtEngine


# =====================================================
# EXPORTAÇÃO PÚBLICA
# =====================================================

__all__ = [
    "Parser",
    "Planner",
    "Reasoner",
    "Executor",
    "Reflection",
    "ThoughtEngine",
]