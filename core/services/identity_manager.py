"""
=========================================
JARVIS CORE

Arquivo:
identity_manager.py

Descrição:
Sistema de identidade do JARVIS.

Responsável por:
- Carregar identidade de forma thread-safe
- Escrita atômica de definições e propósitos
- Fornecer informações limpas do agente
- Tratamento de corrupção de arquivos de persona

Arquitetura:
Genesis Core

Mark:
II - Identity Layer (Patch 2.1 - Production Ready)

Autor:
Caio Vitor Malveira
=========================================
"""

import json
import shutil
import threading
from datetime import datetime
from pathlib import Path

from core.base.module import (
    Module,
    ModuleStatus
)


class IdentityManager(Module):
    """
    Gerenciador seguro da identidade e definições comportamentais do JARVIS.
    """

    def __init__(self, logger=None, event_bus=None):
        super().__init__("core.identity_manager")
        self.version = "2.1"
        self.logger = logger
        self.event_bus = event_bus
        self.identity = {}
        self.file = Path("data/personas/identity.json")
        self._lock = threading.RLock()  # Proteção contra concorrência

    # ======================================================
    # CICLO DE VIDA
    # ======================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        try:
            self.load_identity()
            self.set_status(ModuleStatus.ONLINE)
            
            self.emit("IDENTITY_LOADED")
            self.log_success("Identity Manager iniciado com proteção de camada")
        except Exception as error:
            self.set_error(str(error))
            self.log_error(str(error))

    def shutdown(self):
        self.set_status(ModuleStatus.OFFLINE)
        self.log_info("Identity Manager encerrado")

    # ======================================================
    # CARREGAMENTO E PERSISTÊNCIA
    # ======================================================

    def load_identity(self):
        with self._lock:
            if not self.file.exists():
                self.identity = self.default_identity()
                self.save_identity()
                return

            try:
                with open(self.file, "r", encoding="utf-8") as file:
                    self.identity = json.load(file)
                self.log_info("Identidade carregada com sucesso do disco")
            except (json.JSONDecodeError, TypeError) as decode_error:
                # Recuperação de desastre: evita falha crítica de inicialização do JARVIS
                backup_path = self.file.parent / f"corrupted_identity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                shutil.copy(self.file, backup_path)
                
                self.identity = self.default_identity()
                self.save_identity()
                
                if self.logger and hasattr(self.logger, "error"):
                    self.logger.error(f"Arquivo de identidade corrompido! Resetado para o padrão. Backup em: {backup_path.name}")

    def save_identity(self):
        with self._lock:
            self.file.parent.mkdir(parents=True, exist_ok=True)
            temp_file = self.file.with_suffix(".tmp")
            try:
                # Escrita Atômica
                with open(temp_file, "w", encoding="utf-8") as file:
                    json.dump(self.identity, file, indent=4, ensure_ascii=False)
                
                if temp_file.exists():
                    temp_file.replace(self.file)
            except Exception as e:
                if temp_file.exists():
                    temp_file.unlink()
                if self.logger and hasattr(self.logger, "error"):
                    self.logger.error(f"Falha ao salvar arquivo de identidade: {str(e)}")
                raise e

    # ======================================================
    # IDENTIDADE PADRÃO
    # ======================================================

    def default_identity(self):
        return {
            "name": "JARVIS",
            "creator": "Caio Vitor Malveira",
            "version": "Mark II - Genesis",
            "purpose": [
                "Auxiliar o usuário",
                "Organizar informações",
                "Gerenciar tarefas",
                "Aprender novos conhecimentos"
            ],
            "personality": {
                "style": "assistente inteligente",
                "tone": "amigável"
            }
        }

    # ======================================================
    # CONSULTA
    # ======================================================

    def get(self, key, default=None):
        with self._lock:
            return self.identity.get(key, default)

    def get_full_identity(self):
        with self._lock:
            return dict(self.identity)

    def introduce(self):
        with self._lock:
            purposes = "\n".join([f"- {p}" for p in self.get('purpose', [])])
            
            # Formatação limpa de parágrafos sem quebras absurdas
            intro_text = (
                f"Olá.\n"
                f"Eu sou {self.get('name')}.\n"
                f"Fui criado por {self.get('creator')}.\n\n"
                f"Meu propósito é:\n{purposes}\n\n"
                f"Versão: {self.get('version')}\n"
                f"Sistema operacional."
            )
            return intro_text

    def who_am_i(self):
        return self.introduce()

    # ======================================================
    # EVENTOS E LOG
    # ======================================================

    def emit(self, event, *args, **kwargs):
        if self.event_bus:
            try:
                self.event_bus.emit(event, *args, **kwargs)
            except Exception:
                pass

    def log_info(self, message):
        if self.logger:
            self.logger.info(message)

    def log_success(self, message):
        if self.logger:
            self.logger.success(message)

    def log_error(self, message):
        if self.logger:
            self.logger.error(message)