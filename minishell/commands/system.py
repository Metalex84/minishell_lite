"""Comandos relacionados con información del sistema."""
from __future__ import annotations

from minishell.core.command import Command
from minishell.core.result import CommandResult
from minishell.core.registry import register
from minishell.services.process import ProcessService
from minishell.constants import MAX_PROCESS_LIST, ICON_INFO, ICON_BRAIN, ICON_WARNING


# Servicio compartido para comandos de sistema
_process_service = ProcessService()


@register
class PsCommand(Command):
    """Muestra los procesos en ejecución."""
    
    name = "ps"
    help_text = "Muestra procesos en ejecución (requiere psutil). Uso: ps"
    pedagogical_note = (
        "Ver los procesos en ejecución te permite entender que el sistema operativo gestiona "
        "muchos programas a la vez, cada uno con su identificador de proceso (PID)."
    )

    def execute(self, args: list[str]) -> CommandResult:
        if not _process_service.is_available():
            return CommandResult.error(
                f"{ICON_WARNING} psutil no está instalado. "
                "Instálalo con 'pip install psutil' para usar este comando."
            )
        
        try:
            processes = list(_process_service.list_processes(MAX_PROCESS_LIST))
        except RuntimeError as e:
            return CommandResult.error(str(e))
        
        lines = [f"  PID {p.pid:5} - {p.name}" for p in processes]
        output = "\n".join(lines)
        
        return CommandResult.ok(
            message=f"{ICON_BRAIN} Procesos en ejecución (primeros {MAX_PROCESS_LIST}):\n{output}",
            data=processes,
            tip=self.pedagogical_note,
        )


@register
class InfoCommand(Command):
    """Muestra información del sistema."""
    
    name = "info"
    help_text = "Muestra información básica del sistema. Uso: info"
    pedagogical_note = (
        "Conocer información del sistema (tipo de OS, versión, arquitectura) es útil para "
        "entender en qué entorno se ejecutan tus programas y qué diferencias puede haber "
        "entre Linux, Windows u otros sistemas."
    )

    def execute(self, args: list[str]) -> CommandResult:
        info = _process_service.get_system_info()
        
        output = (
            f"  Sistema : {info.system}\n"
            f"  Nodo    : {info.node}\n"
            f"  Release : {info.release}\n"
            f"  Versión : {info.version}\n"
            f"  Máquina : {info.machine}\n"
            f"  CPU     : {info.processor}"
        )
        
        return CommandResult.ok(
            message=f"{ICON_INFO} Información del sistema:\n{output}",
            data=info,
            tip=self.pedagogical_note,
        )
