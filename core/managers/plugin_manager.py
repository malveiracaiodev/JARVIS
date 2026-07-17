"""
=========================================
JARVIS CORE

Arquivo:
core/managers/plugin_manager.py

Descrição:
Gerenciador dinâmico de plugins do Genesis Core.

Responsável por:
- Descobrir plugins
- Carregar extensões
- Controlar ciclo de vida
- Registrar plugins ativos

Arquitetura:
Genesis Core

Mark:
III - Matrix (Plugin Layer)

Autor:
Caio Vitor Malveira
=========================================
"""


import importlib.util
import threading


from pathlib import Path



from core.base.module import (
    Module,
    ModuleStatus
)



from core.events.plugin_events import (
    PluginEvents
)





class PluginManager(Module):


    """
    Controlador da camada de extensões.
    """



    def __init__(
        self,
        logger=None,
        event_bus=None,
        registry=None,
        config=None,
        plugin_directory="plugins"
    ):


        super().__init__(
            "core.plugin_manager"
        )


        self.version = "3.1"


        self.logger = logger

        self.event_bus = event_bus

        self.registry = registry

        self.config = config


        self.directory = Path(
            plugin_directory
        )


        self.plugins = {}

        self.failed_plugins = {}


        self._lock = threading.RLock()





    # ======================================================
    # CICLO DE VIDA
    # ======================================================


    def initialize(self):


        self.set_status(
            ModuleStatus.INITIALIZING
        )


        try:


            self.directory.mkdir(
                parents=True,
                exist_ok=True
            )


            self.load_all()



            self.set_status(
                ModuleStatus.ONLINE
            )


            self.log_success(
                "Plugin Manager Mark III ONLINE."
            )



        except Exception as error:


            self.set_error(
                str(error)
            )


            self.log_error(
                str(error)
            )






    def shutdown(self):


        with self._lock:


            names = list(
                self.plugins.keys()
            )



        for name in names:


            self.unregister(
                name
            )



        self.set_status(
            ModuleStatus.OFFLINE
        )


        self.log_info(
            "Plugin Manager encerrado."
        )





    # ======================================================
    # DESCOBERTA
    # ======================================================


    def discover(self):


        result = []



        if not self.directory.exists():

            return result




        for file in self.directory.glob(
            "*.py"
        ):


            if not file.name.startswith(
                "_"
            ):

                result.append(
                    file
                )



        for folder in self.directory.iterdir():


            if (

                folder.is_dir()

                and

                (folder / "__init__.py").exists()

            ):


                result.append(
                    folder / "__init__.py"
                )



        return result





    def load_all(self):


        for path in self.discover():

            self.load(
                path
            )





    # ======================================================
    # LOAD
    # ======================================================


    def load(
        self,
        path
    ):


        try:


            name = (

                path.parent.name

                if path.name == "__init__.py"

                else path.stem

            )



            spec = importlib.util.spec_from_file_location(
                name,
                path
            )



            if not spec or not spec.loader:

                raise RuntimeError(
                    "Plugin inválido"
                )



            module = importlib.util.module_from_spec(
                spec
            )


            spec.loader.exec_module(
                module
            )



            if not hasattr(
                module,
                "Plugin"
            ):


                self.log_info(
                    f"Plugin ignorado: {name}"
                )


                return False




            instance = module.Plugin()


            instance.__file__ = str(
                path
            )


            return self.register(
                instance
            )



        except Exception as error:


            self.failed_plugins[
                str(path)
            ] = str(error)


            self.log_error(
                f"Falha carregando plugin: {error}"
            )


            return False





    # ======================================================
    # REGISTRO
    # ======================================================


    def register(
        self,
        plugin
    ):


        name = getattr(
            plugin,
            "name",
            plugin.__class__.__name__
        )



        with self._lock:


            if name in self.plugins:

                return False



            self.plugins[name] = {


                "object":
                    plugin,


                "path":
                    getattr(
                        plugin,
                        "__file__",
                        None
                    ),


                "status":
                    "loading"

            }



        try:


            if hasattr(plugin,"initialize"):

                plugin.initialize()



            self.plugins[name]["status"] = "online"



            if self.registry:

                self.registry.register_plugin(
                    name,
                    plugin
                )



            self.emit(
                PluginEvents.LOADED,
                {
                    "name":name
                }
            )



            self.log_success(
                f"Plugin ativo: {name}"
            )



            return True



        except Exception as error:


            self.failed_plugins[name] = str(error)

            self.log_error(
                str(error)
            )

            return False





    # ======================================================
    # REMOÇÃO
    # ======================================================


    def unregister(
        self,
        name
    ):


        with self._lock:


            data = self.plugins.get(
                name
            )



        if not data:

            return False




        plugin = data["object"]



        try:


            if hasattr(
                plugin,
                "shutdown"
            ):

                plugin.shutdown()



        except Exception:

            pass




        with self._lock:


            del self.plugins[name]



        if self.registry:

            self.registry.unregister(
                name
            )



        self.emit(
            PluginEvents.UNLOADED,
            {
                "name":name
            }
        )


        return True





    # ======================================================
    # CONSULTA
    # ======================================================


    def get(
        self,
        name
    ):


        with self._lock:


            data = self.plugins.get(
                name
            )


            return data["object"] if data else None





    def exists(
        self,
        name
    ):


        return self.get(name) is not None





    def list_plugins(self):


        with self._lock:

            return list(
                self.plugins.keys()
            )





    def count(self):

        return len(
            self.plugins
        )





    def status(self):


        with self._lock:


            return {


                "total":
                    len(self.plugins),


                "errors":
                    len(self.failed_plugins)

            }





    # ======================================================
    # EVENTOS
    # ======================================================


    def emit(
        self,
        event,
        data=None
    ):


        if self.event_bus:


            try:

                self.event_bus.emit(
                    event,
                    data
                )


            except Exception:

                pass





    # ======================================================
    # LOG
    # ======================================================


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



    def log_error(
        self,
        msg
    ):

        if self.logger:

            self.logger.error(msg)