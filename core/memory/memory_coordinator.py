"""
=========================================
GENESIS CORE

Arquivo:
core/memory/memory_coordinator.py

Descrição:
Coordenador e fachada central dos sistemas 
de memória do Genesis Core.

Responsável por unificar o acesso à ShortTermMemory
e LongTermMemory, oferecendo um ponto único 
de entrada para o Thought Engine e o Pipeline Cognitivo.

Arquitetura:
Genesis Core

Mark:
V - Evolution (Memory Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

from core.interfaces.memory_interface import MemoryInterface
from core.memory.short_term_memory import ShortTermMemory
from core.memory.long_term_memory import LongTermMemory
import threading

class MemoryCoordinator(MemoryInterface):
    """
    Fachada que gerencia múltiplos backends de memória (Curto e Longo Prazo),
    roteando comandos de acordo com a criticidade e escopo da informação.
    """

    def __init__(self, memory_manager=None):
        self._short_term = ShortTermMemory()
        self._long_term = LongTermMemory(memory_manager=memory_manager)
        self._lock = threading.RLock()

    def store(self, data, memory_type="short_term"):
        """
        Roteia o armazenamento para o backend apropriado.
        - 'short_term', 'working' -> ShortTermMemory
        - 'long_term', 'episodic', 'semantic' -> LongTermMemory
        """
        with self._lock:
            if memory_type in ["long_term", "episodic", "semantic"]:
                return self._long_term.store(data, memory_type=memory_type)
            else:
                return self._short_term.store(data, memory_type=memory_type)

    def retrieve(self, query, context=None):
        """Busca combinada em ambas as camadas de memória (Curto e Longo Prazo)."""
        with self._lock:
            st_results = self._short_term.retrieve(query, context=context)
            lt_results = self._long_term.retrieve(query, context=context)
            
            return {
                "short_term": st_results,
                "long_term": lt_results
            }

    def search(self, query, limit=10):
        """Executa busca unificada priorizando resultados recentes e persistidos."""
        with self._lock:
            lt_matches = self._long_term.search(query, limit=limit)
            st_matches = self._short_term.search(query, limit=limit)
            
            return {
                "short_term": st_matches,
                "long_term": lt_matches
            }

    def clear(self):
        """Limpa a memória volátil e opcionalmente emite aviso sobre a persistente."""
        with self._lock:
            st_msg = self._short_term.clear()
            return f"Coordinator Reset -> {st_msg} (Long-term memory preserved)."

    def forget(self, memory_id):
        """Tenta remover o ID em ambos os backends."""
        with self._lock:
            if memory_id.startswith("stm_"):
                return self._short_term.forget(memory_id)
            elif memory_id.startswith("ltm_"):
                return self._long_term.forget(memory_id)
            
            # Varredura geral caso o prefixo não seja explícito
            st_removed = self._short_term.forget(memory_id)
            lt_removed = self._long_term.forget(memory_id)
            return st_removed or lt_removed

    def save(self):
        """Força persistência na camada de longo prazo."""
        with self._lock:
            return self._long_term.save()

    def load(self):
        """Carrega dados persistidos."""
        with self._lock:
            return self._long_term.load()

    def status(self):
        """Retorna o status consolidado de todo o sub-sistema de memória."""
        with self._lock:
            return {
                "name": self.name(),
                "short_term_status": self._short_term.status(),
                "long_term_status": self._long_term.status(),
                "status": "operational"
            }

    def name(self):
        return "memory.coordinator"