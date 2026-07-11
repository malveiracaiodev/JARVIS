"""
=========================================
JARVIS CORE

Arquivo:
config_manager.py

Descrição:
Gerenciador central de configurações.

Responsável por:
- Carregar configurações
- Salvar configurações
- Controle de parâmetros do sistema
- Persistência de estado
- Evolução de configurações

Arquitetura:
Genesis Core

Mark:
II.1 - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


import json
import shutil


from pathlib import Path


from core.base.module import (
    Module,
    ModuleStatus
)





class ConfigManager(Module):


    """
    Serviço central de configuração do JARVIS.
    """



    CONFIG_VERSION = 1



    ROOT_DIR = (
        Path(__file__)
        .resolve()
        .parent
        .parent
        .parent
    )



    CONFIG_FOLDER = (
        ROOT_DIR /
        "config"
    )



    CONFIG_FILE = (
        CONFIG_FOLDER /
        "settings.json"
    )



    BACKUP_FILE = (
        CONFIG_FOLDER /
        "settings.backup.json"
    )





    def __init__(
        self,
        logger=None
    ):


        super().__init__(
            "core.config_manager"
        )


        self.version = "2.1"


        self.logger = logger


        self.data = {}








    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:


            self.CONFIG_FOLDER.mkdir(
                exist_ok=True
            )


            self.create_default()


            self.load()



            self.set_status(
                ModuleStatus.ONLINE
            )


            self.log_success(
                "Config Manager iniciado"
            )



        except Exception as error:


            self.set_error(
                str(error)
            )


            self.log_error(
                str(error)
            )







    def shutdown(self):


        self.save()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Config Manager encerrado"
        )








    # ==========================================================
    # Arquivo
    # ==========================================================


    def load(self):


        if not self.CONFIG_FILE.exists():

            self.create_default()



        try:


            with self.CONFIG_FILE.open(
                "r",
                encoding="utf-8"
            ) as file:


                self.data = json.load(
                    file
                )



            self.check_version()



        except json.JSONDecodeError:


            self.log_error(
                "Configuração corrompida"
            )


            self.backup()


            self.restore_default()



        except Exception as error:


            self.log_error(
                str(error)
            )







    def save(self):


        self.CONFIG_FOLDER.mkdir(
            exist_ok=True
        )



        with self.CONFIG_FILE.open(
            "w",
            encoding="utf-8"
        ) as file:


            json.dump(

                self.data,

                file,

                indent=4,

                ensure_ascii=False

            )








    def reload(self):


        self.load()


        self.log_info(
            "Configurações recarregadas"
        )







    # ==========================================================
    # API
    # ==========================================================


    def get(
        self,
        section,
        key=None,
        default=None
    ):


        if key is None:


            return self.data.get(
                section,
                default
            )



        return (

            self.data

            .get(
                section,
                {}
            )

            .get(
                key,
                default
            )

        )







    def get_path(
        self,
        path,
        default=None
    ):


        value = self.data



        for item in path.split("."):


            if isinstance(value, dict):


                value = value.get(
                    item
                )


            else:


                return default



            if value is None:


                return default



        return value







    def set(
        self,
        section,
        key,
        value,
        save=False
    ):


        if section not in self.data:


            self.data[section] = {}



        self.data[section][key] = value



        if save:


            self.save()








    def update(
        self,
        section,
        key,
        value
    ):


        self.set(
            section,
            key,
            value,
            save=True
        )



    def get_all(self):


        return self.data







    # ==========================================================
    # Versão
    # ==========================================================


    def check_version(self):


        version = self.data.get(
            "config_version",
            0
        )


        if version < self.CONFIG_VERSION:


            self.migrate(
                version
            )







    def migrate(
        self,
        old_version
    ):


        self.data["config_version"] = (
            self.CONFIG_VERSION
        )


        self.save()


        self.log_info(
            "Configuração migrada"
        )







    # ==========================================================
    # Configuração padrão
    # ==========================================================


    def create_default(self):


        if self.CONFIG_FILE.exists():

            return



        self.restore_default()







    def restore_default(self):


        default = {


            "config_version":
            self.CONFIG_VERSION,



            "system": {


                "name":
                "JARVIS",


                "version":
                "Mark II - Genesis",


                "language":
                "pt-BR",


                "debug":
                True


            },



            "user": {


                "name":
                "Caio"


            },



            "mind": {


                "enabled":
                True,


                "memory":
                True,


                "reasoning":
                True


            },



            "memory": {


                "enabled":
                True,


                "path":
                "data/memory"


            },



            "knowledge": {


                "enabled":
                True,


                "path":
                "data/knowledge"


            },



            "voice": {


                "enabled":
                False


            },



            "ai": {


                "enabled":
                False,


                "provider":
                "none"


            },



            "plugins": {


                "enabled":
                True,


                "path":
                "plugins"


            },



            "runtime": {


                "workers":
                1


            },



            "personality": {


                "name":
                "Rafiki",


                "mode":
                "advisor"


            }


        }



        self.data = default


        self.save()







    # ==========================================================
    # Backup
    # ==========================================================


    def backup(self):


        if self.CONFIG_FILE.exists():


            shutil.copy2(

                self.CONFIG_FILE,

                self.BACKUP_FILE

            )








    # ==========================================================
    # Logs
    # ==========================================================


    def log_info(
        self,
        message
    ):


        if self.logger:


            self.logger.info(
                message
            )





    def log_success(
        self,
        message
    ):


        if self.logger:


            self.logger.success(
                message
            )





    def log_error(
        self,
        message
    ):


        if self.logger:


            self.logger.error(
                message
            )