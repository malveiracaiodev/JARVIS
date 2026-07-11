"""
=========================================
JARVIS CORE

Arquivo:
memory.py

Descrição:
Sistema de memória persistente.

Responsável por:
- Armazenar experiências
- Recuperar contexto
- Manter histórico
- Garantir compatibilidade
- Preparar memória semântica

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""

import json
from pathlib import Path
from datetime import datetime


class Memory:
    """
    Memória persistente do JARVIS.
    """

    def __init__(self):

        self.name = "Memory"

        self.version = "Mark II"

        self.folder = Path("data")

        self.file = self.folder / "memory.json"

        self.entries = []

        self.load()

    # ==========================================================
    # Inicialização
    # ==========================================================

    def initialize(self):

        self.load()

        print("[MEMORY] Sistema iniciado")

    def shutdown(self):

        self.save()

        print("[MEMORY] Sistema encerrado")

    # ==========================================================
    # Persistência
    # ==========================================================

    def load(self):

        self.folder.mkdir(exist_ok=True)

        if not self.file.exists():

            self.entries = []

            self.save()

            return

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as archive:

                data = json.load(archive)

        except Exception:

            self.entries = []

            return

        self.entries = []

        for item in data:

            self.entries.append(
                self._normalize(item)
            )

    def save(self):

        self.folder.mkdir(exist_ok=True)

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

    # ==========================================================
    # Compatibilidade
    # ==========================================================

    def _normalize(self, item):

        if "data" in item:

            return {

                "id": item.get(
                    "id",
                    len(self.entries) + 1
                ),

                "data": item["data"],

                "created_at": item.get(
                    "created_at",
                    item.get(
                        "created",
                        datetime.now().isoformat()
                    )
                )
            }

        return {

            "id": item.get(
                "id",
                len(self.entries) + 1
            ),

            "data": item,

            "created_at": item.get(
                "timestamp",
                item.get(
                    "created",
                    datetime.now().isoformat()
                )
            )
        }

    # ==========================================================
    # Armazenamento
    # ==========================================================

    def store(
        self,
        data
    ):

        entry = {

            "id": len(self.entries) + 1,

            "data": data,

            "created_at": datetime.now().isoformat()

        }

        self.entries.append(entry)

        self.save()

        return entry

    # ==========================================================
    # Recuperação
    # ==========================================================

    def retrieve(
        self,
        query
    ):

        query = query.lower()

        results = []

        for item in self.entries:

            text = json.dumps(
                item["data"],
                ensure_ascii=False
            ).lower()

            if query in text:

                results.append(item)

        return results

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

    # ==========================================================
    # Remoção
    # ==========================================================

    def remove(
        self,
        memory_id
    ):

        before = len(self.entries)

        self.entries = [

            item

            for item in self.entries

            if item["id"] != memory_id

        ]

        self.save()

        return before != len(self.entries)

    def clear(self):

        self.entries = []

        self.save()

    # ==========================================================
    # Estatísticas
    # ==========================================================

    def status(self):

        return {

            "name": self.name,

            "version": self.version,

            "memories": len(self.entries),

            "file": str(self.file)

        }