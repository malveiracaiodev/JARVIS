"""
=========================================
JARVIS CORE

Arquivo:
knowledge.py

Descrição:
Sistema de conhecimento do JARVIS.

Responsável por:
- Armazenar conhecimento
- Pesquisar informações
- Importar documentos
- Gerenciar fontes
- Preparar integração com IA

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

from pathlib import Path
from datetime import datetime
import json


class Knowledge:
    """
    Biblioteca de conhecimento do JARVIS.

    Armazena informações estruturadas que
    poderão ser utilizadas pelo Brain.
    """

    def __init__(self):

        self.name = "Knowledge"

        self.version = "Mark II"

        self.folder = Path("data")

        self.file = self.folder / "knowledge.json"

        self.database = []

        self.load()

    # ==========================================================
    # Inicialização
    # ==========================================================

    def initialize(self):

        self.load()

        print("[KNOWLEDGE] Sistema iniciado")

    def shutdown(self):

        self.save()

        print("[KNOWLEDGE] Sistema encerrado")

    # ==========================================================
    # Persistência
    # ==========================================================

    def load(self):

        self.folder.mkdir(exist_ok=True)

        if not self.file.exists():

            self.database = []

            self.save()

            return

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as file:

                self.database = json.load(file)

        except Exception:

            self.database = []

    def save(self):

        self.folder.mkdir(exist_ok=True)

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

    # ==========================================================
    # Conhecimento
    # ==========================================================

    def add(
        self,
        topic,
        information,
        source="internal",
        tags=None
    ):

        entry = {

            "id": len(self.database) + 1,

            "topic": topic,

            "information": information,

            "source": source,

            "tags": tags or [],

            "created_at": datetime.now().isoformat()

        }

        self.database.append(entry)

        self.save()

        return entry

    def search(
        self,
        query
    ):

        query = query.lower()

        results = []

        for item in self.database:

            text = (

                f"{item.get('topic','')} "

                f"{item.get('information','')} "

                f"{' '.join(item.get('tags',[]))}"

            ).lower()

            if query in text:

                results.append(item)

        return results

    def get_topic(
        self,
        topic
    ):

        topic = topic.lower()

        for item in self.database:

            if item["topic"].lower() == topic:

                return item

        return None

    def remove(
        self,
        topic
    ):

        topic = topic.lower()

        before = len(self.database)

        self.database = [

            item

            for item in self.database

            if item["topic"].lower() != topic

        ]

        self.save()

        return len(self.database) != before

    # ==========================================================
    # Importação
    # ==========================================================

    def import_text(
        self,
        path
    ):

        file = Path(path)

        if not file.exists():

            return False

        text = file.read_text(
            encoding="utf-8"
        )

        self.add(

            topic=file.stem,

            information=text,

            source=str(file)

        )

        return True

    # ==========================================================
    # Estatísticas
    # ==========================================================

    def total_entries(self):

        return len(self.database)

    def status(self):

        return {

            "name": self.name,

            "version": self.version,

            "entries": len(self.database),

            "file": str(self.file)

        }