"""
=========================================
JARVIS CORE - SERVER GATEWAY

Arquivo:
server.py

Descrição:
Servidor API REST para comunicação remota (Celular -> Notebook).
Permite que o JARVIS opere de qualquer lugar através de chamadas HTTP.
=========================================
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Garantir que o Python encontre a pasta core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.mind.brain import Brain
# Importe seu logger e event_bus reais criados no seu main.py se necessário
# Aqui criaremos instâncias limpas para acoplamento automático

app = Flask(__name__)
CORS(app)

print("\n[KERNEL] Inicializando Cérebro do JARVIS para modo Remoto...")
jarvis_brain = Brain()

# Simulação de acoplamento dos submódulos existentes no seu projeto
# Certifique-se de passar suas instâncias reais de memory/tools se tiver classes prontas
class LocalTools:
    def available(self):
        return ["web_search", "create_persona", "create_plugin", "execute_terminal_command"]
    
    def execute(self, name, **kwargs):
        if name == "execute_terminal_command":
            import subprocess
            cmd = kwargs.get("command", "")
            try:
                res = subprocess.run(cmd, shell=True, text=True, capture_output=True, timeout=30)
                if res.returncode == 0:
                    return f"Sucesso, Senhor. Saída:\n{res.stdout}"
                return f"Erro na execução (Código {res.returncode}):\n{res.stderr}"
            except Exception as e:
                return f"Falha crítica ao rodar comando: {str(e)}"
        return f"Ferramenta {name} executada com sucesso (Simulação)."

jarvis_brain.connect(tools=LocalTools())
jarvis_brain.initialize()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"response": "Estou ouvindo, Senhor. Mas não detectei nenhuma diretriz na mensagem."}), 400
    
    # Processamento cognitivo dinâmico pelo LLM + Ferramentas locais
    response = jarvis_brain.process(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    print("\n============================================================")
    print("      GATEWAY DA MATRIX ONLINE - PORTA 5000")
    print("  O JARVIS está pronto para receber comandos do seu celular.")
    print("============================================================\n")
    app.run(host="0.0.0.0", port=5000, debug=False)