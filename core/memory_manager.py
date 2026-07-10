"""
=========================================
JARVIS CORE

Arquivo:
memory_manager.py

Descrição:
Sistema de memória operacional
do JARVIS.

Responsável por armazenar eventos,
informações e histórico do sistema.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


import json

from datetime import datetime

from pathlib import Path


from core.base.module import (
    Module,
    ModuleStatus
)


from core.events import MemoryEvents





class MemoryManager(Module):
    """
    Gerenciador da memória do JARVIS.
    """



    MEMORY_FOLDER = Path(
        "data"
    )


    MEMORY_FILE = (
        MEMORY_FOLDER /
        "memory.json"
    )





    def __init__(
        self,
        logger,
        event_bus
    ):

        super().__init__(
            "Memory Manager"
        )


        self.logger = logger

        self.event_bus = event_bus


        self.memories = []





    # ==========================================================
    # Inicialização
    # ==========================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.MEMORY_FOLDER.mkdir(
            exist_ok=True
        )


        self.load()



        self.event_bus.subscribe(
            MemoryEvents.SEARCH,
            self.search
        )



        self.set_status(
            ModuleStatus.ONLINE
        )



        self.logger.success(
            "Memory Manager iniciado"
        )





    # ==========================================================
    # Encerramento
    # ==========================================================


    def shutdown(self):


        self.save()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.logger.info(
            "Memory Manager encerrado"
        )





    # ==========================================================
    # Memória
    # ==========================================================


    def remember(
        self,
        event,
        message
    ):

        memory = {


            "event": event,


            "message": message,


            "timestamp":
                datetime.now()
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        }



        self.memories.append(
            memory
        )


        self.event_bus.emit(
            MemoryEvents.CREATED,
            memory
        )


        self.save()

    def last_events(
        self,
        limit=10
    ):


        return (
            self.memories[-limit:]
        )





    def search(
        self,
        text
    ):


        result = []


        for memory in self.memories:


            if text.lower() in (
                memory["message"]
                .lower()
            ):

                result.append(
                    memory
                )



        return result





    # ==========================================================
    # Arquivo
    # ==========================================================


    def load(self):
        """
        Carrega as memórias salvas.
        """


        if not self.MEMORY_FILE.exists():

            self.memories = []

            self.logger.info(
                "Nenhuma memória encontrada. Criando memória inicial."
            )

            return



        with open(
            self.MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:


            self.memories = json.load(
                file
            )



        self.logger.info(
            f"Memórias carregadas: {len(self.memories)}"
        )


        self.event_bus.emit(
            MemoryEvents.LOADED
        )




    def save(self):


        with open(
            self.MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:


            json.dump(

                self.memories,

                file,

                indent=4,

                ensure_ascii=False

            )


        self.event_bus.emit(
            MemoryEvents.SAVED
        )