"""
=========================================
GENESIS CORE

Arquivo:
core/base/module.py

Descrição:
Classe base universal para todos os módulos
do ecossistema Genesis.

Responsável por:
- Identidade
- Ciclo de vida
- Estado operacional
- Telemetria
- Diagnóstico
- Controle concorrente
- Metadados

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
import uuid

from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from enum import Enum


# ==========================================================
# STATUS GLOBAL DOS MÓDULOS
# ==========================================================

class ModuleStatus(Enum):

    OFFLINE = 0
    INITIALIZING = 1
    ONLINE = 2
    WARNING = 3
    ERROR = 4
    DISABLED = 5


# ==========================================================
# CLASSE BASE
# ==========================================================

class Module(ABC):

    """
    Classe base de todos os componentes Genesis.

    Exemplos:

    - Agents
    - Services
    - Managers
    - Cognitive Modules
    - Plugins
    """


    def __init__(
        self,
        name,
        description="",
        version="1.0",
        tags=None,
        capabilities=None,
        dependencies=None
    ):

        # ==================================================
        # IDENTIDADE
        # ==================================================

        self.id = str(uuid.uuid4())

        self.name = name

        self.description = description

        self.version = version


        # ==================================================
        # CLASSIFICAÇÃO
        # ==================================================

        self.tags = tags or []

        self.capabilities = capabilities or []

        self.dependencies = dependencies or []


        # ==================================================
        # CONTROLE
        # ==================================================

        self.enabled = True

        self.status = ModuleStatus.OFFLINE


        # ==================================================
        # TEMPO
        # ==================================================

        self.created_at = datetime.now()

        self.started_at = None

        self.stopped_at = None


        # ==================================================
        # ERROS
        # ==================================================

        self.error_message = None


        # ==================================================
        # MÉTRICAS
        # ==================================================

        self.metrics = {

            "starts": 0,

            "stops": 0,

            "errors": 0,

            "events": 0

        }


        # ==================================================
        # CONFIGURAÇÃO
        # ==================================================

        self.config = {}


        # ==================================================
        # LOCKS
        # ==================================================

        self._state_lock = threading.RLock()


        # ==================================================
        # HISTÓRICO
        # ==================================================

        self.status_history = deque(
            maxlen=200
        )


        self.status_history.append({

            "status": self.status.name,

            "time":
                self.created_at.isoformat()

        })


    # ==========================================================
    # CICLO DE VIDA
    # ==========================================================


    @abstractmethod
    def initialize(self):

        """
        Inicialização executada pelo Kernel.
        """

        pass



    @abstractmethod
    def shutdown(self):

        """
        Encerramento gracioso.
        """

        pass



    # ==========================================================
    # ESTADO
    # ==========================================================


    def set_status(self, status):

        if not isinstance(
            status,
            ModuleStatus
        ):
            raise ValueError(
                "Status inválido."
            )


        with self._state_lock:

            self.status = status


            self.status_history.append({

                "status":
                    status.name,

                "time":
                    datetime.now().isoformat()

            })


            if status == ModuleStatus.ONLINE:

                self.started_at = datetime.now()

                self.metrics["starts"] += 1



            elif status == ModuleStatus.OFFLINE:

                self.stopped_at = datetime.now()

                self.metrics["stops"] += 1



    def set_error(self, message):

        with self._state_lock:

            self.error_message = message

            self.metrics["errors"] += 1

            self.set_status(
                ModuleStatus.ERROR
            )



    def enable(self):

        with self._state_lock:

            self.enabled = True



    def disable(self):

        with self._state_lock:

            self.enabled = False

            self.set_status(
                ModuleStatus.DISABLED
            )



    # ==========================================================
    # CONSULTAS
    # ==========================================================


    def get_status(self):

        with self._state_lock:

            return self.status



    def is_online(self):

        return (
            self.get_status()
            ==
            ModuleStatus.ONLINE
        )



    def is_enabled(self):

        with self._state_lock:

            return self.enabled



    def has_error(self):

        return (
            self.get_status()
            ==
            ModuleStatus.ERROR
        )



    # ==========================================================
    # MÉTRICAS
    # ==========================================================


    def uptime(self):

        with self._state_lock:

            if not self.started_at:

                return 0


            return (
                datetime.now()
                -
                self.started_at
            ).total_seconds()



    def health(self):

        return {

            "name":
                self.name,

            "status":
                self.status.name,

            "enabled":
                self.enabled,

            "uptime":
                self.uptime(),

            "errors":
                self.metrics["errors"]

        }



    # ==========================================================
    # EVENTOS
    # ==========================================================


    def register_event(self):

        with self._state_lock:

            self.metrics["events"] += 1



    # ==========================================================
    # INFORMAÇÕES
    # ==========================================================


    def info(self):

        with self._state_lock:

            return {


                "id":
                    self.id,


                "name":
                    self.name,


                "description":
                    self.description,


                "version":
                    self.version,


                "status":
                    self.status.name,


                "enabled":
                    self.enabled,


                "tags":
                    self.tags,


                "capabilities":
                    self.capabilities,


                "dependencies":
                    self.dependencies,


                "created_at":
                    self.created_at.isoformat(),


                "started_at":
                    (
                        self.started_at.isoformat()
                        if self.started_at
                        else None
                    ),


                "uptime":
                    self.uptime(),


                "metrics":
                    self.metrics,


                "error":
                    self.error_message,


                "history":
                    list(self.status_history)

            }



    def __str__(self):

        return (
            f"{self.name}"
            f" [{self.status.name}]"
        )