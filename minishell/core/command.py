"""Clase base abstracta para comandos."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from minishell.core.result import CommandResult

if TYPE_CHECKING:
    from minishell.core.shell import MiniShell


class Command(ABC):
    """Clase base abstracta para todos los comandos de la shell.
    
    Cada comando debe implementar el método execute() y definir
    los atributos de clase name, help_text y opcionalmente pedagogical_note.
    
    Attributes:
        name: Nombre del comando (usado para invocarlo).
        help_text: Descripción breve del comando.
        pedagogical_note: Nota educativa sobre el concepto que enseña.
    """
    name: str = ""
    help_text: str = ""
    pedagogical_note: str = ""
    
    @abstractmethod
    def execute(self, args: list[str]) -> CommandResult:
        """Ejecuta el comando con los argumentos dados.
        
        Args:
            args: Lista de argumentos pasados al comando.
            
        Returns:
            CommandResult con el resultado de la ejecución.
        """
        raise NotImplementedError
    
    def execute_with_context(self, shell: MiniShell, args: list[str]) -> CommandResult:
        """Ejecuta el comando con acceso al contexto de la shell.
        
        Algunos comandos (como help) necesitan acceso a la shell.
        Por defecto, delega a execute() ignorando el contexto.
        
        Args:
            shell: Instancia de MiniShell para acceder al contexto.
            args: Lista de argumentos pasados al comando.
            
        Returns:
            CommandResult con el resultado de la ejecución.
        """
        return self.execute(args)
