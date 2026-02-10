"""Constantes globales para la MiniShell."""
from __future__ import annotations

# Permisos de archivos (modo octal)
DEFAULT_DIR_MODE: int = 0o755
DEFAULT_FILE_MODE: int = 0o644

# Límites
MAX_PROCESS_LIST: int = 10
HELP_COMMAND_PADDING: int = 8

# Confirmación de usuario
CONFIRM_YES: str = "s"
CONFIRM_NO: str = "n"

# Flags de comandos
FLAG_RECURSIVE: str = "-r"
FLAG_RECURSIVE_LONG: str = "--recursive"

# Mensajes de UI
MSG_WELCOME: str = "👋 Bienvenido/a a la MiniShell educativa."
MSG_HELP_HINT: str = "   Escribe 'help' para ver comandos, 'exit' para salir."
MSG_GOODBYE: str = "👋 Saliendo de la MiniShell. ¡Sigue practicando en la terminal real!"
MSG_UNKNOWN_CMD: str = "❌ Comando no reconocido:"
MSG_USE_HELP: str = "   Usa 'help' para ver la lista de comandos disponibles."

# Iconos
ICON_SUCCESS: str = "✅"
ICON_ERROR: str = "❌"
ICON_WARNING: str = "⚠️"
ICON_DENIED: str = "⛔"
ICON_INFO: str = "ℹ️"
ICON_FOLDER: str = "📂"
ICON_FOLDER_OPEN: str = "📁"
ICON_TRASH: str = "🗑️"
ICON_BOOK: str = "📖"
ICON_BRAIN: str = "🧠"
ICON_CANCELLED: str = "❎"

# Comandos de salida
EXIT_COMMANDS: tuple[str, ...] = ("exit", "quit")
