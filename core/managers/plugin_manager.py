"""
=========================================
JARVIS CORE

Arquivo:
plugin_manager.py

Descrição:
Gerenciador central de Plugins.

Responsável por:

- Descobrir plugins
- Carregar módulos
- Registrar plugins
- Inicializar extensões
- Controlar ciclo de vida
- Emitir eventos
- Diagnóstico de plugins

Arquitetura:
Genesis Core

Mark:
II.1 - Evolution

Autor:
Caio Vitor Malveira
=========================================
"""


from pathlib import Path
import importlib.util


from core.base.module import (
    Module,
    ModuleStatus
)





class PluginManager(Module):


    """
    Gerenciador central de plugins
    do JARVIS.
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


        self.version = "2.1"


        self.logger = logger


        self.event_bus = event_bus


        self.registry = registry


        self.config = config



        self.directory = Path(
            plugin_directory
        )



        self.plugins = {}


        self.failed_plugins = {}








    # =====================================================
    # CICLO DE VIDA
    # =====================================================


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
                "Plugin Manager iniciado"
            )



        except Exception as error:


            self.set_error(
                str(error)
            )


            self.log_error(
                str(error)
            )








    def shutdown(self):


        for name in list(
            self.plugins.keys()
        ):


            self.unload(
                name
            )



        self.plugins.clear()



        self.set_status(
            ModuleStatus.OFFLINE
        )



        self.log_info(
            "Plugin Manager encerrado"
        )








    # =====================================================
    # DESCOBERTA
    # =====================================================


    def discover(self):


        plugins = []



        for file in self.directory.glob(
            "*.py"
        ):


            if file.name.startswith(
                "_"
            ):

                continue



            plugins.append(
                file
            )





        for folder in self.directory.iterdir():


            if (

                folder.is_dir()

                and

                (folder / "__init__.py").exists()

            ):


                plugins.append(
                    folder / "__init__.py"
                )



        return plugins








    # =====================================================
    # CARREGAMENTO
    # =====================================================


    def load_all(self):


        for plugin in self.discover():


            self.load(
                plugin
            )








    def load(
        self,
        path
    ):


        try:


            module_name = (

                path.parent.name

                if path.name == "__init__.py"

                else path.stem

            )



            spec = importlib.util.spec_from_file_location(

                module_name,

                path

            )



            if spec is None or spec.loader is None:


                raise RuntimeError(

                    f"Não foi possível carregar {module_name}"

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


                self.log_warning(

                    f"{module_name} não possui classe Plugin"

                )


                return False






            plugin = module.Plugin()



            plugin.__file__ = str(
                path
            )



            return self.register(
                plugin
            )





        except Exception as error:


            self.failed_plugins[str(path)] = str(
                error
            )


            self.log_error(

                f"Erro carregando plugin {path}: {error}"

            )


            self.emit(

                "PLUGIN_ERROR",

                str(error)

            )


            return False









    # =====================================================
    # REGISTRO
    # =====================================================


    def register(
        self,
        plugin
    ):


        name = getattr(

            plugin,

            "name",

            plugin.__class__.__name__

        )



        if name in self.plugins:


            self.log_warning(

                f"Plugin '{name}' já registrado"

            )


            return False






        metadata = {


            "object":

            plugin,


            "version":

            getattr(
                plugin,
                "version",
                "1.0"
            ),



            "status":

            "loading"


        }



        self.plugins[name] = metadata






        try:



            if hasattr(
                plugin,
                "initialize"
            ):


                plugin.initialize()



            elif hasattr(
                plugin,
                "start"
            ):


                plugin.start()



            metadata["status"] = "online"




            if self.registry:


                self.registry.register_plugin(

                    name,

                    plugin

                )





            self.emit(

                "PLUGIN_REGISTERED",

                name

            )



            self.log_success(

                f"Plugin iniciado: {name}"

            )



            return True





        except Exception as error:


            metadata["status"] = "error"


            self.failed_plugins[name] = str(
                error
            )



            self.log_error(

                f"Erro iniciando plugin {name}: {error}"

            )


            return False









    # =====================================================
    # CONTROLE
    # =====================================================


    def unload(
        self,
        name
    ):


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



            elif hasattr(
                plugin,
                "stop"
            ):


                plugin.stop()





            data["status"] = "offline"




            self.emit(

                "PLUGIN_UNLOADED",

                name

            )



            self.log_info(

                f"Plugin desligado: {name}"

            )



            return True




        except Exception as error:


            self.log_error(

                f"Erro desligando plugin {name}: {error}"

            )


            return False








    def unregister(
        self,
        name
    ):


        if name not in self.plugins:


            return False



        self.unload(
            name
        )


        del self.plugins[name]



        if self.registry:


            self.registry.unregister(
                name
            )



        self.emit(

            "PLUGIN_UNREGISTERED",

            name

        )


        return True








    def reload(
        self,
        name
    ):


        data = self.plugins.get(
            name
        )


        if not data:


            return False



        path = getattr(

            data["object"],

            "__file__",

            None

        )



        self.unregister(
            name
        )



        if path:


            return self.load(
                Path(path)
            )


        return False








    # =====================================================
    # CONSULTAS
    # =====================================================


    def get(
        self,
        name
    ):


        data = self.plugins.get(
            name
        )


        if data:


            return data["object"]



        return None







    def exists(
        self,
        name
    ):


        return name in self.plugins







    def list_plugins(self):


        return list(
            self.plugins.keys()
        )







    def count(self):


        return len(
            self.plugins
        )







    def status(self):


        online = 0


        errors = len(
            self.failed_plugins
        )



        for plugin in self.plugins.values():


            if plugin["status"] == "online":


                online += 1




        return {


            "total":

            len(
                self.plugins
            ),



            "online":

            online,



            "errors":

            errors


        }









    # =====================================================
    # EVENTOS
    # =====================================================


    def emit(
        self,
        event,
        data
    ):


        if self.event_bus:


            self.event_bus.emit(

                event,

                data

            )









    # =====================================================
    # LOGS
    # =====================================================


    def log_info(
        self,
        message
    ):


        if self.logger:


            self.logger.info(
                message
            )





    def log_warning(
        self,
        message
    ):


        if self.logger:


            self.logger.warning(
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





    def log_error(
        self,
        message
    ):


        if self.logger:


            self.logger.error(
                message
            )