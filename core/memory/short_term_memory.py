"""
=========================================
GENESIS CORE

Arquivo:
core/memory/short_term_memory.py

Descrição:
Implementação da memória de curto prazo
(Short-Term Memory) do Genesis Core.

Responsável por armazenar o contexto volátil
da sessão atual, histórico recente e estados
temporários do pipeline cognitivo.

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

class ShortTermMemory(MemoryInterface):
    """
    Gerenciador de memória de curto prazo (volátil).
    Ideal para manter o contexto imediato da conversa e do Thought Engine.
    """

    def __init__(self, max_capacity=50):
        self._storage = []
        self._max_capacity = max_capacity
        self._lock = threading.RLock()

    def store(self, data, memory_type="short_term"):
        """Armazena um dado na memória de curto prazo respeitando o limite máximo."""
        with self._lock:
            entry = {
                "id": f"stm_{len(self._storage) + 1}_{int(datetime.now().timestamp())}",
                "data": data,
                "type": memory_type,
                "timestamp": datetime.now().isoformat()
            }
            
            self._storage.append(entry)
            
            # Controla capacidade máxima (FIFO se estourar o limite)
            if len(self._storage) > self._max_capacity:
                self._storage.pop(0)
                
            return entry["id"]

    def retrieve(self, query, context=None):
        """Recupera itens recentes que correspondem à query ou ao contexto."""
        with self._lock:
            if not query:
                return self._storage.copy()
            
            results = [
                item for item in self._storage 
                if query.lower() in str(item.get("data", "")).lower()
            ]
            return results

    def search(self, query, limit=10):
        """Busca textual simples na memória volátil."""
        with self._lock:
            matches = self.retrieve(query)
            return matches[-limit:]

    def clear(self):
        """Limpa toda a memória de curto prazo da sessão."""
        with self._lock:
            count = len(self._storage)
            self._storage.clear()
            return f"Memória de curto prazo limpa. {count} itens removidos."

    def forget(self, memory_id):
        """Remove um item específico pelo ID."""
        with self._lock:
            initial_len = len(self._storage)
            self._storage = [item for item in self._storage if item.get("id") != memory_id]
            return len(self._storage) < initial_len

    def save(self):
        """Memória de curto prazo é volátil, logo a persistência direta não se aplica aqui."""
        return "Short-term memory is volatile and does not persist directly to disk."

    def load(self):
        """Inicializa ou reinicializa o estado volátil."""
        with self._lock:
            self._storage.clear()
            return True

    def status(self):
        """Retorna o estado operacional."""
        with self._lock:
            return {
                "name": self.name(),
                "active_items": len(self._storage),
                "max_capacity": self._max_capacity,
                "status": "operational"
            }

    def name(self):
        return "memory.short_term"