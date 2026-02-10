"""Registry global para auto-registro de comandos."""
from __future__ import annotations

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from minishell.core.command import Command

# Registry global de comandos
_command_registry: dict[str, Type[Command]] = {}


def register(cls: Type[Command]) -> Type[Command]:
    """Decorador para registrar automáticamente un comando.
    
    Uso:
        @register
        class MiComando(Command):
            name = "micomando"
            ...
    
    Args:
        cls: Clase de comando a registrar.
        
    Returns:
        La misma clase, sin modificar.
        
    Raises:
        ValueError: Si el comando no tiene nombre o ya está registrado.
    """
    if not cls.name:
        raise ValueError(f"El comando {cls.__name__} debe tener un atributo 'name'")
    
    if cls.name in _command_registry:
        raise ValueError(f"Ya existe un comando registrado con nombre '{cls.name}'")
    
    _command_registry[cls.name] = cls
    return cls


def get_registered_commands() -> dict[str, Type[Command]]:
    """Obtiene todos los comandos registrados.
    
    Returns:
        Diccionario de nombre -> clase de comando.
    """
    return _command_registry.copy()


def clear_registry() -> None:
    """Limpia el registry. Útil para testing."""
    _command_registry.clear()
