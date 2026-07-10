"""
=========================================
JARVIS CORE

Arquivo:
config_manager.py

Descrição:
Gerenciador de configurações do JARVIS.

Responsável por carregar, salvar e
controlar as configurações do sistema.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


import json

from pathlib import Path


from core.base.module import Module, ModuleStatus




class ConfigManager(Module):
    """
    Gerenciador das configurações do sistema.
    """



    CONFIG_FOLDER = Path("config")

    CONFIG_FILE = (
        CONFIG_FOLDER /
        "settings.json"
    )

    BACKUP_FILE = (
        CONFIG_FOLDER /
        "settings.backup.json"
    )




    def __init__(self, logger=None):

        super().__init__(
            "Config Manager"
        )


        self.logger = logger

        self.data = {}





    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):
        """
        Inicializa o sistema.
        """


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:


            self.CONFIG_FOLDER.mkdir(
                exist_ok=True
            )


            self._create_default_config()


            self.load()



            self.set_status(
                ModuleStatus.ONLINE
            )


            if self.logger:

                self.logger.success(
                    "Config Manager iniciado"
                )



        except Exception as error:


            self.set_error(
                str(error)
            )


            if self.logger:

                self.logger.error(
                    f"Erro no Config Manager: {error}"
                )





    def shutdown(self):
        """
        Finaliza o módulo.
        """


        try:

            self.save()



        except Exception as error:


            if self.logger:

                self.logger.error(
                    f"Falha ao salvar configurações: {error}"
                )



        self.set_status(
            ModuleStatus.OFFLINE
        )



        if self.logger:

            self.logger.info(
                "Config Manager encerrado"
            )





    # ==========================================================
    # Leitura e escrita
    # ==========================================================


    def load(self):
        """
        Carrega configurações.
        """


        if not self.CONFIG_FILE.exists():

            self._create_default_config()



        try:


            with self.CONFIG_FILE.open(
                "r",
                encoding="utf-8"
            ) as file:


                self.data = json.load(file)



        except json.JSONDecodeError:


            self._backup_config()


            self._create_default_config()


            with self.CONFIG_FILE.open(
                "r",
                encoding="utf-8"
            ) as file:


                self.data = json.load(file)





    def save(self):
        """
        Salva configurações.
        """


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





    # ==========================================================
    # API pública
    # ==========================================================


    def get(
        self,
        section,
        key,
        default=None
    ):
        """
        Retorna uma configuração.
        """


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





    def set(
        self,
        section,
        key,
        value
    ):
        """
        Atualiza uma configuração.
        """


        if section not in self.data:


            self.data[section] = {}



        self.data[section][key] = value



    def get_all(self):
        """
        Retorna todas as configurações.
        """


        return self.data





    # ==========================================================
    # Internos
    # ==========================================================


    def _create_default_config(self):
        """
        Cria configuração inicial.
        """


        if self.CONFIG_FILE.exists():

            return



        default = {


            "system": {

                "name": "JARVIS",

                "version":
                    "Mark I - Heartbeat",

                "language":
                    "pt-BR",

                "debug":
                    True

            },


            "user": {

                "name":
                    "Caio"

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


            "memory": {

                "enabled":
                    False

            },


            "personality": {

                "name":
                    "Rafiki",

                "mode":
                    "advisor"

            }

        }



        with self.CONFIG_FILE.open(
            "w",
            encoding="utf-8"
        ) as file:


            json.dump(
                default,
                file,
                indent=4,
                ensure_ascii=False
            )





    def _backup_config(self):
        """
        Faz backup de configuração corrompida.
        """


        if self.CONFIG_FILE.exists():

            self.CONFIG_FILE.replace(
                self.BACKUP_FILE
            )