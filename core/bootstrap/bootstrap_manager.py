"""
=========================================
JARVIS GENESIS CORE

Arquivo:
bootstrap_manager.py

Descrição:
Gerenciador de montagem do Core. Lê as especificações do Manifest,
resolve acoplamentos e cria instâncias thread-safe.

Arquitetura:
Genesis Core

Mark:
III - Intelligence (Patch 3.1)

Autor:
Caio Vitor Malveira
=========================================
"""

import inspect
import threading
from core.bootstrap.manifest import get_boot_components


class BootstrapManager:
    """
    Orquestrador encarregado da resolução de dependências e injeção do JARVIS.
    """

    def __init__(self):
        self._components = {}
        self._registry = None
        self._lock = threading.RLock()

    # ==================================================
    # BUILD
    # ==================================================
    def build(self):
        """Constrói o ecossistema resolvendo dependências hierárquicas."""
        with self._lock:
            self.clear()
            manifest = get_boot_components()

            # 1. Construção Robusta dos Componentes Ativos
            for component in manifest:
                self._build_component(component)

            # 2. Registro de Subsistemas se um Registry estiver acoplado
            self._register_components(manifest)

            return dict(self._components)

    # ==================================================
    # BUILD COMPONENT (Injeção por Assinatura / Kwargs)
    # ==================================================
    def _build_component(self, component):
        name = component["name"]
        cls = component["class"]
        dependencies = component.get("constructor", [])

        # Coleta as instâncias das dependências exigidas
        kwargs = {}
        for dep in dependencies:
            dep_instance = self.get(dep)
            if dep_instance is None:
                if component.get("required", False):
                    raise RuntimeError(f"Dependência vital '{dep}' ausente para a criação de '{name}'.")
                continue
            kwargs[dep] = dep_instance

        try:
            # Inspeção dinâmica do construtor da classe alvo
            sig = inspect.signature(cls.__init__)
            param_names = list(sig.parameters.keys())

            # Filtra os kwargs para passar apenas o que o construtor aceita real ou aceita via **kwargs
            has_kwargs_param = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
            
            if not has_kwargs_param:
                # Se não aceitar empacotamento genérico, passa apenas chaves explícitas correspondentes
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in param_names}
            else:
                filtered_kwargs = kwargs

            # Instanciação por mapeamento de chaves explícito (Segurança contra troca de ordem)
            instance = cls(**filtered_kwargs) if filtered_kwargs else cls()
            
        except Exception as e:
            raise RuntimeError(f"Falha ao instanciar componente '{name}' da classe '{cls.__name__}': {str(e)}")

        self._components[name] = instance

        # Casamento do nó de registro centralizado se for criado
        if name == "registry":
            self._registry = instance

    # ==================================================
    # REGISTER
    # ==================================================
    def _register_components(self, manifest):
        # Se um módulo de registro global não foi declarado/ativado, ignora graciosamente
        if self._registry is None or not hasattr(self._registry, "register"):
            return

        for component in manifest:
            name = component["name"]
            if name in self._components:
                try:
                    self._registry.register(
                        name,
                        self._components[name],
                        component["category"]
                    )
                except Exception as e:
                    print(f"[BOOTSTRAP WARNING] Erro ao registrar '{name}' no Registry: {str(e)}")

    # ==================================================
    # CONSULTAS THREAD-SAFE
    # ==================================================
    def get(self, name):
        with self._lock:
            return self._components.get(name)

    def exists(self, name):
        with self._lock:
            return name in self._components

    def all(self):
        with self._lock:
            return dict(self._components)

    def registry(self):
        with self._lock:
            return self._registry

    def count(self):
        with self._lock:
            return len(self._components)

    # ==================================================
    # LIMPEZA
    # ==================================================
    def clear(self):
        with self._lock:
            self._components.clear()
            self._registry = None