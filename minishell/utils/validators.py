"""Funciones de validación y utilidades."""
from __future__ import annotations

from pathlib import Path

from minishell.constants import CONFIRM_YES


def parse_octal(value: str) -> int | None:
    """Parsea un string como número octal.
    
    Args:
        value: String con el valor octal (ej: "755", "644").
        
    Returns:
        Valor entero si es válido, None si no.
    """
    try:
        return int(value, 8)
    except ValueError:
        return None


def confirm_action(message: str) -> bool:
    """Solicita confirmación del usuario.
    
    Args:
        message: Mensaje a mostrar al usuario.
        
    Returns:
        True si el usuario confirma, False en caso contrario.
    """
    try:
        response = input(f"{message} (s/N): ").strip().lower()
        return response == CONFIRM_YES
    except (EOFError, KeyboardInterrupt):
        return False


def validate_path_safe(path: str, base_dir: str | None = None) -> tuple[bool, str]:
    """Valida que una ruta sea segura.
    
    Verifica que la ruta no intente escapar del directorio base
    usando secuencias como '..'.
    
    Args:
        path: Ruta a validar.
        base_dir: Directorio base opcional para restringir acceso.
        
    Returns:
        Tupla (es_válida, mensaje_error).
    """
    try:
        resolved = Path(path).resolve()
        
        if base_dir is not None:
            base_resolved = Path(base_dir).resolve()
            try:
                resolved.relative_to(base_resolved)
            except ValueError:
                return False, f"La ruta está fuera del directorio permitido: {base_dir}"
        
        return True, ""
    except Exception as e:
        return False, f"Ruta inválida: {e}"


def count_items_recursive(path: str) -> int:
    """Cuenta el número de elementos en un directorio recursivamente.
    
    Args:
        path: Ruta del directorio.
        
    Returns:
        Número total de archivos y directorios.
    """
    try:
        count = 0
        for _ in Path(path).rglob("*"):
            count += 1
        return count
    except (PermissionError, OSError):
        return -1  # Indica error
