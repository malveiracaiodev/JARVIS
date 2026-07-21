"""
=========================================
JARVIS CORE - SECURE SERVER GATEWAY

Arquivo:
server.py

Descrição:
Servidor API REST seguro para comunicação remota (Celular -> Notebook).
Inicializa o ecossistema oficial através do Kernel e implementa
execução protegida de tarefas em espaço de trabalho isolado.
=========================================
"""

import os
import sys
import shlex
import subprocess
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

# Garante que o interpretador encontre os módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.kernel.kernel import Kernel

app = Flask(__name__)
CORS(app)

# Configurações de Segurança Estruturais
GATEWAY_TOKEN = os.environ.get("JARVIS_API_TOKEN", "substitua_por_um_token_longo_e_seguro")
WORKSPACE_DIR = os.path.abspath("./workspace")

# Garante a existência da pasta de projetos semi-prontos
os.makedirs(WORKSPACE_DIR, exist_ok=True)

print("\n[BOOT] Inicializando o Kernel do Genesis Core...")
kernel = Kernel()
kernel.boot()
print("[OK] Kernel totalmente operativo para requisições externas.\n")


class SecureProjectTools:
    """
    Substitui o mock antigo por um Executor de Tarefas robusto
    e isolado dentro do diretório do Workspace.
    """
    def available(self):
        return ["create_project_structure", "write_source_file", "run_safe_script"]

    def execute(self, name, **kwargs):
        if name == "create_project_structure":
            project_name = kwargs.get("project_name", "novo_projeto").strip()
            # Sanitiza o nome para evitar caminhos relativos maliciosos (ex: ../../)
            safe_name = os.path.basename(project_name)
            project_path = os.path.join(WORKSPACE_DIR, safe_name)
            
            try:
                os.makedirs(project_path, exist_ok=True)
                return f"Estrutura do projeto '{safe_name}' criada com sucesso no workspace, Senhor."
            except Exception as e:
                return f"Falha ao criar diretório do projeto: {str(e)}"

        if name == "write_source_file":
            project_name = os.path.basename(kwargs.get("project_name", ""))
            file_name = os.path.basename(kwargs.get("file_name", "main.py"))
            content = kwargs.get("content", "")
            
            target_path = os.path.join(WORKSPACE_DIR, project_name, file_name)
            try:
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return f"Arquivo '{file_name}' escrito com sucesso em '{project_name}'."
            except Exception as e:
                return f"Erro ao persistir o código em disco: {str(e)}"

        return f"Ação '{name}' não reconhecida pelo ambiente seguro."

# Conecta o ecossistema de ferramentas seguras ao cérebro do Jarvis
if hasattr(kernel, "mind") and hasattr(kernel.mind, "brain"):
    kernel.mind.brain.connect(tools=SecureProjectTools())


@app.route("/chat", methods=["POST"])
def chat():
    # Validação simples e rápida de segurança (Substitua por um Token seu)
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, description="Acesso não autorizado, Senhor.")
    
    token = auth_header.split(" ")[1]
    if token != GATEWAY_TOKEN:
        abort(403, description="Token inválido.")

    data = request.json or {}
    user_input = data.get("message", "").strip()
    # Permite escolher o agente pelo celular ("jarvis" ou "rafiki")
    target_agent = data.get("agent", "jarvis").lower() 
    
    if not user_input:
        return jsonify({"response": "Estou ouvindo, Senhor."}), 400
    
    try:
        # Carrega a persona dinamicamente usando a Factory do Genesis Core
        from personas.persona_factory import PersonaFactory
        factory = PersonaFactory()
        persona = factory.create(target_agent)
        
        # Vincula os motores necessários à persona carregada
        persona.connect_response_engine(kernel.mind.brain.response_engine)
        persona.connect_tools(kernel.mind.brain.tools)
        
        # Intercepta comandos de criação de arquivos direto se o agente for o Jarvis
        if target_agent == "jarvis" and "crie o arquivo" in user_input.lower():
            # Exemplo rápido de automação de escrita de arquivos no workspace
            # (Futuramente integrado de forma 100% autônoma pela LLM)
            resultado = SecureProjectTools().execute(
                "write_source_file", 
                project_name="Rascunhos", 
                file_name="ideia_nova.py", 
                content=f"# Ideia do Caio:\n# {user_input}"
            )
            return jsonify({"response": resultado})

        # Fluxo normal de conversação (IA) injetando o estilo do Rafiki ou Jarvis
        response_text = persona.respond(user_input)
        return jsonify({"response": response_text})

    except Exception as error:
        return jsonify({"error": "Falha no ciclo rápido", "details": str(error)}), 500


if __name__ == "__main__":
    print("\n============================================================")
    print("      GATEWAY DA MATRIX SEGURO OPERANTE - PORTA 5000")
    print("  O JARVIS está pronto para receber suas ideias da rua.")
    print("============================================================\n")
    app.run(host="0.0.0.0", port=5000, debug=False)