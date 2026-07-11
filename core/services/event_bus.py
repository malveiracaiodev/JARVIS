"""
=========================================
JARVIS CORE

Arquivo:
event_bus.py

Descrição:
Sistema central de eventos do JARVIS.

Responsável por:
- Comunicação desacoplada entre módulos
- Distribuição de eventos
- Histórico operacional
- Sincronização interna

Arquitetura:
Genesis Core

Mark:
II - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from collections import defaultdict
from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)




class EventBus(Module):


    """
    Barramento central de comunicação
    do JARVIS.

    Todos os sistemas podem conversar
    sem depender diretamente uns dos outros.
    """



    def __init__(
        self,
        logger=None
    ):


        super().__init__(
            "Event Bus"
        )


        self.version = "2.1"


        self.logger = logger


        self.listeners = defaultdict(list)


        self.history = []


        self.event_count = 0


        self.max_history = 1000





    # =====================================================
    # CICLO DE VIDA
    # =====================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.listeners.clear()

        self.history.clear()

        self.event_count = 0



        self.set_status(
            ModuleStatus.ONLINE
        )


        self.success(
            "Event Bus iniciado"
        )





    def shutdown(self):


        self.listeners.clear()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.info(
            "Event Bus encerrado"
        )





    # =====================================================
    # INSCRIÇÃO
    # =====================================================


    def subscribe(
        self,
        event_name,
        callback
    ):


        if callback not in self.listeners[event_name]:


            self.listeners[event_name].append(
                callback
            )


            self.info(
                f"Listener registrado: {event_name}"
            )





    def unsubscribe(
        self,
        event_name,
        callback
    ):


        if event_name in self.listeners:


            if callback in self.listeners[event_name]:


                self.listeners[event_name].remove(
                    callback
                )





    # =====================================================
    # EMISSÃO DE EVENTOS
    # =====================================================


    def emit(
        self,
        event_name,
        *args,
        **kwargs
    ):


        self.event_count += 1



        payload = None



        if args:

            payload = args[0]


        elif kwargs:

            payload = kwargs




        event = {


            "id":
                self.event_count,


            "event":
                event_name,


            "payload":
                payload,


            "time":
                datetime.now()
                .isoformat()

        }



        self.history.append(
            event
        )



        if len(self.history) > self.max_history:


            self.history.pop(0)





        self.info(
            f"Evento emitido: {event_name}"
        )





        listeners = list(

            self.listeners.get(

                event_name,

                []

            )

        )





        for callback in listeners:


            try:


                callback(
                    *args,
                    **kwargs
                )


            except Exception as error:


                self.error(

                    f"Erro no evento {event_name}: {error}"

                )







    # =====================================================
    # CONSULTAS
    # =====================================================


    def has_event(
        self,
        event_name
    ):


        return event_name in self.listeners





    def get_history(self):


        return self.history





    def get_event_count(self):


        return self.event_count





    def clear_history(self):


        self.history.clear()





    # =====================================================
    # LOGGER
    # =====================================================


    def info(
        self,
        message
    ):


        if self.logger:

            self.logger.info(
                message
            )





    def success(
        self,
        message
    ):


        if self.logger:

            self.logger.success(
                message
            )





    def error(
        self,
        message
    ):


        if self.logger:

            self.logger.error(
                message
            )