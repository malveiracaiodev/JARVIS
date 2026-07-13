"""
=========================================
JARVIS CORE

Arquivo:
agent.py

Descrição:
Classe base thread-safe para agentes inteligentes do ecossistema.

Arquitetura:
Genesis Core

Mark:
II - Evolution (Patch 2.6)
=========================================
"""

import threading
from collections import deque
from datetime import datetime


class Agent:
    """
    Classe base para representação de agentes autônomos e integrados.
    """

    def __init__(self, name, personality="default"):
        self.name = name
        self.personality = personality
        self.status = "created"
        
        # Histórico de memória interna circular para evitar vazamento de RAM
        self.memory = deque(maxlen=500)
        self.mind = None
        self.created = datetime.now()
        
        # Lock de sincronização interno do agente
        self._lock = threading.RLock()

    def connect_mind(self, mind):
        with self._lock:
            self.mind = mind
            self.speak(f"Conexão estabelecida com a matriz analítica (Mind).")

    def start(self):
        with self._lock:
            self.status = "online"
            self.speak("Subsistema de IA ativado. Online.")

    def receive(self, message):
        with self._lock:
            self.memory.append({
                "message": message,
                "time": datetime.now().isoformat()
            })
            
            if self.mind:
                try:
                    return self.mind.think(message)
                except Exception as e:
                    return f"Erro de processamento neural: {str(e)}"

            return self.think(message)

    def think(self, message):
        """Método padrão a ser sobrescrito por especializações."""
        return f"{self.name}: Núcleo cognitivo padrão ativo. Nenhuma diretiva customizada."

    def speak(self, text):
        # Desacoplamento para o terminal padrão usando formatação uniforme
        print(f"[{self.name.upper()}] -> {text}")

    def stop(self):
        with self._lock:
            self.status = "offline"
            self.speak("Sequência de encerramento concluída. Offline.")