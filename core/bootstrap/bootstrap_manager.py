"""
=========================================
GENESIS CORE

Arquivo:
core/bootstrap/bootstrap_manager.py

Descrição:
Gerenciador responsável pela construção,
injeção de dependências e inicialização
do ecossistema Genesis.

Responsável por:
- Dependency Injection
- Construção de componentes
- Ordem de boot
- Registro global
- Ciclo de vida

Arquitetura:
Genesis Core

Mark:
III - Matrix

Autor:
Caio Vitor Malveira
=========================================
"""

import inspect
import threading
from typing import Any, Dict, List, Optional

from core.bootstrap.manifest import (
    get_boot_components
)
from core.base.module import (
    Module,
    ModuleStatus
)


class BootstrapManager:
    """
    Construtor central do Genesis.

    O Bootstrap não possui inteligência.
    Ele apenas monta o organismo.
    """

    def __init__(
        self,
        logger: Optional[Any] = None
    ) -> None:
        self.logger = logger
        self._components: Dict[str, Any] = {}
        self._manifest: List[Dict[str, Any]] = []
        self._registry: Optional[Any] = None
        self._lock = threading.RLock()

    # ======================================================
    # BUILD PRINCIPAL
    # ======================================================

    def build(self) -> Dict[str, Any]:
        """Executa a construção completa e inicialização do ecossistema."""
        with self._lock:
            self.clear()

            self._manifest = get_boot_components()

            for component in self._manifest:
                self._build_component(component)

            self._initialize_components()
            self._register_components()

            self.info("Bootstrap concluído.")

            return dict(self._components)

    # ======================================================
    # CRIAÇÃO DE COMPONENTES
    # ======================================================

    def _build_component(
        self,
        component: Dict[str, Any]
    ) -> None:
        """Constrói um componente individual resolvendo suas dependências."""
        name = component["name"]

        if name in self._components:
            raise RuntimeError(
                f"Componente duplicado: {name}"
            )

        cls = component["class"]
        kwargs: Dict[str, Any] = {}

        dependencies = component.get("constructor", [])

        for dependency in dependencies:
            instance = self.get(dependency)

            if instance is None:
                if component.get("required", False):
                    raise RuntimeError(
                        f"Dependência '{dependency}' "
                        f"ausente para '{name}'."
                    )
                continue

            kwargs[dependency] = instance

        try:
            signature = inspect.signature(cls.__init__)
            accepts_kwargs = any(
                param.kind == inspect.Parameter.VAR_KEYWORD
                for param in signature.parameters.values()
            )

            if not accepts_kwargs:
                allowed = set(signature.parameters.keys())
                kwargs = {
                    key: value
                    for key, value in kwargs.items()
                    if key in allowed
                }

            instance = (
                cls(**kwargs)
                if kwargs
                else cls()
            )

        except Exception as error:
            raise RuntimeError(
                f"Falha ao criar {name}: {error}"
            )

        self._components[name] = instance

        if name == "registry":
            self._registry = instance

        self.info(f"Criado: {name}")

    # ======================================================
    # INICIALIZAÇÃO
    # ======================================================

    def _initialize_components(self) -> None:
        """Inicializa todos os módulos criados que herdam de Module."""
        for name, component in self._components.items():
            if isinstance(component, Module):
                try:
                    component.initialize()
                    self.info(f"Inicializado: {name}")
                except Exception as error:
                    component.set_error(str(error))
                    raise RuntimeError(
                        f"Erro iniciando {name}: {error}"
                    )

    # ======================================================
    # REGISTRY
    # ======================================================

    def _register_components(self) -> None:
        """Registra os componentes no registro global se disponível."""
        if not self._registry:
            return

        if not hasattr(self._registry, "register"):
            return

        for component in self._manifest:
            name = component["name"]
            instance = self.get(name)

            if instance:
                try:
                    self._registry.register(
                        name,
                        instance,
                        component.get("category", "module")
                    )
                except Exception as error:
                    self.warning(
                        f"Falha registry {name}: {error}"
                    )

    # ======================================================
    # SHUTDOWN
    # ======================================================

    def shutdown(self) -> None:
        """Encerra graciosamente todos os componentes ativos em ordem reversa."""
        with self._lock:
            components = list(self._components.values())

            for component in reversed(components):
                if isinstance(component, Module):
                    try:
                        component.shutdown()
                    except Exception as error:
                        self.warning(str(error))

            self.clear()

    # ======================================================
    # CONSULTAS
    # ======================================================

    def get(self, name: str) -> Optional[Any]:
        """Retorna um componente pelo nome de forma segura."""
        with self._lock:
            return self._components.get(name)

    def exists(self, name: str) -> bool:
        """Verifica se um componente existe."""
        with self._lock:
            return name in self._components

    def all(self) -> Dict[str, Any]:
        """Retorna uma cópia de todos os componentes."""
        with self._lock:
            return dict(self._components)

    def count(self) -> int:
        """Retorna o total de componentes carregados."""
        with self._lock:
            return len(self._components)

    def registry(self) -> Optional[Any]:
        """Retorna a instância do registro global."""
        return self._registry

    # ======================================================
    # LIMPEZA
    # ======================================================

    def clear(self) -> None:
        """Limpa o dicionário de componentes e referências."""
        self._components.clear()
        self._registry = None

    # ======================================================
    # LOGGING
    # ======================================================

    def info(self, message: str) -> None:
        """Registra log informativo."""
        if self.logger and hasattr(self.logger, "info"):
            self.logger.info(message)

    def warning(self, message: str) -> None:
        """Registra log de aviso."""
        if self.logger and hasattr(self.logger, "warning"):
            self.logger.warning(message)