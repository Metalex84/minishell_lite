"""Tests para servicios."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from minishell.services.filesystem import FileSystemService
from minishell.services.process import ProcessService


class TestFileSystemService:
    """Tests para FileSystemService."""

    def test_getcwd(self) -> None:
        fs = FileSystemService()
        assert fs.getcwd() == os.getcwd()

    def test_listdir(self) -> None:
        fs = FileSystemService()
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "file.txt").touch()
            entries = fs.listdir(tmpdir)
            assert "file.txt" in entries

    def test_exists(self) -> None:
        fs = FileSystemService()
        with tempfile.TemporaryDirectory() as tmpdir:
            assert fs.exists(tmpdir) is True
            assert fs.exists("/nonexistent/path") is False

    def test_isdir(self) -> None:
        fs = FileSystemService()
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "file.txt"
            file_path.touch()
            assert fs.isdir(tmpdir) is True
            assert fs.isdir(str(file_path)) is False

    def test_isfile(self) -> None:
        fs = FileSystemService()
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "file.txt"
            file_path.touch()
            assert fs.isfile(str(file_path)) is True
            assert fs.isfile(tmpdir) is False


class TestFileSystemServiceSandbox:
    """Tests para el modo sandbox de FileSystemService."""

    def test_sandbox_allows_operations_inside(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = FileSystemService(sandbox_root=tmpdir)
            # Operaciones dentro del sandbox deben funcionar
            entries = fs.listdir(tmpdir)
            assert isinstance(entries, list)

    def test_sandbox_blocks_operations_outside(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = FileSystemService(sandbox_root=tmpdir)
            # Intentar acceder fuera del sandbox
            with pytest.raises(PermissionError):
                fs.listdir("/")


class TestProcessService:
    """Tests para ProcessService."""

    def test_get_system_info(self) -> None:
        ps = ProcessService()
        info = ps.get_system_info()
        
        assert info.system != ""
        assert info.node != ""
        assert info.machine != ""

    def test_is_available(self) -> None:
        ps = ProcessService()
        # Esto depende de si psutil está instalado
        result = ps.is_available()
        assert isinstance(result, bool)

    def test_list_processes_when_available(self) -> None:
        ps = ProcessService()
        if ps.is_available():
            processes = list(ps.list_processes(5))
            assert len(processes) <= 5
            if processes:
                # PID 0 es válido en Windows (System Idle Process)
                assert processes[0].pid >= 0
                assert processes[0].name != ""
