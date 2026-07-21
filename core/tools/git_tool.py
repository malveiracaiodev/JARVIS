"""
=========================================
GENESIS CORE

Arquivo:
core/tools/git_tool.py

Descrição:
Ferramenta de automação Git para
o DeveloperAgent (Mark V).

Autor:
Caio Vitor Malveira
=========================================
"""

import subprocess
from typing import Any, Dict


class GitTool:
    """
    Executa comandos git de forma programática.
    """

    def __init__(self, repo_dir: str = ".") -> None:
        self.repo_dir = repo_dir

    def _run_git(self, args: list) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "success": True,
                "output": result.stdout.strip()
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "output": e.stdout.strip(),
                "error": e.stderr.strip()
            }

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        command = action.get("strategy") or action.get("command")

        if command == "git_status":
            return self._run_git(["status", "--porcelain"])

        elif command == "git_diff":
            return self._run_git(["diff"])

        elif command == "git_commit":
            message = action.get("message", "Auto commit by Genesis DeveloperAgent")
            add_all = action.get("add_all", True)
            if add_all:
                self._run_git(["add", "."])
            return self._run_git(["commit", "-m", message])

        return {"success": False, "message": f"Comando git desconhecido: {command}"}