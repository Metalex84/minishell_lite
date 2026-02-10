"""Comandos relacionados con el sistema de archivos."""
from __future__ import annotations

from minishell.core.command import Command
from minishell.core.result import CommandResult
from minishell.core.registry import register
from minishell.services.filesystem import FileSystemService
from minishell.utils.decorators import handle_fs_errors, require_args
from minishell.utils.validators import parse_octal, confirm_action, count_items_recursive
from minishell.constants import (
    DEFAULT_DIR_MODE,
    FLAG_RECURSIVE,
    FLAG_RECURSIVE_LONG,
    ICON_SUCCESS,
    ICON_FOLDER,
    ICON_FOLDER_OPEN,
    ICON_TRASH,
    ICON_ERROR,
    ICON_CANCELLED,
)


# Servicio compartido para comandos de filesystem
_fs_service = FileSystemService()


@register
class PwdCommand(Command):
    """Muestra el directorio de trabajo actual."""
    
    name = "pwd"
    help_text = "Muestra el directorio de trabajo actual."
    pedagogical_note = (
        "Este comando te ayuda a entender el concepto de 'directorio actual', "
        "que es el punto de referencia para rutas relativas."
    )

    def execute(self, args: list[str]) -> CommandResult:
        cwd = _fs_service.getcwd()
        return CommandResult.ok(
            message=f"{ICON_FOLDER} Directorio actual:\n{cwd}",
            data=cwd,
            tip=self.pedagogical_note,
        )


@register
class CdCommand(Command):
    """Cambia el directorio de trabajo actual."""
    
    name = "cd"
    help_text = "Cambia el directorio actual. Uso: cd RUTA"
    pedagogical_note = (
        "Al cambiar de directorio practicas el uso de rutas relativas y absolutas, "
        "un concepto clave para navegar por cualquier sistema de archivos."
    )

    @handle_fs_errors
    @require_args(1, "cd RUTA")
    def execute(self, args: list[str]) -> CommandResult:
        path = args[0]
        _fs_service.chdir(path)
        new_cwd = _fs_service.getcwd()
        return CommandResult.ok(
            message=f"{ICON_SUCCESS} Ahora estás en: {new_cwd}",
            data=new_cwd,
            tip=self.pedagogical_note,
        )


@register
class LsCommand(Command):
    """Lista el contenido de un directorio."""
    
    name = "ls"
    help_text = "Lista el contenido de un directorio. Uso: ls [RUTA]"
    pedagogical_note = (
        "Listar el contenido de un directorio te permite visualizar la estructura de "
        "carpetas y ficheros, similar al explorador gráfico pero en modo texto."
    )

    @handle_fs_errors
    def execute(self, args: list[str]) -> CommandResult:
        path = args[0] if args else "."
        entries = _fs_service.listdir(path)
        abs_path = _fs_service.abspath(path)
        
        entries_text = "\n".join(f"  - {e}" for e in entries)
        return CommandResult.ok(
            message=f"{ICON_FOLDER_OPEN} Contenido de {abs_path}:\n{entries_text}",
            data=entries,
            tip=self.pedagogical_note,
        )


@register
class MkdirCommand(Command):
    """Crea un nuevo directorio."""
    
    name = "mkdir"
    help_text = "Crea un directorio. Uso: mkdir NOMBRE"
    pedagogical_note = (
        "Crear directorios te ayuda a organizar información en jerarquías, "
        "un principio básico en la gestión de sistemas de archivos."
    )

    @handle_fs_errors
    @require_args(1, "mkdir NOMBRE")
    def execute(self, args: list[str]) -> CommandResult:
        name = args[0]
        _fs_service.mkdir(name, DEFAULT_DIR_MODE)
        return CommandResult.ok(
            message=f"{ICON_SUCCESS} Directorio creado: {name}",
            data=name,
            tip=self.pedagogical_note,
        )


