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
II.1 - Evolution (Patch 2.2 - Robust Storage)

Autor:
Caio Vitor Malveira
=========================================
"""

import json
import shutil
import threading
from pathlib import Path
from core.base.module import (
    Module,
    ModuleStatus
)


class ConfigManager(Module):
    """
    Serviço central de configuração com persistência atômica e segura do JARVIS.
    """

    CONFIG_VERSION = 1

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    CONFIG_FOLDER = ROOT_DIR / "config"
    CONFIG_FILE = CONFIG_FOLDER / "settings.json"
    BACKUP_FILE = CONFIG_FOLDER / "settings.backup.json"
    TEMP_FILE = CONFIG_FOLDER / "settings.tmp.json"

    def __init__(self, logger=None):
        super().__init__("core.config_manager")
        self.version = "2.2"
        self.logger = logger
        self.data = {}
        
        # Lock de exclusão mútua para sincronizar E/S em disco e acessos em memória
        self._lock = threading.Lock()

    # ==========================================================
    # Ciclo de Vida
    # ==========================================================

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        try:
            with self._lock:
                self.CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)
                self.create_default()
                self._load_internal()

            self.set_status(ModuleStatus.ONLINE)
            self.success("Config Manager iniciado com persistência isolada")
        except Exception as error:
            # Compatibilidade com a assinatura set_error do core base se aplicável
            if hasattr(self, "set_error"):
                self.set_error(str(error))
            self.error(f"Erro fatal na inicialização do ConfigManager: {str(error)}")

    def shutdown(self):
        self.save()
        self.set_status(ModuleStatus.OFFLINE)
        self.info("Config Manager encerrado e dados descarregados em disco")

    # ==========================================================
    # Arquivo e Persistência Atômica
    # ==========================================================

    def _load_internal(self):
        """Método privado para carregamento interno (deve rodar sob escopo de lock)."""
        if not self.CONFIG_FILE.exists():
            self._restore_default_internal()

        try:
            with self.CONFIG_FILE.open("r", encoding="utf-8") as file:
                self.data = json.load(file)
            self.check_version()
        except (json.JSONDecodeError, ValueError):
            self.error("Arquivo de configuração corrompido. Tentando restaurar do backup...")
            self._recover_from_backup()

    def load(self):
        with self._lock:
            self._load_internal()

    def save(self):
        """Salva as configurações de forma atômica para evitar arquivos corrompidos por interrupções."""
        with self._lock:
            try:
                self.CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)
                
                # Gera primeiro um backup rápido do arquivo íntegro atual
                self.backup()

                # Escreve no arquivo temporário primeiro
                with self.TEMP_FILE.open("w", encoding="utf-8") as file:
                    json.dump(self.data, file, indent=4, ensure_ascii=False)
                
                # Substituição atômica no sistema de arquivos (evita zerar se a energia cair no dump)
                self.TEMP_FILE.replace(self.CONFIG_FILE)
            except Exception as error:
                self.error(f"Falha ao descarregar configurações em disco: {str(error)}")

    def reload(self):
        with self._lock:
            self._load_internal()
            self.info("Configurações recarregadas com sucesso")

    def _recover_from_backup(self):
        """Tenta recuperar dados do arquivo de backup. Em último caso, recria o padrão."""
        if self.BACKUP_FILE.exists():
            try:
                with self.BACKUP_FILE.open("r", encoding="utf-8") as file:
                    self.data = json.load(file)
                self.check_version()
                # Salva a versão recuperada de volta na trilha principal
                with self.CONFIG_FILE.open("w", encoding="utf-8") as file:
                    json.dump(self.data, file, indent=4, ensure_ascii=False)
                self.success("Configuração recuperada com sucesso através do Backup local")
                return
            except Exception:
                self.error("Arquivo de backup também está corrompido.")
        
        self.error("Restaurando configurações para o padrão de fábrica.")
        self._restore_default_internal()

    # ==========================================================
    # Interface de API Externa
    # ==========================================================

    def get(self, section, key=None, default=None):
        with self._lock:
            if key is None:
                return self.data.get(section, default)
            return self.data.get(section, {}).get(key, default)

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
            return value

    def set(self, section, key, value, save=False):
        with self._lock:
            if section not in self.data:
                self.data[section] = {}
            self.data[section][key] = value
            if save:
                self.save()

    def update(self, section, key, value):
        self.set(section, key, value, save=True)

    def get_all(self):
        with self._lock:
            return dict(self.data)

    # ==========================================================
    # Versionamento e Migrações
    # ==========================================================

    def check_version(self):
        version = self.data.get("config_version", 0)
        if version < self.CONFIG_VERSION:
            self.migrate(version)

    def migrate(self, old_version):
        self.data["config_version"] = self.CONFIG_VERSION
        self.save()
        self.info(f"Esquema de configuração migrado da v{old_version} para a v{self.CONFIG_VERSION}")

    # ==========================================================
    # Inicialização Padrão
    # ==========================================================

    def create_default(self):
        if self.CONFIG_FILE.exists():
            return
        self._restore_default_internal()

    def _restore_default_internal(self):
        """Implementação privada de restauração de fábrica padrão."""
        default = {
            "config_version": self.CONFIG_VERSION,
            "system": {
                "name": "JARVIS",
                "version": "Mark II - Genesis",
                "language": "pt-BR",
                "debug": True
            },
            "user": {
                "name": "Caio"
            },
            "mind": {
                "enabled": True,
                "memory": True,
                "reasoning": True
            },
            "memory": {
                "enabled": True,
                "path": "data/memory"
            },
            "knowledge": {
                "enabled": True,
                "path": "data/knowledge"
            },
            "voice": {
                "enabled": False
            },
            "ai": {
                "enabled": False,
                "provider": "none"
            },
            "plugins": {
                "enabled": True,
                "path": "plugins"
            },
            "runtime": {
                "workers": 1
            },
            "personality": {
                "name": "Rafiki",
                "mode": "advisor"
            }
        }
        self.data = default
        
        # Garante a escrita imediata
        self.CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)
        with self.CONFIG_FILE.open("w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def restore_default(self):
        with self._lock:
            self._restore_default_internal()

    # ==========================================================
    # Rotinas de Backup Manual/Automático
    # ==========================================================

    def backup(self):
        """Duplica o arquivo ativo para o destino de backup se ele existir em estado íntegro."""
        if self.CONFIG_FILE.exists():
            try:
                shutil.copy2(self.CONFIG_FILE, self.BACKUP_FILE)
            except Exception as error:
                self.error(f"Não foi possível criar o arquivo de backup: {str(error)}")

    # ==========================================================
    # Logs Redirecionados
    # ==========================================================

    def info(self, message):
        if self.logger:
            self.logger.info(message)

    def success(self, message):
        if self.logger:
            self.logger.success(message)

    def error(self, message):
        if self.logger:
            self.logger.error(message)