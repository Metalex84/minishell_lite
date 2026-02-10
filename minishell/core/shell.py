"""Shell principal de la aplicación."""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from minishell.core.result import CommandResult
from minishell.core.registry import get_registered_commands
from minishell.constants import (
    MSG_WELCOME,
    MSG_HELP_HINT,
    MSG_GOODBYE,
    MSG_UNKNOWN_CMD,
    MSG_USE_HELP,
    EXIT_COMMANDS,
)

if TYPE_CHECKING:
    from minishell.core.command import Command


class MiniShell:
    """Mini shell educativa basada en el módulo os y algunas librerías auxiliares.
    
    La shell carga automáticamente todos los comandos registrados con el decorador
    @register y proporciona un REPL interactivo.
    
    Attributes:
        commands: Diccionario de comandos disponibles (nombre -> instancia).
    """

    def __init__(self) -> None:
        """Inicializa la shell cargando los comandos registrados."""
        self.commands: dict[str, Command] = {}
        self._load_commands()

    def _load_commands(self) -> None:
        """Carga todos los comandos registrados.
        
        Importa el módulo de comandos para activar el auto-registro
        y luego instancia cada comando.
        """
        # Importar comandos para activar el registro
        import minishell.commands  # noqa: F401
        
        # Instanciar cada comando registrado
        for name, cls in get_registered_commands().items():
            self.commands[name] = cls()

    def _display_result(self, result: CommandResult) -> None:
        """Muestra el resultado de un comando al usuario.
        
        Args:
            result: Resultado del comando a mostrar.
        """
        if result.message:
            print(result.message)
        if result.tip:
            print("TIP:", result.tip)

    def run(self) -> None:
        """Ejecuta el loop principal de la shell (REPL)."""
        print(MSG_WELCOME)
        print(MSG_HELP_HINT)
        
        while True:
            try:
                line = input(f"{os.getcwd()} 💻$ ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

            line = line.strip()
            if not line:
                continue

            parts = line.split()
            cmd_name, args = parts[0], parts[1:]

            if cmd_name in EXIT_COMMANDS:
                print(MSG_GOODBYE)
                break

            cmd = self.commands.get(cmd_name)
            if cmd is None:
                print(MSG_UNKNOWN_CMD, cmd_name)
                print(MSG_USE_HELP)
                continue

            # Ejecutar comando con o sin contexto según sea necesario
            result = cmd.execute_with_context(self, args)
            self._display_result(result)

    def execute_command(self, command_line: str) -> CommandResult | None:
        """Ejecuta un comando programáticamente.
        
        Útil para testing o integración con otras herramientas.
        
        Args:
            command_line: Línea de comando completa a ejecutar.
            
        Returns:
            CommandResult si el comando existe, None si es comando de salida
            o no reconocido.
        """
        parts = command_line.strip().split()
        if not parts:
            return None
            
        cmd_name, args = parts[0], parts[1:]
        
        if cmd_name in EXIT_COMMANDS:
            return None
            
        cmd = self.commands.get(cmd_name)
        if cmd is None:
            return CommandResult.error(f"{MSG_UNKNOWN_CMD} {cmd_name}")
            
        return cmd.execute_with_context(self, args)
