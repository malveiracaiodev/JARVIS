"""
=========================================
JARVIS CORE

Arquivo:
core/mind/memory.py

Descrição:
Sistema de memória episódica persistente
do Genesis Core.

Responsável por armazenar:
- Experiências
- Eventos
- Preferências
- Dados aprendidos

Arquitetura:
Genesis Core

Mark:
III - Cognitive Support Layer

Autor:
Caio Vitor Malveira
=========================================
"""


import json
import threading
import uuid


from pathlib import Path
from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)



class Memory(Module):

    """
    Memória episódica persistente.

    Não representa conhecimento.

    Representa experiências armazenadas.
    """



    def __init__(
        self
    ):

        super().__init__(
            "core.mind.memory"
        )


        self.version = (
            "Mark III"
        )


        self.folder = Path(
            "data"
        )


        self.file = (
            self.folder /
            "memory.json"
        )


        self.entries = []


        self._lock = threading.RLock()


        self.load()



    # ==================================================
    # Lifecycle
    # ==================================================


    def initialize(
        self
    ):


        with self._lock:

            self.set_status(
                ModuleStatus.INITIALIZING
            )


            self.load()


            self.set_status(
                ModuleStatus.ONLINE
            )


            self._log_safe(
                "success",
                "Memory ONLINE."
            )


        return True




    def shutdown(
        self
    ):


        with self._lock:


            self.save()


            self.set_status(
                ModuleStatus.OFFLINE
            )


            self._log_safe(
                "info",
                "Memory finalizada."
            )


        return True



    # ==================================================
    # Log
    # ==================================================


    def _log_safe(
        self,
        level,
        message
    ):


        if getattr(
            self,
            "logger",
            None
        ):


            method = getattr(
                self.logger,
                level,
                None
            )


            if callable(method):

                method(
                    f"[{self.name}] {message}"
                )

                return



        print(
            f"[MEMORY] {message}"
        )



    # ==================================================
    # Persistência
    # ==================================================


    def load(
        self
    ):


        with self._lock:


            try:


                self.folder.mkdir(
                    exist_ok=True
                )


                if not self.file.exists():

                    self.entries = []

                    self.save()

                    return



                with open(
                    self.file,
                    "r",
                    encoding="utf-8"
                ) as archive:


                    self.entries = json.load(
                        archive
                    )



            except Exception as error:


                self.entries = []


                self._log_safe(
                    "error",
                    str(error)
                )



    def save(
        self
    ):


        with self._lock:


            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as archive:


                json.dump(
                    self.entries,
                    archive,
                    indent=4,
                    ensure_ascii=False
                )



    # ==================================================
    # Armazenamento
    # ==================================================


    def store(
        self,
        data,
        memory_type="general",
        importance=1
    ):


        with self._lock:


            entry = {


                "id":
                    str(uuid.uuid4()),


                "type":
                    memory_type,


                "data":
                    data,


                "importance":
                    importance,


                "created_at":
                    datetime.now().isoformat()


            }



            self.entries.append(
                entry
            )


            self.save()



            return entry



    # ==================================================
    # Recuperação
    # ==================================================


    def retrieve(
        self,
        query
    ):


        query = query.lower().strip()


        result = []



        with self._lock:


            for item in self.entries:


                text = json.dumps(
                    item["data"],
                    ensure_ascii=False
                ).lower()



                if query in text:

                    result.append(
                        item
                    )



        return result



    def last(
        self,
        limit=10
    ):


        return self.entries[-limit:]



    def get(
        self,
        memory_id
    ):


        for item in self.entries:


            if item["id"] == memory_id:

                return item



        return None



    # ==================================================
    # Remoção
    # ==================================================


    def remove(
        self,
        memory_id
    ):


        with self._lock:


            old = len(
                self.entries
            )



            self.entries = [

                item

                for item in self.entries

                if item["id"] != memory_id

            ]



            if len(self.entries) != old:


                self.save()

                return True



        return False



    def clear(
        self
    ):


        with self._lock:


            self.entries.clear()

            self.save()



    # ==================================================
    # Estado
    # ==================================================


    def snapshot(
        self
    ):


        return {

            "total":
                len(self.entries),

            "version":
                self.version

        }



    def status(
        self
    ):


        return {

            "name":
                self.name,

            "version":
                self.version,

            "memories":
                len(self.entries),

            "file":
                str(self.file)

        }