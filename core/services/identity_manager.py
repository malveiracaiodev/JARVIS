"""
=========================================
JARVIS CORE

Arquivo:
core/services/identity_manager.py

Descrição:
Camada de identidade do Genesis Core.

Responsável por:
- Gerenciar identidade do sistema
- Controlar personas dos agentes
- Persistência segura da identidade
- Recuperação contra corrupção
- Fornecer contexto de identidade para agentes

Arquitetura:
Genesis Core

Mark:
III - Matrix (Identity Layer)

Autor:
Caio Vitor Malveira
=========================================
"""

import copy
import json
import os
import shutil
import threading
from datetime import datetime
from pathlib import Path
from core.base.module import Module, ModuleStatus


class IdentityManager(Module):
    """
    Gerenciador central de identidade (Mark III - Matrix).
    Reforçado para persistência atômica e resiliência a corrupção.
    """

    def __init__(self, logger=None, event_bus=None):
        super().__init__("core.identity_manager")
        self.version = "3.1"
        self.logger = logger
        self.event_bus = event_bus
        self.identity = {}
        self.file = Path("data/personas/identity.json")
        self._lock = threading.RLock()

    # ==================================================
    # CICLO DE VIDA (CONTRATOS OBRIGATÓRIOS)
    # ==================================================

    def initialize(self):
        """Inicializa o IdentityManager e carrega os dados de identidade."""
        with self._lock:
            if self.is_online():
                return

            self.set_status(ModuleStatus.INITIALIZING)
            try:
                self.load_identity()
                self.set_status(ModuleStatus.ONLINE)
                if self.logger:
                    self.logger.info("IdentityManager online e identidade carregada.")
            except Exception as error:
                self.set_error(f"Falha na inicialização do IdentityManager: {error}")
                if self.logger:
                    self.logger.error(self.error_message)

    def shutdown(self):
        """Encerra o IdentityManager garantindo salvamento seguro."""
        with self._lock:
            self.set_status(ModuleStatus.OFFLINE)
            try:
                self.save_identity()
            except Exception:
                pass
            if self.logger:
                self.logger.info("IdentityManager encerrado.")

    # ==================================================
    # LOGS AUXILIARES
    # ==================================================

    def log_info(self, message):
        if self.logger:
            self.logger.info(message)

    def log_error(self, message):
        if self.logger:
            self.logger.error(message)

    # ==================================================
    # PERSISTÊNCIA E IDENTIDADE
    # ==================================================

    def default_identity(self):
        """Retorna a estrutura de identidade padrão do sistema."""
        return {
            "name": "JARVIS",
            "version": "Genesis Core Mark IV",
            "creator": "Caio Vitor Malveira",
            "persona": "Assistente de Inteligência Artificial avançado e autônomo.",
            "traits": ["resiliente", "analítico", "proativo"]
        }

    def save_identity(self):
        """Salva a identidade com garantia de integridade física (fsync)."""
        with self._lock:
            self.file.parent.mkdir(parents=True, exist_ok=True)
            temp_file = self.file.with_suffix(".tmp")
            
            try:
                # Escrita atômica com descarga física
                with open(temp_file, "w", encoding="utf-8") as file:
                    json.dump(self.identity, file, indent=4, ensure_ascii=False)
                    file.flush()
                    os.fsync(file.fileno())
                
                # Substituição atômica no sistema de arquivos
                temp_file.replace(self.file)
            except Exception as error:
                if temp_file.exists():
                    temp_file.unlink()
                self.log_error(f"Falha crítica na escrita da identidade: {error}")
                raise

    def load_identity(self):
        """Carregamento com recuperação automática de falhas."""
        with self._lock:
            if not self.file.exists():
                self.identity = self.default_identity()
                self.save_identity()
                return

            try:
                with open(self.file, "r", encoding="utf-8") as file:
                    self.identity = json.load(file)
            except (json.JSONDecodeError, TypeError, OSError) as e:
                self.log_error(f"Identidade corrompida detectada: {e}")
                self._handle_corruption()
                self.identity = self.default_identity()
                self.save_identity()

    def _handle_corruption(self):
        """Isola o arquivo corrompido para análise forense."""
        backup = self.file.parent / f"corrupted_identity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            shutil.move(self.file, backup)
            self.log_info(f"Arquivo corrompido movido para: {backup}")
        except Exception as e:
            self.log_error(f"Falha ao mover arquivo corrompido: {e}")

    def get_full_identity(self):
        with self._lock:
            return copy.deepcopy(self.identity)

    def get(self, key, default=None):
        with self._lock:
            return self.identity.get(key, default)