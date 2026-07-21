"""
=========================================
GENESIS CORE

Arquivo:
core/tools/file_system_tool.py

Descrição:
Ferramenta de manipulação do sistema de arquivos
para o DeveloperAgent (Mark V).

Autor:
Caio Vitor Malveira
=========================================
"""

import os
from typing import Any, Dict


class FileSystemTool:
    """
    Permite ler, escrever e listar arquivos de forma controlada.
    """

    def __init__(self, base_dir: str = ".") -> None:
        self.base_dir = os.path.abspath(base_dir)

    def _resolve_path(self, relative_path: str) -> str:
        # Previne path traversal básico
        safe_path = os.path.normpath(
            os.path.join(self.base_dir, relative_path)
        )
        if not safe_path.startswith(self.base_dir):
            raise ValueError("Acesso negado fora do diretório base do projeto.")
        return safe_path

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        command = action.get("strategy") or action.get("command")
        path = action.get("path")

        if not path:
            return {"success": False, "message": "Caminho do arquivo não fornecido."}

        try:
            full_path = self._resolve_path(path)

            if command == "read_file":
                if not os.path.exists(full_path):
                    return {"success": False, "message": f"Arquivo não encontrado: {path}"}
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return {"success": True, "content": content}

            elif command == "write_file":
                content = action.get("content", "")
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return {"success": True, "message": f"Arquivo gravado com sucesso: {path}"}

            elif command == "list_dir":
                if not os.path.exists(full_path):
                    return {"success": False, "message": f"Diretório não encontrado: {path}"}
                items = os.listdir(full_path)
                return {"success": True, "items": items}

            return {"success": False, "message": f"Comando desconhecido: {command}"}

        except Exception as error:
            return {"success": False, "message": str(error)}