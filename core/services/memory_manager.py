"""
=========================================
JARVIS CORE

Arquivo:
core/services/memory_manager.py

Descrição:
Gerenciador central da memória do Genesis Core.

Responsável por:
- Persistência segura de memórias
- Histórico cognitivo
- Busca thread-safe
- Recuperação contra corrupção
- Comunicação com EventBus

Arquitetura:
Genesis Core

Mark:
III - Matrix (Memory Layer)

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


from core.events import MemoryEvents



class MemoryManager(Module):
    """
    Serviço responsável pela memória persistente
    do Genesis Core.
    """



    MEMORY_FOLDER = Path(
        "data/memory"
    )


    MEMORY_FILE = (
        MEMORY_FOLDER /
        "long_term.json"
    )



    def __init__(
        self,
        logger=None,
        event_bus=None
    ):

        super().__init__(
            "core.memory_manager"
        )


        self.version = "3.0"


        self.logger = logger

        self.event_bus = event_bus


        self.memories = []


        self._lock = threading.RLock()



    # ==========================================================
    # CICLO DE VIDA
    # ==========================================================


    def initialize(self):

        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:


            self.MEMORY_FOLDER.mkdir(
                parents=True,
                exist_ok=True
            )


            self.load()



            self.set_status(
                ModuleStatus.ONLINE
            )



            self.log_success(
                "Memory Manager Mark III ONLINE."
            )



        except Exception as error:


            self.set_error(
                str(error)
            )


            self.log_error(
                str(error)
            )





    def shutdown(self):

        try:

            self.save()


        except Exception:

            pass



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Memory Manager encerrado."
        )



    # ==========================================================
    # MEMÓRIA
    # ==========================================================


    def remember(
        self,
        content,
        memory_type="experience",
        importance=1
    ):


        with self._lock:


            next_id = (

                max(
                    [
                        memory.get(
                            "id",
                            0
                        )

                        for memory in self.memories
                    ],

                    default=0

                )

                + 1

            )



            memory = {


                "id":
                    next_id,


                "type":
                    memory_type,


                "content":
                    content,


                "importance":
                    importance,


                "created":
                    datetime.now()
                    .isoformat(),


                "access_count":
                    0


            }



            self.memories.append(
                memory
            )


            self.emit(
                MemoryEvents.CREATED,
                memory
            )


            self.save()



            return copy.deepcopy(
                memory
            )





    def last_events(
        self,
        limit=10
    ):


        with self._lock:


            return copy.deepcopy(
                self.memories[-limit:]
            )





    def search(
        self,
        text
    ):


        if not text:

            return []



        target = (
            str(text)
            .lower()
        )


        results = []



        with self._lock:


            for memory in self.memories:


                content = (

                    str(
                        memory.get(
                            "content",
                            ""
                        )

                    )

                    .lower()

                )



                if target in content:


                    memory["access_count"] = (

                        memory.get(
                            "access_count",
                            0
                        )

                        + 1

                    )


                    results.append(
                        copy.deepcopy(memory)
                    )



        return results



    # ==========================================================
    # PERSISTÊNCIA
    # ==========================================================



    def load(self):

        with self._lock:


            if not self.MEMORY_FILE.exists():


                self.memories = []


                self.log_info(
                    "Memória inexistente. Criando estrutura vazia."
                )


                return



            try:


                with open(
                    self.MEMORY_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:


                    self.memories = json.load(
                        file
                    )



                self.log_info(
                    f"Memórias carregadas: {len(self.memories)}"
                )


                self.emit(
                    MemoryEvents.LOADED
                )



            except (
                json.JSONDecodeError,
                TypeError
            ):



                backup_path = (

                    self.MEMORY_FOLDER /

                    (
                        "corrupted_memory_"

                        +

                        datetime.now()
                        .strftime(
                            "%Y%m%d_%H%M%S"
                        )

                        +

                        ".json"

                    )

                )



                shutil.copy(
                    self.MEMORY_FILE,
                    backup_path
                )



                self.memories = []



                self.log_error(
                    "Memória corrompida. "
                    f"Backup criado: {backup_path.name}"
                )



                self.emit(
                    MemoryEvents.LOADED
                )





    def save(self):

        with self._lock:



            temp_file = (

                self.MEMORY_FILE
                .with_suffix(".tmp")

            )



            try:


                with open(
                    temp_file,
                    "w",
                    encoding="utf-8"
                ) as file:



                    json.dump(

                        self.memories,

                        file,

                        indent=4,

                        ensure_ascii=False

                    )



                    file.flush()


                    os.fsync(
                        file.fileno()
                    )



                temp_file.replace(
                    self.MEMORY_FILE
                )



                self.emit(
                    MemoryEvents.SAVED
                )



            except Exception as error:



                if temp_file.exists():

                    temp_file.unlink()



                self.log_error(
                    f"Falha salvando memória: {error}"
                )


                raise





    # ==========================================================
    # EVENTOS E LOG
    # ==========================================================


    def emit(
        self,
        event,
        *args
    ):


        if self.event_bus:


            try:

                self.event_bus.emit(
                    event,
                    *args
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