"""
=========================================
JARVIS CORE

Arquivo:
reasoning.py

Descrição:
Motor analítico e gerador de planos lógicos sequenciais estruturados.

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from datetime import datetime
from core.base.module import Module, ModuleStatus


class Reasoning(Module):
    """
    Mecanismo determinístico estruturado para resolução e decomposição de problemas.
    Atua nativamente sob a persona de JARVIS.
    """

    def __init__(self):
        super().__init__("core.mind.reasoning")
        self.version = "3.0"
        self.history = []
        self._lock = threading.RLock()

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        self.set_status(ModuleStatus.ONLINE)
        self._log_safe("success", "Motor de decomposição de problemas e raciocínio ativo.")

    def shutdown(self):
        self.set_status(ModuleStatus.OFFLINE)
        self._log_safe("info", "Motor de raciocínio suspenso temporariamente.")

    def _log_safe(self, level, message):
        """Prevenção contra erros de herança de loggers no shutdown."""
        if hasattr(self, "logger") and self.logger:
            log_method = getattr(self.logger, level, None)
            if log_method and callable(log_method):
                log_method(f"[{self.name}] {message}")
                return
        
        log_fallback = getattr(super(), level, None)
        if log_fallback and callable(log_fallback):
            try:
                log_fallback(message)
            except TypeError:
                print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{level.upper()}] [{self.name}] {message}")

    def analyze(self, input_text, context=None):
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "context": context
        }
        with self._lock:
            self.history.append(analysis)
        return self.generate_response(input_text, context)

    def generate_response(self, input_text, context):
        text = input_text.lower()

        if "como" in text:
            return "[JARVIS] Analisando a questão estruturalmente... Irei considerar os vetores de contexto disponíveis e traçar as rotas de execução ideais."

        if any(keyword in text for keyword in ["devo", "vale a pena", "compensa"]):
            return "[JARVIS] Deixe-me executar uma análise ponderada de risco, Senhor. Irei comparar custos, escopo e benefícios da ação projetada."

        if any(keyword in text for keyword in ["planejar", "plano", "organizar"]):
            plan = self.create_plan(input_text)
            return "[JARVIS] Planejamento sequencial estruturado:\n\n- " + "\n- ".join(plan["steps"])

        if context:
            knowledge_list = context.get("knowledge")
            if knowledge_list and len(knowledge_list) > 0:
                first = knowledge_list[0]
                return f"[JARVIS] Encontrei este registro relevante em meus arquivos locais:\n\n{first.get('information')}"

        return "[JARVIS] Entendi seu comando, Senhor. Estou de prontidão para processar requisições ou gerenciar novas integrações físicas no Kernel."

    def create_plan(self, objective):
        return {
            "objective": objective,
            "steps": [
                "Isolar variáveis, restrições e objetivos descritos pelo Criador",
                "Mapear dependências externas na árvore lógica do sistema",
                "Executar varredura em bancos de conhecimento históricos",
                "Sintetizar rotas analíticas em chamadas assíncronas",
                "Consolidar a resposta e registrar novos aprendizados no Knowledge Core"
            ]
        }

    def last_analysis(self):
        with self._lock:
            return self.history[-1] if self.history else None

    def clear_history(self):
        with self._lock:
            self.history.clear()

    def status_report(self):
        with self._lock:
            return {
                "name": self.name,
                "version": self.version,
                "status": self.get_status().value,
                "analyses": len(self.history)
            }