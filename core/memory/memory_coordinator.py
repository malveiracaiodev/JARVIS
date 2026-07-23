"""
=========================================
GENESIS CORE

Arquivo:
core/memory/memory_coordinator.py

Descrição:

Fachada central da arquitetura de memória
do Genesis Core.

Responsável por:

- Coordenar memória de curto prazo
- Coordenar memória de longo prazo
- Recuperação contextual
- Integração com Thought Engine
- Preparação de contexto cognitivo
- Persistência

Arquitetura:

Thought Engine
      |
      v
MemoryCoordinator
      |
  +---+---+
  |       |
 STM     LTM


Mark:
V - Evolution Memory Layer

Autor:
Caio Vitor Malveira
=========================================
"""


from __future__ import annotations


import threading

from datetime import datetime
from typing import Any


from core.interfaces.memory_interface import MemoryInterface

from core.memory.short_term_memory import ShortTermMemory
from core.memory.long_term_memory import LongTermMemory





class MemoryCoordinator(MemoryInterface):


    """
    Coordenador universal de memória.

    Atua como ponte entre:

    - Pipeline Cognitivo
    - Thought Engine
    - Personas
    - Agentes
    - Conhecimento persistente
    """



    def __init__(
        self,
        memory_manager=None,
        logger=None
    ):


        self._short_term = ShortTermMemory()


        self._long_term = LongTermMemory(
            memory_manager=memory_manager
        )


        self.logger = logger


        self._lock = threading.RLock()


        self._cache = {}


        self._stats = {

            "stored": 0,

            "retrieved": 0,

            "searches": 0,

            "forgotten": 0

        }





    # =====================================================
    # STORE
    # =====================================================


    def store(
        self,
        data: Any,
        memory_type: str = "short_term"
    ):


        with self._lock:


            try:


                if memory_type in (
                    "long_term",
                    "episodic",
                    "semantic"
                ):


                    result = self._long_term.store(

                        data,

                        memory_type=memory_type

                    )


                else:


                    result = self._short_term.store(

                        data,

                        memory_type=memory_type

                    )



                self._stats["stored"] += 1


                return result



            except Exception as error:


                self._log(
                    "Memory store error",
                    error
                )


                return None





    # =====================================================
    # MEMÓRIA COGNITIVA
    # =====================================================


    def remember_fact(
        self,
        fact: str,
        importance: int = 5
    ):


        return self.store(

            {

                "type":
                    "fact",

                "content":
                    fact,

                "importance":
                    importance,

                "created_at":
                    datetime.now().isoformat()

            },

            memory_type="semantic"

        )





    def remember_event(
        self,
        event: str
    ):


        return self.store(

            {

                "type":
                    "event",

                "content":
                    event,

                "created_at":
                    datetime.now().isoformat()

            },

            memory_type="episodic"

        )







    # =====================================================
    # RETRIEVE
    # =====================================================


    def retrieve(
        self,
        query,
        context=None
    ):


        with self._lock:


            cache_key = str(query)


            if cache_key in self._cache:

                return self._cache[cache_key]



            short = self._short_term.retrieve(

                query,

                context=context

            )


            long = self._long_term.retrieve(

                query,

                context=context

            )



            result = {


                "query":
                    query,


                "short_term":
                    short,


                "long_term":
                    long


            }



            self._cache[cache_key] = result


            self._stats["retrieved"] += 1



            return result





    # =====================================================
    # CONTEXTO PARA IA
    # =====================================================


    def build_context(
        self,
        query
    ):


        memories = self.retrieve(
            query
        )


        return {


            "memory":

                memories,


            "summary":

                self._summarize(
                    memories
                )

        }





    def _summarize(
        self,
        memories
    ):


        return {

            "short_count":

                len(
                    memories.get(
                        "short_term",
                        []
                    )
                ),


            "long_count":

                len(
                    memories.get(
                        "long_term",
                        []
                    )
                )

        }





    # =====================================================
    # SEARCH
    # =====================================================


    def search(
        self,
        query,
        limit=10
    ):


        with self._lock:


            self._stats["searches"] += 1



            return {


                "short_term":

                    self._short_term.search(

                        query,

                        limit=limit

                    ),



                "long_term":

                    self._long_term.search(

                        query,

                        limit=limit

                    )

            }






    # =====================================================
    # CLEAR
    # =====================================================


    def clear(self):


        with self._lock:


            self._cache.clear()


            return self._short_term.clear()







    # =====================================================
    # FORGET
    # =====================================================


    def forget(
        self,
        memory_id
    ):


        with self._lock:


            self._stats["forgotten"] += 1



            if memory_id.startswith("stm_"):


                return self._short_term.forget(
                    memory_id
                )



            if memory_id.startswith("ltm_"):


                return self._long_term.forget(
                    memory_id
                )



            return (

                self._short_term.forget(
                    memory_id
                )

                or

                self._long_term.forget(
                    memory_id
                )

            )






    # =====================================================
    # PERSISTÊNCIA
    # =====================================================


    def save(self):


        with self._lock:

            return self._long_term.save()





    def load(self):


        with self._lock:

            return self._long_term.load()






    # =====================================================
    # STATUS
    # =====================================================


    def status(self):


        return {


            "name":

                self.name(),



            "status":

                "operational",



            "short_term":

                self._short_term.status(),



            "long_term":

                self._long_term.status(),



            "statistics":

                self._stats

        }






    # =====================================================
    # UTIL
    # =====================================================


    def _log(
        self,
        message,
        error=None
    ):


        if self.logger:


            self.logger.error(
                message,
                error
            )


        else:


            print(
                "[MEMORY]",
                message,
                error
            )





    def name(self):

        return "memory.coordinator"