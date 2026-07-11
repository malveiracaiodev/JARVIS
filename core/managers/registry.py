"""
=========================================
JARVIS CORE

Arquivo:
registry.py

Descrição:
Registro central de componentes.

Responsável por:
- Registrar serviços
- Registrar agentes
- Registrar plugins
- Localizar componentes
- Diagnóstico do sistema

Arquitetura:
Genesis Core

Mark:
II.1 - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from datetime import datetime


from core.base.module import (
    Module,
    ModuleStatus
)





class Registry(Module):


    """
    Registro central do JARVIS.
    """



    def __init__(
        self,
        logger=None
    ):


        super().__init__(
            "Registry"
        )


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







    # ======================================================
    # CICLO DE VIDA
    # ======================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        self.set_status(
            ModuleStatus.ONLINE
        )


        self.log(
            "Registry ONLINE"
        )





    def shutdown(self):


        self.components.clear()


        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log(
            "Registry OFFLINE"
        )







    # ======================================================
    # REGISTRO
    # ======================================================


    def register(
        self,
        name,
        component,
        category="module",
        version="1.0"
    ):


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

        }




        self.components[name] = data



        if category in self.categories:


            self.categories[category][name] = data




        self.log(
            f"Registrado: {name}"
        )







    # ======================================================
    # BUSCA
    # ======================================================


    def get(
        self,
        name
    ):


        component = self.components.get(
            name
        )


        if component:


            return component["object"]



        return None







    def get_info(
        self,
        name
    ):


        return self.components.get(
            name
        )







    def exists(
        self,
        name
    ):


        return name in self.components







    # ======================================================
    # LISTAGEM
    # ======================================================


    def list_all(self):


        return list(
            self.components.keys()
        )






    def list_category(
        self,
        category
    ):


        if category not in self.categories:


            return []



        return list(
            self.categories[category].keys()
        )






    # ======================================================
    # REGISTROS ESPECÍFICOS
    # ======================================================


    def register_service(
        self,
        name,
        service
    ):


        self.register(
            name,
            service,
            "service"
        )





    def register_agent(
        self,
        name,
        agent
    ):


        self.register(
            name,
            agent,
            "agent"
        )





    def register_plugin(
        self,
        name,
        plugin
    ):


        self.register(
            name,
            plugin,
            "plugin"
        )





    def register_capability(
        self,
        name,
        capability
    ):


        self.register(
            name,
            capability,
            "capability"
        )








    # ======================================================
    # DIAGNÓSTICO
    # ======================================================


    def diagnostics(self):


        return {


            "total":

            len(
                self.components
            ),



            "services":

            len(
                self.categories["service"]
            ),



            "agents":

            len(
                self.categories["agent"]
            ),



            "plugins":

            len(
                self.categories["plugin"]
            ),



            "capabilities":

            len(
                self.categories["capability"]
            ),



            "drivers":

            len(
                self.categories["driver"]
            ),



            "modules":

            len(
                self.categories["module"]
            )

        }








    # ======================================================
    # REMOVER
    # ======================================================


    def unregister(
        self,
        name
    ):


        component = self.components.get(
            name
        )



        if not component:


            return False




        category = component["category"]



        del self.components[name]



        if category in self.categories:


            self.categories[category].pop(
                name,
                None
            )



        self.log(
            f"Removido: {name}"
        )


        return True







    # ======================================================
    # LOG
    # ======================================================


    def log(
        self,
        message
    ):


        if self.logger:


            self.logger.info(
                message
            )


        else:


            print(
                "[REGISTRY]",
                message
            )