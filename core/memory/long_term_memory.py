"""
=========================================
GENESIS CORE

Arquivo:
core/memory/long_term_memory.py

Descrição:
Implementação da memória de longo prazo
(Long-Term Memory) do Genesis Core.

Responsável por persistir e recuperar
informações de longo prazo utilizando
o MemoryManager base como motor
de armazenamento atômico.

Arquitetura:
Genesis Core

Mark:
V - Evolution (Memory Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

from core.interfaces.memory_interface import MemoryInterface
from datetime import datetime
import threading

class LongTermMemory(MemoryInterface):
    """
    Gerenciador de memória de longo prazo (persistente).
    Integra-se com o MemoryManager para garantir atomicidade,
    fsync e recuperação contra corrupção em disco.
    """

    def __init__(self, memory_manager=None):
        self._memory_manager = memory_manager
        self._lock = threading.RLock()

    def store(self, data, memory_type="long_term"):
        """Armazena um dado de forma persistente no sistema de longo prazo."""
        with self._lock:
            if not self._memory_manager:
                raise RuntimeError("MemoryManager não foi injetado na LongTermMemory.")
            
            entry = {
                "id": f"ltm_{int(datetime.now().timestamp())}",
                "data": data,
                "type": memory_type,
                "timestamp": datetime.now().isoformat()
            }
            
            # Adiciona na lista gerenciada pelo MemoryManager e persiste
            self._memory_manager.memories.append(entry)
            self._memory_manager.save()
            return entry["id"]

    def retrieve(self, query, context=None):
        """Recupera memórias persistidas que correspondem à query."""
        with self._lock:
            if not self._memory_manager:
                return []
            
            memories = self._memory_manager.memories
            if not query:
                return memories.copy()
            
            results = [
                item for item in memories 
                if query.lower() in str(item.get("data", "")).lower()
            ]
            return results

    def search(self, query, limit=10):
        """Busca semântica ou textual nas memórias persistidas de longo prazo."""
        with self._lock:
            matches = self.retrieve(query)
            return matches[-limit:]

    def clear(self):
        """Limpa toda a base de longo prazo (requer cautela)."""
        with self._lock:
            if not self._memory_manager:
                return "MemoryManager indisponível."
            
            count = len(self._memory_manager.memories)
            self._memory_manager.memories.clear()
            self._memory_manager.save()
            return f"Memória de longo prazo limpa. {count} registros removidos do disco."

    def forget(self, memory_id):
        """Remove uma memória persistente específica pelo ID."""
        with self._lock:
            if not self._memory_manager:
                return False
            
            memories = self._memory_manager.memories
            initial_len = len(memories)
            
            self._memory_manager.memories = [
                item for item in memories if item.get("id") != memory_id
            ]
            
            if len(self._memory_manager.memories) < initial_len:
                self._memory_manager.save()
                return True
            return False

    def save(self):
        """Força a persistência atual via MemoryManager."""
        with self._lock:
            if self._memory_manager:
                self._memory_manager.save()
                return True
            return False

    def load(self):
        """Carrega as memórias persistidas do disco."""
        with self._lock:
            if self._memory_manager:
                self._memory_manager.load()
                return True
            return False

    def status(self):
        """Retorna o estado operacional da memória de longo prazo."""
        with self._lock:
            total_items = len(self._memory_manager.memories) if self._memory_manager else 0
            return {
                "name": self.name(),
                "persisted_items": total_items,
                "storage_backend": "MemoryManager (JSON + fsync)",
                "status": "operational" if self._memory_manager else "degraded"
            }

    def name(self):
        return "memory.long_term"