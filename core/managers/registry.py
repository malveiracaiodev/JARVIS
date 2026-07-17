"""
=========================================
JARVIS CORE

Arquivo:
core/managers/registry.py

Descrição:
Registro centralizado de componentes
do Genesis Core.

Responsável por:
- Catalogar módulos
- Registrar serviços
- Indexar agentes
- Controlar plugins
- Diagnóstico estrutural

Arquitetura:
Genesis Core

Mark:
III - Matrix (Registry Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import copy
import threading


from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)





class Registry(Module):

    """
    Catálogo global do Genesis Core.
    """



    def __init__(
        self,
        logger=None
    ):


        super().__init__(
            "core.registry"
        )


        self.version = "3.5"


        self.logger = logger



        self.components = {}



        self.categories = {

            "service": {},

            "agent": {},

            "plugin": {},

            "capability": {},

            "driver": {},

            "module": {}

        }



        self.created = datetime.now()



        self._lock = threading.RLock()





    # ==================================================
    # CICLO DE VIDA
    # ==================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log_success(
            "Registry Mark III ONLINE."
        )





    def shutdown(self):


        with self._lock:


            self.components.clear()


            for category in self.categories:

                self.categories[category].clear()



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Registry encerrado."
        )





    # ==================================================
    # REGISTRO
    # ==================================================


    def register(
        self,
        name,
        component,
        category="module",
        version="1.0"
    ):


        key = (
            str(name)
            .lower()
            .strip()
        )



        with self._lock:


            if key in self.components:


                self.log_info(
                    f"Registro ignorado. Já existe: {name}"
                )


                return False





            if category not in self.categories:


                self.categories[category] = {}





            data = {


                "name":
                    name,


                "object":
                    component,


                "category":
                    category,


                "version":
                    version,


                "status":
                    "registered",


                "created":
                    datetime.now()
                    .isoformat()

            }




            self.components[key] = data



            self.categories[category][key] = data




        self.log_info(
            f"Componente registrado [{category}]: {name}"
        )


        return True





    # ==================================================
    # CONSULTA
    # ==================================================


    def get(
        self,
        name
    ):


        data = self.get_info(
            name
        )


        return (
            data["object"]
            if data
            else None
        )





    def get_info(
        self,
        name
    ):


        key = str(name).lower().strip()



        with self._lock:


            data = self.components.get(
                key
            )


            return copy.deepcopy(
                data
            ) if data else None





    def exists(
        self,
        name
    ):


        key = str(name).lower().strip()



        with self._lock:


            return key in self.components





    def list_all(self):


        with self._lock:


            return list(
                self.components.keys()
            )





    def list_category(
        self,
        category
    ):


        with self._lock:


            return list(

                self.categories
                .get(
                    category,
                    {}
                )
                .keys()

            )





    def count(self):

        with self._lock:

            return len(
                self.components
            )





    # ==================================================
    # WRAPPERS
    # ==================================================


    def register_service(
        self,
        name,
        service
    ):

        return self.register(
            name,
            service,
            "service"
        )





    def register_agent(
        self,
        name,
        agent
    ):

        return self.register(
            name,
            agent,
            "agent"
        )





    def register_plugin(
        self,
        name,
        plugin
    ):

        return self.register(
            name,
            plugin,
            "plugin"
        )





    def register_capability(
        self,
        name,
        capability
    ):

        return self.register(
            name,
            capability,
            "capability"
        )





    # ==================================================
    # REMOÇÃO
    # ==================================================


    def unregister(
        self,
        name
    ):


        key = str(name).lower().strip()



        with self._lock:


            data = self.components.get(
                key
            )



            if not data:

                return False



            del self.components[key]



            self.categories[
                data["category"]
            ].pop(
                key,
                None
            )



        self.log_info(
            f"Componente removido: {name}"
        )


        return True





    # ==================================================
    # DIAGNÓSTICO
    # ==================================================


    def diagnostics(self):


        with self._lock:


            return {


                "total":
                    len(self.components),


                "categories":

                    {

                        category:
                            len(items)

                        for category, items

                        in self.categories.items()

                    }


            }





    # ==================================================
    # LOG
    # ==================================================


    def log_info(
        self,
        msg
    ):

        if self.logger:

            self.logger.info(msg)





    def log_success(
        self,
        msg
    ):

        if self.logger:

            self.logger.success(msg)