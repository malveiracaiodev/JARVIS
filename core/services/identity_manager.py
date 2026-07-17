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


from core.base.module import (
    Module,
    ModuleStatus
)


class IdentityManager(Module):
    """
    Gerenciador central de identidade do Genesis Core.

    Responsável por manter:
    - Identidade do sistema
    - Personas
    - Propósitos
    - Características comportamentais
    """


    def __init__(
        self,
        logger=None,
        event_bus=None
    ):
        super().__init__("core.identity_manager")

        self.version = "3.0"

        self.logger = logger
        self.event_bus = event_bus

        self.identity = {}

        self.file = Path(
            "data/personas/identity.json"
        )

        self._lock = threading.RLock()



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
                "Identity Manager Mark III iniciado."
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
            "Identity Manager encerrado."
        )



    # ======================================================
    # PERSISTÊNCIA
    # ======================================================


    def load_identity(self):

        with self._lock:


            if not self.file.exists():

                self.identity = (
                    self.default_identity()
                )

                self.save_identity()

                return



            try:

                with open(
                    self.file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.identity = json.load(file)


                self.log_info(
                    "Identidade carregada."
                )


            except (
                json.JSONDecodeError,
                TypeError
            ):


                backup = (
                    self.file.parent /
                    (
                        "corrupted_identity_"
                        +
                        datetime.now()
                        .strftime("%Y%m%d_%H%M%S")
                        +
                        ".json"
                    )
                )


                shutil.copy(
                    self.file,
                    backup
                )


                self.identity = (
                    self.default_identity()
                )


                self.save_identity()


                self.log_error(
                    "Identidade corrompida. "
                    f"Backup criado: {backup.name}"
                )



    def save_identity(self):

        with self._lock:


            self.file.parent.mkdir(
                parents=True,
                exist_ok=True
            )


            temp_file = (
                self.file.with_suffix(".tmp")
            )


            try:


                with open(
                    temp_file,
                    "w",
                    encoding="utf-8"
                ) as file:


                    json.dump(
                        self.identity,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )


                    file.flush()

                    os.fsync(
                        file.fileno()
                    )



                temp_file.replace(
                    self.file
                )



            except Exception as error:


                if temp_file.exists():

                    temp_file.unlink()



                self.log_error(
                    f"Erro ao salvar identidade: {error}"
                )


                raise



    # ======================================================
    # IDENTIDADE PADRÃO
    # ======================================================


    def default_identity(self):

        return {

            "system": "Genesis Core",

            "name": "JARVIS",

            "creator":
                "Caio Vitor Malveira",


            "version":
                "Mark III - Matrix",


            "purpose": [

                "Auxiliar o usuário",

                "Organizar informações",

                "Gerenciar tarefas",

                "Aprender novos conhecimentos",

                "Controlar recursos autorizados"

            ],



            "agents": {


                "jarvis": {

                    "name":
                        "JARVIS",

                    "role":
                        "Assistente técnico inteligente",

                    "style":
                        "analítico"

                },


                "rafiki": {

                    "name":
                        "Rafiki",

                    "role":
                        "Conselheiro pessoal",

                    "style":
                        "empático"

                }


            },



            "personality": {

                "tone":
                    "amigável",

                "behavior":
                    "assistente inteligente"

            }


        }



    # ======================================================
    # CONSULTA
    # ======================================================


    def get(
        self,
        key,
        default=None
    ):

        with self._lock:

            return self.identity.get(
                key,
                default
            )



    def get_full_identity(self):

        with self._lock:

            return copy.deepcopy(
                self.identity
            )



    def get_agent_identity(
        self,
        agent_name
    ):

        with self._lock:

            agents = self.identity.get(
                "agents",
                {}
            )


            return copy.deepcopy(
                agents.get(
                    agent_name,
                    {}
                )
            )



    def introduce(self):

        with self._lock:


            purposes = "\n".join(
                [
                    f"- {item}"
                    for item in
                    self.identity.get(
                        "purpose",
                        []
                    )
                ]
            )


            return (

                f"Olá.\n"
                f"Eu sou {self.get('name')}.\n"
                f"Fui criado por "
                f"{self.get('creator')}.\n\n"

                f"Meu propósito é:\n"
                f"{purposes}\n\n"

                f"Versão: "
                f"{self.get('version')}\n\n"

                "Estou online e pronto para auxiliar."

            )



    def who_am_i(self):

        return self.introduce()



    # ======================================================
    # EVENTOS E LOG
    # ======================================================


    def emit(
        self,
        event,
        *args,
        **kwargs
    ):

        if self.event_bus:

            try:

                self.event_bus.emit(
                    event,
                    *args,
                    **kwargs
                )

            except Exception:

                pass



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