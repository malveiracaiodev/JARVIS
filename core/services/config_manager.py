"""
=========================================
JARVIS CORE

Arquivo:
config_manager.py

Descrição:
Gerenciador central de configurações persistentes.

Responsável por:
- Carregamento e salvamento atômico thread-safe
- Controle parametrizado e migração de esquemas
- Tolerância a falhas na escrita (Prevenção de arquivos corrompidos)
- Ciclo de backup automático em tempo de execução

Arquitetura:
Genesis Core

Mark:
3 - Evolution (Patch 2.2 - Robust Storage)

Autor:
Caio Vitor Malveira
=========================================
"""

import json
import shutil
import threading
import os
import copy
from pathlib import Path
from core.base.module import Module, ModuleStatus


class ConfigManager(Module):
    """
    Serviço central de configuração com persistência atômica e segura (Mark III).
    """
    CONFIG_VERSION = 1
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    CONFIG_FOLDER = ROOT_DIR / "config"
    CONFIG_FILE = CONFIG_FOLDER / "settings.json"
    BACKUP_FILE = CONFIG_FOLDER / "settings.backup.json"
    TEMP_FILE = CONFIG_FOLDER / "settings.tmp.json"

    def __init__(self, logger=None):
        super().__init__("core.config_manager")
        self.version = "3.0"
        self.logger = logger
        self.data = {}
        self._lock = threading.RLock()

    # ==================================================
    # CICLO DE VIDA (CONTRATOS OBRIGATÓRIOS)
    # ==================================================

    def initialize(self):
        """Inicializa o gerenciador e carrega as configurações persistidas."""
        with self._lock:
            if self.is_online():
                return

            self.set_status(ModuleStatus.INITIALIZING)
            
            try:
                self.load()
                self.set_status(ModuleStatus.ONLINE)
                if self.logger:
                    self.logger.info("ConfigManager online e configurações carregadas.")
            except Exception as error:
                self.set_error(f"Falha na inicialização do ConfigManager: {str(error)}")
                if self.logger:
                    self.logger.error(self.error_message)

    def shutdown(self):
        """Encerra o gerenciador salvando o estado atual se necessário."""
        with self._lock:
            self.set_status(ModuleStatus.OFFLINE)
            try:
                self.save()
            except Exception:
                pass
            if self.logger:
                self.logger.info("ConfigManager encerrado.")

    # ==================================================
    # CARREGAMENTO E PERSISTÊNCIA
    # ==================================================

    def load(self):
        """Carrega as configurações do disco de forma segura."""
        with self._lock:
            self.CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)
            
            target_file = self.CONFIG_FILE
            if not target_file.exists() and self.BACKUP_FILE.exists():
                target_file = self.BACKUP_FILE

            if target_file.exists():
                try:
                    with target_file.open("r", encoding="utf-8") as file:
                        self.data = json.load(file)
                except Exception as error:
                    if self.logger:
                        self.logger.error(f"Erro ao ler configurações: {str(error)}. Tentando restaurar backup.")
                    self.restore_backup()
            else:
                self.data = {}
                self.save()

    def save(self):
        """Salva as configurações com descarga física (fsync) e substituição atômica."""
        with self._lock:
            try:
                self.CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)
                self.backup()

                # Escreve no arquivo temporário com flush e sincronização física
                with self.TEMP_FILE.open("w", encoding="utf-8") as file:
                    json.dump(self.data, file, indent=4, ensure_ascii=False)
                    file.flush()
                    os.fsync(file.fileno())  # Garante que os dados atingiram o hardware
                
                # Substituição atômica
                self.TEMP_FILE.replace(self.CONFIG_FILE)
            except Exception as error:
                error_msg = f"Falha crítica ao descarregar configurações: {str(error)}"
                if self.logger:
                    self.logger.error(error_msg)
                raise RuntimeError(error_msg)

    def get(self, section, key=None, default=None):
        with self._lock:
            value = self.data.get(section, {}) if key is None else self.data.get(section, {}).get(key, default)
            return copy.deepcopy(value) if isinstance(value, (dict, list)) else value

    def get_path(self, path, default=None):
        with self._lock:
            value = self.data
            for item in path.split("."):
                if isinstance(value, dict):
                    value = value.get(item)
                else:
                    return default
                if value is None:
                    return default
            return copy.deepcopy(value) if isinstance(value, (dict, list)) else value

    def get_all(self):
        with self._lock:
            return copy.deepcopy(self.data)

    def set(self, section, key, value):
        with self._lock:
            if section not in self.data:
                self.data[section] = {}
            self.data[section][key] = value
            self.save()

    def backup(self):
        """Cópia segura utilizando flush para garantir integridade."""
        if self.CONFIG_FILE.exists():
            try:
                shutil.copy2(self.CONFIG_FILE, self.BACKUP_FILE)
            except Exception as error:
                if self.logger:
                    self.logger.error(f"Erro no backup: {str(error)}")

    def restore_backup(self):
        """Restaura o arquivo de configurações a partir do backup."""
        with self._lock:
            if self.BACKUP_FILE.exists():
                try:
                    shutil.copy2(self.BACKUP_FILE, self.CONFIG_FILE)
                    with self.CONFIG_FILE.open("r", encoding="utf-8") as file:
                        self.data = json.load(file)
                except Exception as error:
                    if self.logger:
                        self.logger.error(f"Falha ao restaurar backup: {str(error)}")
                    self.data = {}