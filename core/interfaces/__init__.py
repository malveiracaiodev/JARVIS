"""
=========================================
JARVIS CORE

Pacote:
core.interfaces

Descrição:
Exposição centralizada dos contratos
abstratos utilizados pelo Genesis Core.

Esta camada define os acordos entre
módulos do sistema.

Nenhuma implementação deve existir aqui.

Arquitetura:

                Genesis Core

                    |
            Interfaces / Contracts

                    |
    --------------------------------

    Input
      |
    Parser

    Cognition
      |
    Brain
    Planner
    Reasoner

    Execution
      |
    Executor
    Tool

    Memory
      |
    Memory
    Knowledge


Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""


# =====================================================
# INPUT / ENTRADA
# =====================================================

from .command_interface import CommandInterface
from .parser_interface import ParserInterface



# =====================================================
# COGNIÇÃO
# =====================================================

from .brain_interface import BrainInterface
from .pipeline_interface import PipelineInterface
from .planner_interface import PlannerInterface
from .reasoner_interface import ReasonerInterface



# =====================================================
# EXECUÇÃO
# =====================================================

from .executor_interface import ExecutorInterface
from .tool_interface import ToolInterface



# =====================================================
# MEMÓRIA / CONHECIMENTO
# =====================================================

from .memory_interface import MemoryInterface
from .knowledge_interface import KnowledgeInterface



# =====================================================
# EXPORTAÇÃO PÚBLICA
# =====================================================

__all__ = [

    # Entrada
    "CommandInterface",
    "ParserInterface",


    # Cognição
    "BrainInterface",
    "PipelineInterface",
    "PlannerInterface",
    "ReasonerInterface",


    # Execução
    "ExecutorInterface",
    "ToolInterface",


    # Memória
    "MemoryInterface",
    "KnowledgeInterface",

]