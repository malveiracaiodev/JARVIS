"""
=========================================
GENESIS CORE - TOOLS: LLM INTEGRATION (OLLAMA LOCAL)
=========================================
"""

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "phi3"

def processar_comando_jarvis(prompt_usuario):
    print(f"[Parser/Planner] Analisando via Ollama ({MODEL_NAME}): '{prompt_usuario}'")
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "Você é o Jarvis, um sistema operacional de IA direto e conciso."
            },
            {
                "role": "user",
                "content": prompt_usuario
            }
        ],
        "stream": False,
        "options": {
            "num_predict": 150,  # Limita o tamanho da resposta para poupar processamento
            "temperature": 0.3
        }
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        # Timeout de 30 segundos para evitar travamento infinito do processo
        response = requests.post(OLLAMA_URL, data=json.dumps(payload), headers=headers, timeout=30)
        response.raise_for_status()
        
        resultado = response.json()
        return resultado.get("message", {}).get("content", "[Erro]: Resposta vazia da IA.")
        
    except requests.exceptions.Timeout:
        return "[Erro]: O Ollama demorou muito para responder. O hardware excedeu a capacidade de processamento atual."
    except requests.exceptions.ConnectionError:
        return "[Erro Crítico]: Falha de conexão com o servidor do Ollama na porta 11434."
    except Exception as e:
        return f"[Erro na IA]: {e}"