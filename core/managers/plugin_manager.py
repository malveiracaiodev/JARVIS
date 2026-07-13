"""
=========================================
JARVIS CORE

Arquivo:
plugin_manager.py

Descrição:
Injetor dinâmico e supervisor do ecossistema isolado de Plugins.

Arquitetura:
Genesis Core

Mark:
III - Intelligence

Autor:
Caio Vitor Malveira
=========================================
"""

import importlib.util
import threading
from pathlib import Path
from core.base.module import Module, ModuleStatus
from core.events.plugin_events import PluginEvents


class PluginManager(Module):
    """
    Responsável por varrer diretórios e plugar extensões runtime em fios isolados.
    """

    def __init__(self, logger=None, event_bus=None, registry=None, config=None, plugin_directory="plugins"):
        super().__init__("core.plugin_manager")
        self.version = "3.0"
        self.logger = logger
        self.event_bus = event_bus
        self.registry = registry
        self.config = config
        self.directory = Path(plugin_directory)
        self.plugins = {}
        self.failed_plugins = {}
        self._lock = threading.RLock()

    def initialize(self):
        self.set_status(ModuleStatus.INITIALIZING)
        try:
            with self._lock:
                self.directory.mkdir(parents=True, exist_ok=True)
            self.load_all()
            self.set_status(ModuleStatus.ONLINE)
            self.success("Plugin Manager estabilizado")
        except Exception as error:
            self.set_error(str(error))
            self.error(f"Colapso no boot do gerenciador de plugins: {str(error)}")

    def shutdown(self):
        with self._lock:
            names = list(self.plugins.keys())
        for name in names:
            self.unload(name)
        self.set_status(ModuleStatus.OFFLINE)
        self.info("Todos os plugins foram desacoplados e liberados da memória")

    def discover(self):
        plugins = []
        with self._lock:
            if not self.directory.exists():
                return plugins
            
            # Varrer arquivos isolados .py
            for file in self.directory.glob("*.py"):
                if file.name.startswith("_"):
                    continue
                plugins.append(file)

            # Varrer subdiretórios que empacotam pacotes (__init__.py)
            for folder in self.directory.iterdir():
                if folder.is_dir() and (folder / "__init__.py").exists():
                    plugins.append(folder / "__init__.py")
        return plugins

    def load_all(self):
        for plugin_path in self.discover():
            self.load(plugin_path)

    def load(self, path):
        try:
            module_name = path.parent.name if path.name == "__init__.py" else path.stem
            
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"Falta de assinatura/especificação válida em {module_name}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if not hasattr(module, "Plugin"):
                if self.logger:
                    self.logger.warning(f"Módulo '{module_name}' descartado: Não expõe classe 'Plugin'.")
                return False

            plugin_instance = module.Plugin()
            plugin_instance.__file__ = str(path)

            return self.register(plugin_instance)

        except Exception as error:
            with self._lock:
                self.failed_plugins[str(path)] = str(error)
            self.error(f"Erro mecânico carregando plugin {path}: {str(error)}")
            self.emit(PluginEvents.ERROR, {"path": str(path), "error": str(error)})
            return False

    def register(self, plugin):
        name = getattr(plugin, "name", plugin.__class__.__name__)
        
        with self._lock:
            if name in self.plugins:
                if self.logger:
                    self.logger.warning(f"Plugin '{name}' rejeitado: Já existe uma instância viva registrada.")
                return False

            metadata = {
                "object": plugin,
                "version": getattr(plugin, "version", "1.0"),
                "status": "loading"
            }
            self.plugins[name] = metadata

        try:
            if hasattr(plugin, "initialize"):
                plugin.initialize()
            elif hasattr(plugin, "start"):
                plugin.start()

            with self._lock:
                metadata["status"] = "online"

            if self.registry:
                self.registry.register_plugin(name, plugin)

            self.emit(PluginEvents.LOADED, {"name": name})
            self.success(f"Plugin ativado e injetado: '{name}'")
            return True

        except Exception as error:
            with self._lock:
                metadata["status"] = "error"
                self.failed_plugins[name] = str(error)
            self.error(f"Falha na rotina de boot do plugin '{name}': {str(error)}")
            return False

    def unload(self, name):
        with self._lock:
            data = self.plugins.get(name)
        if not data:
            return False

        plugin = data["object"]
        try:
            if hasattr(plugin, "shutdown"):
                plugin.shutdown()
            elif hasattr(plugin, "stop"):
                plugin.stop()

            with self._lock:
                data["status"] = "offline"

            self.emit(PluginEvents.UNLOADED, {"name": name})
            self.info(f"Plugin desvinculado com sucesso: '{name}'")
            return True
        except Exception as error:
            self.error(f"Erro ao forçar shutdown em '{name}': {str(error)}")
            return False

    def unregister(self, name):
        with self._lock:
            if name not in self.plugins:
                return False
        self.unload(name)
        
        with self._lock:
            del self.plugins[name]
        
        if self.registry:
            self.registry.unregister(name)
        return True

    def reload(self, name):
        with self._lock:
            data = self.plugins.get(name)
        if not data:
            return False
        path = getattr(data["object"], "__file__", None)
        self.unregister(name)
        return self.load(Path(path)) if path else False

    def get(self, name):
        with self._lock:
            data = self.plugins.get(name)
            return data["object"] if data else None

    def exists(self, name):
        with self._lock:
            return name in self.plugins

    def list_plugins(self):
        with self._lock:
            return list(self.plugins.keys())

    def count(self):
        with self._lock:
            return len(self.plugins)

    def status(self):
        with self._lock:
            online = sum(1 for p in self.plugins.values() if p["status"] == "online")
            return {
                "total": len(self.plugins),
                "online": online,
                "errors": len(self.failed_plugins)
            }

    def emit(self, event, data):
        if self.event_bus:
            self.event_bus.emit(event, data)

    def info(self, msg):
        if self.logger: self.logger.info(msg)
    def success(self, msg):
        if self.logger: self.logger.success(msg)
    def error(self, msg):
        if self.logger: self.logger.error(msg)