"""
=========================================
JARVIS CORE

Arquivo:
registry.py

Descrição:
Registro centralizado e thread-safe de todos os componentes, 
serviços, drivers e agentes do ecossistema.

Arquitetura:
Genesis Core

Mark:
III - Intelligence (Patch 3.4)

Autor:
Caio Vitor Malveira
=========================================
"""

import threading
from datetime import datetime
from core.base.module import Module, ModuleStatus


class Registry(Module):
    """
    Catálogo unificado do JARVIS para indexação e busca de componentes em runtime.
    """

    def __init__(self, logger=None):
        super().__init__("core.registry")
        self.version = "3.0"
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

    def initialize(self):
        with self._lock:
            self.set_status(ModuleStatus.INITIALIZING)
            self.set_status(ModuleStatus.ONLINE)
            self.success("Registro central unificado ONLINE")

    def shutdown(self):
        with self._lock:
            self.components.clear()
            for cat in self.categories:
                self.categories[cat].clear()
            self.set_status(ModuleStatus.OFFLINE)
            self.info("Registro central esvaziado e OFFLINE")

    def register(self, name, component, category="module", version="1.0"):
        name_key = name.lower().strip()
        with self._lock:
            data = {
                "name": name,
                "object": component,
                "category": category,
                "version": version,
                "status": "registered",
                "created": datetime.now()
            }
            self.components[name_key] = data
            if category in self.categories:
                self.categories[category][name_key] = data
            
            self.info(f"Componente catalogado [{category.upper()}]: {name}")

    def get(self, name):
        with self._lock:
            component = self.components.get(name.lower().strip())
            return component["object"] if component else None

    def get_info(self, name):
        with self._lock:
            return self.components.get(name.lower().strip())

    def exists(self, name):
        with self._lock:
            return name.lower().strip() in self.components

    def list_all(self):
        with self._lock:
            return list(self.components.keys())

    def list_category(self, category):
        with self._lock:
            if category not in self.categories:
                return []
            return list(self.categories[category].keys())

    # Helper Wrappers explicitados no Manifest/Core
    def register_service(self, name, service): self.register(name, service, "service")
    def register_agent(self, name, agent): self.register(name, agent, "agent")
    def register_plugin(self, name, plugin): self.register(name, plugin, "plugin")
    def register_capability(self, name, capability): self.register(name, capability, "capability")

    def unregister(self, name):
        name_key = name.lower().strip()
        with self._lock:
            component = self.components.get(name_key)
            if not component:
                return False
            category = component["category"]
            del self.components[name_key]
            if category in self.categories:
                self.categories[category].pop(name_key, None)
            
            self.info(f"Componente removido do registro: {name}")
            return True

    def diagnostics(self):
        with self._lock:
            return {cat: len(items) for cat, items in self.categories.items()}

    # Redirecionamento da interface de log unificada
    def info(self, msg):
        if self.logger: self.logger.info(msg)
    def success(self, msg):
        if self.logger: self.logger.success(msg)