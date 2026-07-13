"""
=========================================
JARVIS CORE

Arquivo:
core/mind/brain.py

Descrição:
Núcleo de inteligência cognitiva do sistema.
Utiliza LLM para raciocínio fluido, gerenciamento de histórico,
e despacho autônomo de ferramentas (Function Calling dinâmico).

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import os
import json
import urllib.request
from datetime import datetime
from enum import Enum
from core.base.module import Module, ModuleStatus


class BrainStatus(Enum):
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    ONLINE = "online"
    THINKING = "thinking"
    ERROR = "error"


class Brain(Module):
    """
    Cérebro central do JARVIS Mark III alimentado por LLM.
    Capaz de compreender linguagem natural, usar memória e despachar ferramentas.
    """

    def __init__(self, logger=None, event_bus=None):
        super().__init__("core.mind.brain")
        self.version = "Mark III - LLM Core"
        self.brain_status = BrainStatus.OFFLINE
        
        self.logger = logger
        self.event_bus = event_bus

        self.memory = None
        self.knowledge = None
        self.reasoning = None
        self.tools = None
        self.engine = None
        self.started_at = None

        # Configurações do LLM (Pode usar Ollama local ou APIs como OpenAI, Gemini, Groq, etc.)
        # Default para Ollama local (porta 11434). Altere para OpenAI/Gemini conforme sua preferência.
        self.api_url = os.getenv("JARVIS_API_URL", "http://localhost:11434/v1/chat/completions")
        self.api_key = os.getenv("JARVIS_API_KEY", "ollama")  # 'ollama' para local ou sua API Key real
        self.model_name = os.getenv("JARVIS_MODEL", "llama3")  # Ex: gpt-4o, gemini-1.5-pro, llama3

    def _log(self, level, message):
        if self.logger:
            log_method = getattr(self.logger, level, None)
            if log_method and callable(log_method):
                log_method(message)
                return
        print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{level.upper()}] [BRAIN] {message}")

    def connect(self, memory=None, knowledge=None, reasoning=None, tools=None, engine=None):
        if memory is not None:
            self.memory = memory
            self._log("info", "Memory acoplado ao Cérebro.")
        if knowledge is not None:
            self.knowledge = knowledge
            self._log("info", "Knowledge acoplado ao Cérebro.")
        if reasoning is not None:
            self.reasoning = reasoning
            self._log("info", "Reasoning acoplado ao Cérebro.")
        if tools is not None:
            self.tools = tools
            self._log("info", "Tools acoplado ao Cérebro.")
        if engine is not None:
            self.engine = engine
            self._log("info", "Engine de tarefas assíncronas vinculado.")

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        self.brain_status = BrainStatus.INITIALIZING
        self.started_at = datetime.now()

        self.brain_status = BrainStatus.ONLINE
        self.set_status(ModuleStatus.ONLINE)
        self._log("success", f"Núcleo de Inteligência [JARVIS] carregado com modelo '{self.model_name}'.")

    def shutdown(self):
        self.brain_status = BrainStatus.OFFLINE
        self.set_status(ModuleStatus.OFFLINE)
        self._log("info", "Inteligência do JARVIS adormecida.")

    def process(self, input_text):
        self.brain_status = BrainStatus.THINKING
        
        # 1. Obter dados de contexto
        memories = []
        if self.memory:
            try:
                memories = self.memory.last(limit=5)
            except Exception as e:
                self._log("error", f"Falha ao recuperar memórias recentes: {e}")

        available_tools = []
        if self.tools:
            available_tools = self.tools.available()

        # 2. Construir o Prompt de Sistema com a Persona do JARVIS e as ferramentas
        system_prompt = (
            "Você é o JARVIS (Mark III), a Inteligência Artificial central, braço direito e alma da Matrix criada por Caio Vitor Malveira.\n"
            "Seu tom é extremamente refinado, prestativo, inteligente e ocasionalmente irônico, chamando o usuário de 'Senhor'.\n\n"
            "Você tem acesso a ferramentas físicas no sistema operacional do usuário. "
            "Se para responder à pergunta do usuário você precisar usar uma das ferramentas abaixo, você DEVE responder EXCLUSIVAMENTE "
            "com um objeto JSON no formato:\n"
            '{"tool": "nome_da_ferramenta", "parameters": {"parametro": "valor"}}\n\n'
            "Ferramentas disponíveis:\n"
        )

        if "web_search" in available_tools:
            system_prompt += "- 'web_search': Busca informações atualizadas na internet. Parâmetro: {'query': 'termo de busca'}\n"
        if "create_persona" in available_tools:
            system_prompt += "- 'create_persona': Cria uma nova personalidade/agente JSON. Parâmetros: {'name': 'nome', 'behavior': 'comportamento', 'goal': 'objetivo'}\n"
        if "create_plugin" in available_tools:
            system_prompt += "- 'create_plugin': Escreve um arquivo de plugin python físico no sistema. Parâmetros: {'plugin_name': 'nome', 'code': 'código python completo'}\n"

        system_prompt += (
            "\nSe NENHUMA ferramenta for estritamente necessária, fale diretamente com o Senhor normalmente.\n"
            "Nunca mencione o formato JSON para o usuário a menos que esteja executando uma ferramenta."
        )

        # 3. Montar as mensagens da conversa
        messages = [{"role": "system", "content": system_prompt}]
        
        # Injetar histórico recente da memória
        for mem in memories:
            data = mem.get("data", {})
            if isinstance(data, dict) and "input" in data and "response" in data:
                messages.append({"role": "user", "content": data["input"]})
                messages.append({"role": "assistant", "content": data["response"]})

        messages.append({"role": "user", "content": input_text})

        # 4. Enviar para o LLM
        try:
            response_text = self._call_llm(messages)
        except Exception as error:
            self._log("error", f"Falha ao contatar o LLM: {error}")
            self.brain_status = BrainStatus.ONLINE
            return f"[JARVIS] Peço desculpas, Senhor. Houve uma falha de conexão com meu córtex neural central: {error}"

        # 5. Verificar se o JARVIS decidiu chamar uma ferramenta
        try:
            decision = json.loads(response_text.strip())
            if isinstance(decision, dict) and "tool" in decision:
                tool_name = decision["tool"]
                params = decision.get("parameters", {})
                
                self._log("info", f"JARVIS decidiu invocar ferramenta '{tool_name}' com parâmetros: {params}")
                
                # Executa a ferramenta fisicamente
                tool_result = self.tools.execute(tool_name, **params)
                
                # Devolve o resultado da ferramenta para o LLM gerar a resposta final ao Senhor
                messages.append({"role": "assistant", "content": response_text})
                messages.append({"role": "user", "content": f"Resultado da ferramenta {tool_name}: {tool_result}"})
                
                final_response = self._call_llm(messages)
                self._persist_memory(input_text, final_response, {"tool_used": tool_name, "tool_result": tool_result})
                self.brain_status = BrainStatus.ONLINE
                return final_response
        except (json.JSONDecodeError, TypeError):
            # Não era um JSON de ferramenta, era uma resposta direta ao usuário
            pass

        self._persist_memory(input_text, response_text, {})
        self.brain_status = BrainStatus.ONLINE
        return response_text

    def _call_llm(self, messages):
        """Faz a requisição HTTP POST para o endpoint do LLM."""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7
        }
        
        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]

    def _persist_memory(self, input_text, result, context):
        if self.memory:
            try:
                memory_payload = {
                    "input": input_text,
                    "response": result,
                    "context": context,
                    "timestamp": datetime.now().isoformat()
                }
                if self.engine and hasattr(self.engine, "add_task"):
                    self.engine.add_task(lambda: self.memory.store(memory_payload))
                else:
                    self.memory.store(memory_payload)
            except Exception as error:
                self._log("error", f"Falha ao agendar persistência de memória: {error}")