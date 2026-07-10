"""
=========================================
JARVIS CORE

Arquivo:
event_bus.py

Descrição:
Sistema central de eventos do JARVIS.

Responsável pela comunicação entre
módulos sem criar dependências diretas.

Mark:
I - Heartbeat

Autor:
Caio Vitor Malveira
=========================================
"""


from collections import defaultdict
from datetime import datetime


from core.base.module import Module, ModuleStatus





class EventBus(Module):
    """
    Barramento central de eventos.
    """



    def __init__(self, logger=None):

        super().__init__(
            "Event Bus"
        )


        self.logger = logger


        self.listeners = defaultdict(list)


        self.history = []


        self.event_count = 0





    # ==========================================================
    # Ciclo de vida
    # ==========================================================


    def initialize(self):
        """
        Inicializa o sistema.
        """


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:


            self.listeners.clear()

            self.history.clear()

            self.event_count = 0



            self.set_status(
                ModuleStatus.ONLINE
            )



            if self.logger:

                self.logger.success(
                    "Event Bus iniciado"
                )



        except Exception as error:


            self.set_error(
                str(error)
            )



            if self.logger:

                self.logger.error(
                    f"Erro no Event Bus: {error}"
                )





    def shutdown(self):
        """
        Encerra o Event Bus.
        """


        self.clear(
            silent=True
        )


        self.set_status(
            ModuleStatus.OFFLINE
        )



        if self.logger:

            self.logger.info(
                "Event Bus encerrado"
            )





    # ==========================================================
    # Registro de eventos
    # ==========================================================


    def subscribe(
        self,
        event_name,
        callback
    ):
        """
        Registra um listener.
        """


        self.listeners[event_name].append(
            callback
        )



        if self.logger:

            self.logger.info(
                f"Listener registrado: {event_name}"
            )





    def unsubscribe(
        self,
        event_name,
        callback
    ):
        """
        Remove um listener.
        """


        if callback in self.listeners[event_name]:


            self.listeners[event_name].remove(
                callback
            )



            if self.logger:

                self.logger.info(
                    f"Listener removido: {event_name}"
                )





    def emit(
        self,
        event_name,
        *args,
        **kwargs
    ):
        """
        Dispara um evento.
        """


        self.event_count += 1



        event_data = {


            "event":
                event_name,


            "time":
                datetime.now().strftime(
                    "%H:%M:%S"
                )

        }



        self.history.append(
            event_data
        )



        if self.logger:

            self.logger.info(
                f"Evento emitido: {event_name}"
            )



        for callback in list(
            self.listeners[event_name]
        ):


            try:


                callback(
                    *args,
                    **kwargs
                )



            except Exception as error:


                if self.logger:

                    self.logger.error(
                        f"Erro no evento {event_name}: {error}"
                    )





    # ==========================================================
    # Diagnóstico
    # ==========================================================


    def has_event(
        self,
        event_name
    ):
        """
        Verifica listeners.
        """


        return len(
            self.listeners[event_name]
        ) > 0





    def get_history(self):
        """
        Retorna histórico de eventos.
        """


        return self.history





    def get_event_count(self):
        """
        Retorna quantidade de eventos.
        """


        return self.event_count





    def clear(
        self,
        silent=False
    ):
        """
        Remove todos os eventos.
        """


        self.listeners.clear()



        if not silent and self.logger:


            self.logger.warning(
                "Todos os eventos removidos"
            )