"""Servicio de abstracción sobre el sistema de archivos."""
from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class FileSystemProtocol(Protocol):
    """Protocolo para operaciones del sistema de archivos.
    
    Define la interfaz que debe implementar cualquier servicio
    de sistema de archivos, permitiendo inyección de dependencias
    y facilitando el testing con mocks.
    """
    
    def getcwd(self) -> str: ...
    def chdir(self, path: str) -> None: ...
    def listdir(self, path: str) -> list[str]: ...
    def mkdir(self, path: str, mode: int) -> None: ...
    def touch(self, path: str) -> None: ...
    def chmod(self, path: str, mode: int) -> None: ...
    def remove(self, path: str) -> None: ...
    def rmdir(self, path: str) -> None: ...
    def rmtree(self, path: str) -> None: ...
    def exists(self, path: str) -> bool: ...
    def isdir(self, path: str) -> bool: ...
    def isfile(self, path: str) -> bool: ...
    def abspath(self, path: str) -> str: ...


class FileSystemService:
    """Implementación concreta del servicio de sistema de archivos.
    
    Encapsula las operaciones de os, shutil y pathlib, proporcionando
    una interfaz unificada y facilitando el testing.
    """
    
    def __init__(self, sandbox_root: str | None = None) -> None:
        """Inicializa el servicio.
        
        Args:
            sandbox_root: Si se especifica, restringe operaciones a este directorio.
        """
        self._sandbox_root = Path(sandbox_root).resolve() if sandbox_root else None
    
    def _validate_path(self, path: str) -> Path:
        """Valida que la ruta esté dentro del sandbox si está configurado.
        
        Args:
            path: Ruta a validar.
            
        Returns:
            Path resuelto y validado.
            
        Raises:
            PermissionError: Si la ruta está fuera del sandbox.
        """
        resolved = Path(path).resolve()
        if self._sandbox_root is not None:
            try:
                resolved.relative_to(self._sandbox_root)
            except ValueError:
                raise PermissionError(
                    f"Acceso denegado: la ruta está fuera del directorio permitido"
                )
        return resolved
    
    def getcwd(self) -> str:
        """Obtiene el directorio de trabajo actual."""
        return os.getcwd()
    
    def chdir(self, path: str) -> None:
        """Cambia el directorio de trabajo actual."""
        self._validate_path(path)
        os.chdir(path)
    
    def listdir(self, path: str = ".") -> list[str]:
        """Lista el contenido de un directorio."""
        self._validate_path(path)
        return os.listdir(path)
    
    def mkdir(self, path: str, mode: int = 0o755) -> None:
        """Crea un directorio."""
        self._validate_path(path)
        os.mkdir(path, mode)
    
    def touch(self, path: str) -> None:
        """Crea un archivo vacío o actualiza su timestamp."""
        self._validate_path(path)
        with open(path, "a"):
            os.utime(path, None)
    
    def chmod(self, path: str, mode: int) -> None:
        """Cambia los permisos de un archivo."""
        self._validate_path(path)
        os.chmod(path, mode)
    
    def remove(self, path: str) -> None:
        """Elimina un archivo."""
        self._validate_path(path)
        os.remove(path)
    
    def rmdir(self, path: str) -> None:
        """Elimina un directorio vacío."""
        self._validate_path(path)
        os.rmdir(path)
    
    def rmtree(self, path: str) -> None:
        """Elimina un directorio y todo su contenido recursivamente."""
        self._validate_path(path)
        shutil.rmtree(path)
    
    def exists(self, path: str) -> bool:
        """Verifica si existe una ruta."""
        return os.path.exists(path)
    
    def isdir(self, path: str) -> bool:
        """Verifica si la ruta es un directorio."""
        return os.path.isdir(path)
    
    def isfile(self, path: str) -> bool:
        """Verifica si la ruta es un archivo."""
        return os.path.isfile(path)
    
    def abspath(self, path: str) -> str:
        """Obtiene la ruta absoluta."""
        return os.path.abspath(path)
