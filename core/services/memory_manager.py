"""
=========================================
JARVIS CORE

Arquivo:
memory_manager.py

Descrição:
Gerenciador de armazenamento da memória.

Responsável por:
- Persistência de dados
- Carregamento
- Histórico
- Eventos de memória

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



from core.base.module import (
    Module,
    ModuleStatus
)



from core.events import MemoryEvents





class MemoryManager(Module):


    """
    Serviço responsável pela persistência
    da memória do JARVIS.
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


        self.version = "2.0"


        self.logger = logger


        self.event_bus = event_bus


        self.memories = []






    # ==========================================================
    # Ciclo de vida
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



            if self.event_bus:


                self.event_bus.subscribe(

                    MemoryEvents.SEARCH,

                    self.search

                )



            self.set_status(
                ModuleStatus.ONLINE
            )


            self.log_success(
                "Memory Manager iniciado"
            )



        except Exception as error:


            self.set_error(
                str(error)
            )








    def shutdown(self):


        self.save()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Memory Manager encerrado"
        )








    # ==========================================================
    # Memória
    # ==========================================================


    def remember(
        self,
        content,
        memory_type="experience",
        importance=1
    ):


        memory = {


            "id":

            len(self.memories)+1,


            "type":

            memory_type,


            "content":

            content,


            "importance":

            importance,


            "created":

            datetime.now().isoformat()

        }



        self.memories.append(
            memory
        )


        self.emit(
            MemoryEvents.CREATED,
            memory
        )


        self.save()



        return memory






    def last_events(
        self,
        limit=10
    ):


        return self.memories[-limit:]







    def search(
        self,
        text
    ):


        result = []



        text = text.lower()



        for memory in self.memories:


            content = str(
                memory.get(
                    "content",
                    ""
                )
            ).lower()



            if text in content:


                result.append(
                    memory
                )



        return result







    # ==========================================================
    # Persistência
    # ==========================================================


    def load(self):


        if not self.MEMORY_FILE.exists():


            self.memories = []


            self.log_info(
                "Memória inicial criada"
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



        self.log_info(
            f"Memórias carregadas: {len(self.memories)}"
        )



        self.emit(
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



        self.emit(
            MemoryEvents.SAVED
        )







    # ==========================================================
    # Auxiliares
    # ==========================================================


    def emit(
        self,
        event,
        *args
    ):


        if self.event_bus:


            self.event_bus.emit(
                event,
                *args
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