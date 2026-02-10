"""Comando de ayuda."""
from __future__ import annotations

from typing import TYPE_CHECKING

from minishell.core.command import Command
from minishell.core.result import CommandResult
from minishell.core.registry import register
from minishell.constants import ICON_BOOK, ICON_ERROR, HELP_COMMAND_PADDING

if TYPE_CHECKING:
    from minishell.core.shell import MiniShell


@register
class HelpCommand(Command):
    """Muestra la ayuda de comandos disponibles."""
    
    name = "help"
    help_text = "Muestra esta ayuda. Uso: help [COMANDO]"
    pedagogical_note = (
        "Consultar la ayuda es una habilidad esencial: en sistemas reales, la documentación "
        "en línea (man, --help) es tu principal fuente de referencia."
    )

    def execute(self, args: list[str]) -> CommandResult:
        # Este comando necesita contexto, así que devuelve error si se llama sin él
        return CommandResult.error(
            "Este comando requiere contexto de la shell. Usa execute_with_context()."
        )
    
    def execute_with_context(self, shell: MiniShell, args: list[str]) -> CommandResult:
        """Muestra ayuda general o de un comando específico."""
        if not args:
            return self._show_all_commands(shell)
        else:
            return self._show_command_help(shell, args[0])
    
    def _show_all_commands(self, shell: MiniShell) -> CommandResult:
        """Muestra la lista de todos los comandos disponibles."""
        lines = []
        for cmd_name, cmd in sorted(shell.commands.items()):
            lines.append(f"  {cmd_name:<{HELP_COMMAND_PADDING}} - {cmd.help_text}")
        
        output = "\n".join(lines)
        return CommandResult.ok(
            message=f"{ICON_BOOK} Comandos disponibles:\n{output}",
            data=list(shell.commands.keys()),
            tip=self.pedagogical_note,
        )
    
    def _show_command_help(self, shell: MiniShell, cmd_name: str) -> CommandResult:
        """Muestra la ayuda de un comando específico."""
        cmd = shell.commands.get(cmd_name)
        
        if cmd is None:
            return CommandResult.error(f"{ICON_ERROR} Comando no encontrado: {cmd_name}")
        
        message = f"{ICON_BOOK} {cmd_name}: {cmd.help_text}"
        return CommandResult.ok(
            message=message,
            data={"name": cmd_name, "help": cmd.help_text},
            tip=cmd.pedagogical_note if cmd.pedagogical_note else None,
        )
