"""Resultado de ejecución de comandos."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CommandResult:
    """Representa el resultado de la ejecución de un comando.
    
    Separa la lógica de ejecución de la presentación, permitiendo
    que los comandos devuelvan datos estructurados en lugar de
    imprimir directamente.
    
    Attributes:
        success: Indica si el comando se ejecutó correctamente.
        message: Mensaje principal para mostrar al usuario.
        data: Datos adicionales devueltos por el comando.
        tip: Nota pedagógica opcional para mostrar.
    """
    success: bool
    message: str = ""
    data: Any = None
    tip: str = ""
    
    @classmethod
    def ok(cls, message: str = "", data: Any = None, tip: str = "") -> CommandResult:
        """Crea un resultado exitoso."""
        return cls(success=True, message=message, data=data, tip=tip)
    
    @classmethod
    def error(cls, message: str, data: Any = None) -> CommandResult:
        """Crea un resultado de error."""
        return cls(success=False, message=message, data=data)
    
    @classmethod
    def usage(cls, usage_text: str) -> CommandResult:
        """Crea un resultado indicando uso incorrecto."""
        return cls(success=False, message=f"⚠️ Uso: {usage_text}")
