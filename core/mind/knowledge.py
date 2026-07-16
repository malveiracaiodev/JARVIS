"""
=========================================
JARVIS CORE

Arquivo:
core/mind/knowledge.py

Descrição:
Biblioteca estruturada de conhecimento
semântico do Genesis Core.

Responsável por armazenar:
- Fatos
- Documentos
- Informações aprendidas
- Dados estruturados

Arquitetura:
Genesis Core

Mark:
III - Matrix

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



class Knowledge(Module):
    """
    Memória semântica estática do Genesis Core.
    """



    def __init__(
        self
    ):


        super().__init__(
            "core.mind.knowledge"
        )


        self.version = (
            "Mark III"
        )


        self.folder = Path(
            "data"
        )


        self.file = (
            self.folder /
            "knowledge.json"
        )


        self.database = []


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
                "Knowledge ONLINE."
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
                "Knowledge finalizado."
            )


        return True



    # ==================================================
    # Logs
    # ==================================================


    def _log_safe(
        self,
        level,
        message
    ):


        if hasattr(
            self,
            "logger"
        ) and self.logger:


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
            f"[KNOWLEDGE] {message}"
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

                    self.database = []

                    self.save()

                    return



                with open(
                    self.file,
                    "r",
                    encoding="utf-8"
                ) as file:


                    self.database = json.load(
                        file
                    )



            except Exception as error:


                self.database = []


                self._log_safe(
                    "error",
                    str(error)
                )



    def save(
        self
    ):


        with self._lock:


            try:


                self.folder.mkdir(
                    exist_ok=True
                )


                with open(
                    self.file,
                    "w",
                    encoding="utf-8"
                ) as file:


                    json.dump(
                        self.database,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )


            except Exception as error:


                self._log_safe(
                    "error",
                    str(error)
                )



    # ==================================================
    # Conhecimento
    # ==================================================


    def add(
        self,
        topic,
        information,
        source="internal",
        tags=None
    ):


        with self._lock:


            entry = {


                "id":
                    str(uuid.uuid4()),


                "topic":
                    topic,


                "information":
                    information,


                "source":
                    source,


                "tags":
                    tags or [],


                "created_at":
                    datetime.now().isoformat()

            }



            self.database.append(
                entry
            )


            self.save()



            return entry



    # ==================================================
    # Busca
    # ==================================================


    def search(
        self,
        query,
        context=None
    ):


        query = (
            query.lower()
            .strip()
        )


        results = []



        with self._lock:


            for item in self.database:


                text = (

                    f"{item.get('topic','')} "

                    f"{item.get('information','')} "

                    f"{' '.join(item.get('tags',[]))}"

                ).lower()



                if query in text:

                    results.append(
                        item
                    )



        return results



    def get_topic(
        self,
        topic
    ):


        target = topic.lower().strip()



        with self._lock:


            for item in self.database:


                if item["topic"].lower().strip() == target:

                    return item



        return None



    # ==================================================
    # Remoção
    # ==================================================


    def remove(
        self,
        topic
    ):


        target = topic.lower().strip()



        with self._lock:


            old = len(
                self.database
            )



            self.database = [

                item

                for item in self.database

                if item["topic"].lower().strip()
                != target

            ]



            if len(self.database) != old:


                self.save()

                return True



        return False



    # ==================================================
    # Importação
    # ==================================================


    def import_text(
        self,
        path
    ):


        file = Path(
            path
        )


        if not file.exists():

            return False



        try:


            self.add(

                topic=file.stem,

                information=file.read_text(
                    encoding="utf-8"
                ),

                source=str(file)

            )


            return True



        except Exception as error:


            self._log_safe(
                "error",
                str(error)
            )


            return False



    # ==================================================
    # Estado
    # ==================================================


    def snapshot(
        self
    ):


        with self._lock:


            return {

                "entries":
                    len(self.database),

                "version":
                    self.version

            }



    def total_entries(
        self
    ):


        return len(
            self.database
        )



    def status(
        self
    ):


        return {


            "name":
                self.name,


            "version":
                self.version,


            "entries":
                len(self.database),


            "file":
                str(self.file)

        }