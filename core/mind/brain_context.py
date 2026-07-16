"""
=========================================
JARVIS CORE

Arquivo:
core/mind/context.py

Descrição:
Gerenciador do contexto cognitivo do Genesis Core.

Responsável por manter:
- Estado do usuário
- Estado dos agentes
- Conversação
- Tarefas
- Ambiente
- Sessão cognitiva

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""


from copy import deepcopy
from datetime import datetime



class Context:
    """
    Memória de trabalho cognitiva.

    Mantém informações utilizadas pelos
    componentes inteligentes.

    Não executa lógica.

    Apenas fornece estado.
    """



    def __init__(self):

        now = datetime.now().isoformat()


        self._context = {


            "session": {

                "id": None,

                "created_at": now,

                "updated_at": now

            },


            "system": {

                "status": "booting",

                "version": "Genesis Core"

            },


            "user": {

                "name": None,

                "id": None

            },


            "agent": {

                "active": "jarvis",

                "available": [

                    "jarvis",

                    "rafiki"

                ]

            },


            "conversation": {

                "last_message": None,

                "last_response": None

            },


            "task": {

                "current": None,

                "queue": []

            },


            "thought": {

                "current": None,

                "history": []

            },


            "environment": {

                "os": None,

                "internet": None,

                "location": None

            },


            "applications": {},


            "devices": {

                "bluetooth": [],

                "wifi": []

            },


            "custom": {}

        }



    # ==================================================
    # Atualização
    # ==================================================


    def update(
        self,
        section,
        key,
        value
    ):

        if section not in self._context:

            self._context[section] = {}



        self._context[section][key] = value


        self._context["session"]["updated_at"] = (
            datetime.now().isoformat()
        )



    # ==================================================
    # Consulta
    # ==================================================


    def get(
        self,
        section=None,
        key=None
    ):


        if section is None:

            return deepcopy(
                self._context
            )



        if section not in self._context:

            return None



        if key is None:

            return deepcopy(
                self._context[section]
            )



        return deepcopy(
            self._context[section].get(key)
        )



    # ==================================================
    # Agente
    # ==================================================


    def set_agent(
        self,
        agent
    ):

        self._context["agent"]["active"] = agent



    def get_agent(
        self
    ):

        return self._context["agent"]["active"]



    # ==================================================
    # Conversação
    # ==================================================


    def set_last_message(
        self,
        message
    ):

        self._context["conversation"]["last_message"] = message



    def set_last_response(
        self,
        response
    ):

        self._context["conversation"]["last_response"] = response



    # ==================================================
    # Pensamento
    # ==================================================


    def set_thought(
        self,
        thought
    ):

        self._context["thought"]["current"] = thought



    def finish_thought(
        self
    ):

        current = self._context["thought"]["current"]


        if current:

            self._context["thought"]["history"].append(
                current
            )


        self._context["thought"]["current"] = None



    # ==================================================
    # Tarefas
    # ==================================================


    def set_task(
        self,
        task
    ):

        self._context["task"]["current"] = task



    def add_task(
        self,
        task
    ):

        self._context["task"]["queue"].append(task)



    def clear_tasks(
        self
    ):

        self._context["task"]["queue"].clear()



    # ==================================================
    # Aplicações
    # ==================================================


    def register_application(
        self,
        name,
        data=None
    ):

        self._context["applications"][name] = data or {}



    def unregister_application(
        self,
        name
    ):

        self._context["applications"].pop(
            name,
            None
        )



    # ==================================================
    # Dispositivos
    # ==================================================


    def set_devices(
        self,
        device_type,
        devices
    ):

        self._context["devices"][device_type] = devices



    # ==================================================
    # Custom
    # ==================================================


    def set_custom(
        self,
        key,
        value
    ):

        self._context["custom"][key] = value



    def get_custom(
        self,
        key,
        default=None
    ):

        return self._context["custom"].get(
            key,
            default
        )



    # ==================================================
    # Utilidades
    # ==================================================


    def clear_temporary(
        self
    ):

        """
        Limpa somente memória temporária.
        """

        self._context["conversation"] = {

            "last_message": None,

            "last_response": None

        }


        self._context["task"]["current"] = None



        self._context["thought"]["current"] = None



    def snapshot(
        self
    ):

        return deepcopy(
            self._context
        )



    def __repr__(self):

        return (

            f"<Context "
            f"agent={self.get_agent()} "
            f">"

        )