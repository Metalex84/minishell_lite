# 🐚 MiniShell Educativa

Una shell interactiva educativa escrita en Python, diseñada para aprender conceptos básicos de sistemas operativos y línea de comandos.

## 📋 Requisitos

- Python 3.10+
- psutil (opcional, para el comando `ps`)

## 🚀 Instalación

```bash
# Clonar o descargar el proyecto
cd py_minishell

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Uso

```bash
python app.py
```

### Comandos disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `pwd` | Muestra el directorio actual | `pwd` |
| `cd` | Cambia de directorio | `cd ../` |
| `ls` | Lista contenido de un directorio | `ls`, `ls /tmp` |
| `mkdir` | Crea un directorio | `mkdir nueva_carpeta` |
| `touch` | Crea un archivo vacío | `touch archivo.txt` |
| `rm` | Elimina archivos o directorios | `rm archivo.txt`, `rm -r carpeta` |
| `chmod` | Cambia permisos (modo octal) | `chmod 755 script.sh` |
| `ps` | Lista procesos en ejecución | `ps` |
| `info` | Información del sistema | `info` |
| `help` | Muestra ayuda | `help`, `help cd` |
| `exit` | Sale de la shell | `exit` |

Cada comando incluye una **nota pedagógica** que explica el concepto que enseña.

## 🧪 Tests

```bash
# Ejecutar todos los tests
python -m pytest tests -v

# Ejecutar tests con cobertura
python -m pytest tests --cov=minishell
```

## 🏗️ Arquitectura

El proyecto sigue los principios **SOLID** y patrones de **Clean Code**.

### Estructura de directorios

```
py_minishell/
├── minishell/                 # Paquete principal
│   ├── constants.py           # Constantes centralizadas
│   ├── core/                  # Núcleo de la aplicación
│   │   ├── command.py         # Clase abstracta Command
│   │   ├── registry.py        # Sistema de auto-registro
│   │   ├── result.py          # CommandResult (DTO)
│   │   └── shell.py           # Clase MiniShell (REPL)
│   ├── commands/              # Implementación de comandos
│   │   ├── filesystem.py      # Comandos de archivos
│   │   ├── system.py          # Comandos de sistema
│   │   └── help.py            # Comando de ayuda
│   ├── services/              # Capa de servicios
│   │   ├── filesystem.py      # Abstracción del sistema de archivos
│   │   └── process.py         # Abstracción de procesos
│   └── utils/                 # Utilidades
│       ├── decorators.py      # Decoradores reutilizables
│       └── validators.py      # Funciones de validación
├── tests/                     # Tests unitarios
├── app.py                     # Punto de entrada
└── requirements.txt
```

### Principios SOLID aplicados

#### S - Single Responsibility Principle
Cada clase tiene una única responsabilidad:
- **Command**: Define la interfaz de un comando
- **CommandResult**: Encapsula el resultado de ejecución
- **MiniShell**: Gestiona el REPL y coordina comandos
- **FileSystemService**: Abstrae operaciones de archivos

#### O - Open/Closed Principle
El sistema de comandos usa el decorador `@register` para auto-registro:

```python
from minishell.core.registry import register
from minishell.core.command import Command

@register
class MiComando(Command):
    name = "micomando"
    help_text = "Descripción del comando"
    
    def execute(self, args: list[str]) -> CommandResult:
        # Implementación
        return CommandResult.ok("Éxito")
```

Añadir nuevos comandos no requiere modificar código existente.

#### L - Liskov Substitution Principle
Todos los comandos heredan de `Command` y pueden sustituirse entre sí.

#### I - Interface Segregation Principle
- `execute(args)`: Para comandos simples
- `execute_with_context(shell, args)`: Solo para comandos que necesitan contexto (ej: `help`)

#### D - Dependency Inversion Principle
Los comandos dependen de abstracciones (`FileSystemService`, `ProcessService`), no de módulos concretos como `os` o `psutil`.

### Patrones de diseño

- **Registry Pattern**: Auto-registro de comandos con decorador
- **Command Pattern**: Encapsulación de operaciones como objetos
- **Template Method**: Clase base `Command` con métodos hook
- **DTO (Data Transfer Object)**: `CommandResult` para transferir resultados

### Seguridad

`FileSystemService` soporta modo **sandbox** para restringir operaciones a un directorio base:

```python
from minishell.services.filesystem import FileSystemService

# Restringir operaciones a /home/user/workspace
fs = FileSystemService(sandbox_root="/home/user/workspace")
fs.listdir("/etc")  # Lanza PermissionError
```

### Manejo de errores centralizado

El decorador `@handle_fs_errors` captura excepciones comunes y las convierte en `CommandResult`:

```python
from minishell.utils.decorators import handle_fs_errors

@handle_fs_errors
def execute(self, args):
    # FileNotFoundError, PermissionError, etc.
    # se convierten automáticamente en CommandResult.error()
```

## 📝 Licencia

Proyecto educativo de libre uso.
