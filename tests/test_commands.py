"""Tests para comandos de la MiniShell."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from minishell.core.result import CommandResult
from minishell.core.registry import clear_registry, get_registered_commands


# Importar comandos una vez al inicio para asegurar que están registrados
import minishell.commands  # noqa: F401


class TestCommandResult:
    """Tests para CommandResult."""

    def test_ok_creates_success_result(self) -> None:
        result = CommandResult.ok("Success message", data={"key": "value"})
        assert result.success is True
        assert result.message == "Success message"
        assert result.data == {"key": "value"}

    def test_error_creates_failure_result(self) -> None:
        result = CommandResult.error("Error message")
        assert result.success is False
        assert result.message == "Error message"

    def test_usage_creates_usage_result(self) -> None:
        result = CommandResult.usage("command ARG")
        assert result.success is False
        assert "Uso:" in result.message
        assert "command ARG" in result.message


class TestPwdCommand:
    """Tests para PwdCommand."""

    def test_pwd_returns_current_directory(self) -> None:
        from minishell.commands.filesystem import PwdCommand
        
        cmd = PwdCommand()
        result = cmd.execute([])
        
        assert result.success is True
        assert os.getcwd() in result.message
        assert result.data == os.getcwd()


class TestCdCommand:
    """Tests para CdCommand."""

    def test_cd_without_args_returns_usage(self) -> None:
        from minishell.commands.filesystem import CdCommand
        
        cmd = CdCommand()
        result = cmd.execute([])
        
        assert result.success is False
        assert "Uso:" in result.message

    def test_cd_to_valid_directory(self) -> None:
        from minishell.commands.filesystem import CdCommand
        
        cmd = CdCommand()
        original_dir = os.getcwd()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = cmd.execute([tmpdir])
            assert result.success is True
            assert os.getcwd() == tmpdir
            
            # Restaurar directorio original
            os.chdir(original_dir)

    def test_cd_to_nonexistent_directory(self) -> None:
        from minishell.commands.filesystem import CdCommand
        
        cmd = CdCommand()
        result = cmd.execute(["/nonexistent/path/that/does/not/exist"])
        
        assert result.success is False
        assert "No encontrado" in result.message


class TestLsCommand:
    """Tests para LsCommand."""

    def test_ls_current_directory(self) -> None:
        from minishell.commands.filesystem import LsCommand
        
        cmd = LsCommand()
        result = cmd.execute([])
        
        assert result.success is True
        assert isinstance(result.data, list)

    def test_ls_with_path(self) -> None:
        from minishell.commands.filesystem import LsCommand
        
        cmd = LsCommand()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear algunos archivos
            (Path(tmpdir) / "file1.txt").touch()
            (Path(tmpdir) / "file2.txt").touch()
            
            result = cmd.execute([tmpdir])
            
            assert result.success is True
            assert "file1.txt" in result.data
            assert "file2.txt" in result.data


class TestMkdirCommand:
    """Tests para MkdirCommand."""

    def test_mkdir_creates_directory(self) -> None:
        from minishell.commands.filesystem import MkdirCommand
        
        cmd = MkdirCommand()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = Path(tmpdir) / "new_directory"
            result = cmd.execute([str(new_dir)])
            
            assert result.success is True
            assert new_dir.exists()
            assert new_dir.is_dir()

    def test_mkdir_without_args_returns_usage(self) -> None:
        from minishell.commands.filesystem import MkdirCommand
        
        cmd = MkdirCommand()
        result = cmd.execute([])
        
        assert result.success is False
        assert "Uso:" in result.message


class TestTouchCommand:
    """Tests para TouchCommand."""

    def test_touch_creates_file(self) -> None:
        from minishell.commands.filesystem import TouchCommand
        
        cmd = TouchCommand()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            new_file = Path(tmpdir) / "new_file.txt"
            result = cmd.execute([str(new_file)])
            
            assert result.success is True
            assert new_file.exists()
            assert new_file.is_file()

    def test_touch_without_args_returns_usage(self) -> None:
        from minishell.commands.filesystem import TouchCommand
        
        cmd = TouchCommand()
        result = cmd.execute([])
        
        assert result.success is False
        assert "Uso:" in result.message


class TestChmodCommand:
    """Tests para ChmodCommand."""

    def test_chmod_without_args_returns_usage(self) -> None:
        from minishell.commands.filesystem import ChmodCommand
        
        cmd = ChmodCommand()
        result = cmd.execute([])
        
        assert result.success is False
        assert "Uso:" in result.message

    def test_chmod_with_invalid_mode(self) -> None:
        from minishell.commands.filesystem import ChmodCommand
        
        cmd = ChmodCommand()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_file.txt"
            test_file.touch()
            result = cmd.execute(["invalid", str(test_file)])
            assert result.success is False
            assert "inválido" in result.message.lower()


class TestInfoCommand:
    """Tests para InfoCommand."""

    def test_info_returns_system_info(self) -> None:
        from minishell.commands.system import InfoCommand
        
        cmd = InfoCommand()
        result = cmd.execute([])
        
        assert result.success is True
        assert "Sistema" in result.message
        assert result.data is not None


class TestHelpCommand:
    """Tests para HelpCommand."""

    def test_help_requires_context(self) -> None:
        from minishell.commands.help import HelpCommand
        
        cmd = HelpCommand()
        # execute() sin contexto debe fallar
        result = cmd.execute([])
        assert result.success is False

    def test_help_with_context_lists_commands(self) -> None:
        from minishell.commands.help import HelpCommand
        from minishell.core.shell import MiniShell
        
        shell = MiniShell()
        cmd = HelpCommand()
        
        result = cmd.execute_with_context(shell, [])
        
        assert result.success is True
        assert "pwd" in result.message
        assert "ls" in result.message

    def test_help_specific_command(self) -> None:
        from minishell.commands.help import HelpCommand
        from minishell.core.shell import MiniShell
        
        shell = MiniShell()
        cmd = HelpCommand()
        
        result = cmd.execute_with_context(shell, ["pwd"])
        
        assert result.success is True
        assert "pwd" in result.message