@register
class TouchCommand(Command):
    """Crea un archivo vacío o actualiza su timestamp."""
    
    name = "touch"
    help_text = "Crea un fichero vacío o actualiza su marca de tiempo. Uso: touch FICHERO"
    pedagogical_note = (
        "Con este comando practicas la creación de ficheros y la idea de 'marca de tiempo', "
        "que registra cuándo se modifica un archivo."
    )

    @handle_fs_errors
    @require_args(1, "touch FICHERO")
    def execute(self, args: list[str]) -> CommandResult:
        name = args[0]
        _fs_service.touch(name)
        return CommandResult.ok(
            message=f"{ICON_SUCCESS} Fichero actualizado/creado: {name}",
            data=name,
            tip=self.pedagogical_note,
        )


@register
class ChmodCommand(Command):
    """Cambia los permisos de un archivo."""
    
    name = "chmod"
    help_text = "Cambia permisos de un fichero. Uso: chmod MODO FICHERO (ej: chmod 644 notas.txt)"
    pedagogical_note = (
        "Este comando introduce el modelo de permisos (lectura, escritura, ejecución) y "
        "los modos octales (como 644 o 755). En Windows, muchos de estos bits no tienen efecto real."
    )

    @handle_fs_errors
    @require_args(2, "chmod MODO FICHERO")
    def execute(self, args: list[str]) -> CommandResult:
        mode_str, path = args[0], args[1]
        mode = parse_octal(mode_str)
        
        if mode is None:
            return CommandResult.error(
                f"{ICON_ERROR} Modo inválido (usa octal, p.ej. 644, 755)"
            )
        
        _fs_service.chmod(path, mode)
        return CommandResult.ok(
            message=f"{ICON_SUCCESS} Permisos cambiados para: {path}",
            data={"path": path, "mode": mode_str},
            tip=self.pedagogical_note,
        )


@register
class RmCommand(Command):
    """Elimina archivos o directorios."""
    
    name = "rm"
    help_text = "Borra un archivo o directorio. Uso: rm RUTA | rm -r RUTA (recursivo)"
    pedagogical_note = (
        "Borrar archivos o directorios refuerza la idea de que las operaciones en el sistema de archivos "
        "son destructivas y no siempre reversibles. El modo recursivo (-r) elimina jerarquías completas."
    )

    @handle_fs_errors
    def execute(self, args: list[str]) -> CommandResult:
        if not args:
            return CommandResult.usage("rm RUTA | rm -r RUTA")
        
        # Detectar modo recursivo
        recursive = False
        if args[0] in (FLAG_RECURSIVE, FLAG_RECURSIVE_LONG):
            recursive = True
            args = args[1:]
        
        if not args:
            return CommandResult.usage("Especifica la ruta a borrar")
        
        path = args[0]
        
        if not _fs_service.exists(path):
            return CommandResult.error(f"{ICON_ERROR} No existe: {path}")
        
        # Determinar tipo de operación
        is_dir = _fs_service.isdir(path)
        
        if recursive and is_dir:
            item_count = count_items_recursive(path)
            what = f"directorio y TODO su contenido ({item_count} elementos)"
        elif is_dir:
            what = "directorio vacío"
        else:
            what = "fichero"
        
        # Solicitar confirmación
        if not confirm_action(f"⚠️ ¿Seguro que quieres borrar '{path}' ({what})?"):
            return CommandResult.ok(f"{ICON_CANCELLED} Operación cancelada.")
        
        # Ejecutar borrado
        if recursive and is_dir:
            _fs_service.rmtree(path)
            return CommandResult.ok(
                message=f"{ICON_TRASH} Directorio borrado RECURSIVAMENTE: {path}",
                tip=self.pedagogical_note,
            )
        elif is_dir:
            _fs_service.rmdir(path)
            return CommandResult.ok(
                message=f"{ICON_TRASH} Directorio vacío borrado: {path}",
                tip=self.pedagogical_note,
            )
        else:
            _fs_service.remove(path)
            return CommandResult.ok(
                message=f"{ICON_TRASH} Fichero borrado: {path}",
                tip=self.pedagogical_note,
            )
