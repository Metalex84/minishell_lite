"""Servicio de abstracción sobre procesos del sistema."""
from __future__ import annotations

import platform
from dataclasses import dataclass
from typing import Iterator, Protocol, runtime_checkable

# Importación opcional de psutil
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    psutil = None  # type: ignore
    HAS_PSUTIL = False


@dataclass
class ProcessInfo:
    """Información básica de un proceso."""
    pid: int
    name: str


@dataclass
class SystemInfo:
    """Información del sistema."""
    system: str
    node: str
    release: str
    version: str
    machine: str
    processor: str


@runtime_checkable
class ProcessProtocol(Protocol):
    """Protocolo para operaciones de procesos."""
    
    def list_processes(self, limit: int) -> Iterator[ProcessInfo]: ...
    def get_system_info(self) -> SystemInfo: ...
    def is_available(self) -> bool: ...


class ProcessService:
    """Implementación concreta del servicio de procesos.
    
    Encapsula las operaciones de psutil y platform.
    """
    
    def is_available(self) -> bool:
        """Verifica si psutil está disponible."""
        return HAS_PSUTIL
    
    def list_processes(self, limit: int = 10) -> Iterator[ProcessInfo]:
        """Lista los procesos en ejecución.
        
        Args:
            limit: Número máximo de procesos a listar.
            
        Yields:
            ProcessInfo para cada proceso.
            
        Raises:
            RuntimeError: Si psutil no está instalado.
        """
        if not HAS_PSUTIL or psutil is None:
            raise RuntimeError(
                "psutil no está instalado. Instálalo con 'pip install psutil'"
            )
        
        count = 0
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                info = proc.info
                yield ProcessInfo(pid=info["pid"], name=info["name"])
                count += 1
                if count >= limit:
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def get_system_info(self) -> SystemInfo:
        """Obtiene información del sistema."""
        uname = platform.uname()
        return SystemInfo(
            system=uname.system,
            node=uname.node,
            release=uname.release,
            version=uname.version,
            machine=uname.machine,
            processor=uname.processor,
        )
