"""
=========================================
JARVIS CORE

Arquivo:
identity_manager.py

Descrição:
Sistema de identidade do JARVIS.

Responsável por:
- Carregar identidade
- Definir propósito
- Fornecer informações do agente

Arquitetura:
Genesis Core

Mark:
II - Identity Layer

Autor:
Caio Vitor Malveira
=========================================
"""


import json


from pathlib import Path



from core.base.module import (
    Module,
    ModuleStatus
)





class IdentityManager(Module):


    """
    Gerenciador da identidade
    do sistema.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None
    ):


        super().__init__(
            "core.identity_manager"
        )


        self.version = "2.0"


        self.logger = logger


        self.event_bus = event_bus


        self.identity = {}



        self.file = Path(
            "personas/identity.json"
        )






    # ======================================================
    # CICLO DE VIDA
    # ======================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:


            self.load_identity()



            self.set_status(
                ModuleStatus.ONLINE
            )



            self.emit(
                "IDENTITY_LOADED"
            )


            self.log_success(
                "Identity Manager iniciado"
            )



        except Exception as error:


            self.set_error(
                str(error)
            )



            self.log_error(
                str(error)
            )








    def shutdown(self):


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Identity Manager encerrado"
        )








    # ======================================================
    # CARREGAMENTO
    # ======================================================


    def load_identity(self):


        if not self.file.exists():


            self.identity = self.default_identity()


            self.save_identity()


            return






        with open(

            self.file,

            "r",

            encoding="utf-8"

        ) as file:


            self.identity = json.load(
                file
            )



        self.log_info(
            "Identidade carregada"
        )








    def save_identity(self):


        self.file.parent.mkdir(
            exist_ok=True
        )



        with open(

            self.file,

            "w",

            encoding="utf-8"

        ) as file:


            json.dump(

                self.identity,

                file,

                indent=4,

                ensure_ascii=False

            )








    # ======================================================
    # IDENTIDADE PADRÃO
    # ======================================================


    def default_identity(self):


        return {


            "name":
            "JARVIS",


            "creator":
            "Caio Vitor Malveira",


            "version":
            "Mark II - Genesis",


            "purpose":
            [

                "Auxiliar o usuário",

                "Organizar informações",

                "Gerenciar tarefas",

                "Aprender novos conhecimentos"

            ],


            "personality":
            {

                "style":
                "assistente inteligente",

                "tone":
                "amigável"

            }


        }








    # ======================================================
    # CONSULTA
    # ======================================================


    def get(
        self,
        key
    ):


        return self.identity.get(
            key
        )





    def get_full_identity(self):


        return self.identity







    def introduce(self):


        return f"""

Olá.

Eu sou {self.get('name')}.


Fui criado por
{self.get('creator')}.


Meu propósito é:


{', '.join(self.get('purpose', []))}


Versão:

{self.get('version')}


Sistema operacional.

"""








    def who_am_i(self):


        return self.introduce()







    # ======================================================
    # EVENTOS E LOG
    # ======================================================


    def emit(
        self,
        event
    ):


        if self.event_bus:


            self.event_bus.emit(
                event
            )



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