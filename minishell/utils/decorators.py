"""Decoradores para comandos."""
from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar

from minishell.core.result import CommandResult
from minishell.constants import ICON_ERROR, ICON_DENIED

F = TypeVar("F", bound=Callable[..., CommandResult])


def handle_fs_errors(func: F) -> F:
    """Decorador que maneja errores comunes del sistema de archivos.
    
    Captura excepciones típicas de operaciones de archivos y las convierte
    en CommandResult con mensajes apropiados.
    
    Args:
        func: Función que devuelve CommandResult.
        
    Returns:
        Función decorada con manejo de errores.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> CommandResult:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            path = getattr(e, "filename", str(e))
            return CommandResult.error(f"{ICON_ERROR} No encontrado: {path}")
        except FileExistsError as e:
            path = getattr(e, "filename", str(e))
            return CommandResult.error(f"ℹ️ Ya existe: {path}")
        except NotADirectoryError as e:
            path = getattr(e, "filename", str(e))
            return CommandResult.error(f"{ICON_ERROR} No es un directorio: {path}")
        except IsADirectoryError as e:
            path = getattr(e, "filename", str(e))
            return CommandResult.error(f"{ICON_ERROR} Es un directorio: {path}")
        except PermissionError as e:
            path = getattr(e, "filename", str(e))
            return CommandResult.error(f"{ICON_DENIED} Permiso denegado: {path}")
        except OSError as e:
            return CommandResult.error(f"{ICON_ERROR} Error del sistema: {e}")
    return wrapper  # type: ignore


def require_args(min_args: int, usage: str) -> Callable[[F], F]:
    """Decorador que valida el número mínimo de argumentos.
    
    Args:
        min_args: Número mínimo de argumentos requeridos.
        usage: Texto de uso a mostrar si faltan argumentos.
        
    Returns:
        Decorador que valida argumentos.
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(self, args: list[str], *extra_args, **kwargs) -> CommandResult:
            if len(args) < min_args:
                return CommandResult.usage(usage)
            return func(self, args, *extra_args, **kwargs)
        return wrapper  # type: ignore
    return decorator
