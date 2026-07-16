"""
=========================================
JARVIS CORE

Pacote:
core.cognitive

Descrição:
Exposição centralizada dos módulos
cognitivos do Genesis Core.

Esta camada reúne os componentes
especializados responsáveis pelo
processamento inteligente do sistema.

Arquitetura:

                Brain
                  │
         Cognitive Pipeline
                  │
    ┌─────────────┼─────────────┐
    │             │             │
 Parser       Planner      Reasoner
                                   │
                              Executor
                                   │
                              Reflection

Arquitetura:
Genesis Core

Mark:
III - Intelligence

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
# APRENDIZADO
# =====================================================

from .reflection import Reflection


# =====================================================
# EXPORTAÇÃO PÚBLICA
# =====================================================

__all__ = [

    "Parser",

    "Planner",

    "Reasoner",

    "Executor",

    "Reflection",

]