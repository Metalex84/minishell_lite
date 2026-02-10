"""Tests para funciones de validación."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from minishell.utils.validators import (
    parse_octal,
    validate_path_safe,
    count_items_recursive,
)


class TestParseOctal:
    """Tests para parse_octal()."""

    def test_valid_octal_755(self) -> None:
        assert parse_octal("755") == 0o755

    def test_valid_octal_644(self) -> None:
        assert parse_octal("644") == 0o644

    def test_valid_octal_777(self) -> None:
        assert parse_octal("777") == 0o777

    def test_valid_octal_000(self) -> None:
        assert parse_octal("000") == 0

    def test_invalid_octal_letters(self) -> None:
        assert parse_octal("abc") is None

    def test_invalid_octal_digit_8(self) -> None:
        # 8 no es un dígito octal válido
        assert parse_octal("888") is None

    def test_invalid_octal_empty(self) -> None:
        assert parse_octal("") is None

    def test_invalid_octal_mixed(self) -> None:
        assert parse_octal("75a") is None


class TestValidatePathSafe:
    """Tests para validate_path_safe()."""

    def test_valid_path_no_base(self) -> None:
        is_valid, error = validate_path_safe(".")
        assert is_valid is True
        assert error == ""

    def test_valid_path_with_base(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            is_valid, error = validate_path_safe(str(subdir), tmpdir)
            assert is_valid is True
            assert error == ""

    def test_invalid_path_escapes_base(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Intentar salir del directorio base
            escape_path = str(Path(tmpdir) / ".." / "..")
            is_valid, error = validate_path_safe(escape_path, tmpdir)
            assert is_valid is False
            assert "fuera del directorio" in error.lower()

    def test_absolute_path_outside_base(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Usar una ruta absoluta fuera del base
            other_path = tempfile.gettempdir()
            if Path(other_path).resolve() != Path(tmpdir).resolve():
                is_valid, error = validate_path_safe(other_path, tmpdir)
                assert is_valid is False


class TestCountItemsRecursive:
    """Tests para count_items_recursive()."""

    def test_empty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            count = count_items_recursive(tmpdir)
            assert count == 0

    def test_directory_with_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear algunos archivos
            (Path(tmpdir) / "file1.txt").touch()
            (Path(tmpdir) / "file2.txt").touch()
            count = count_items_recursive(tmpdir)
            assert count == 2

    def test_directory_with_subdirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear estructura de directorios
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            (subdir / "file.txt").touch()
            (Path(tmpdir) / "root_file.txt").touch()
            count = count_items_recursive(tmpdir)
            assert count == 3  # subdir + subdir/file.txt + root_file.txt

    def test_nonexistent_directory(self) -> None:
        # En Windows, rglob en paths no existentes puede no lanzar error
        # sino devolver un iterador vacío, así que aceptamos 0 o -1
        count = count_items_recursive("/nonexistent/path/that/does/not/exist")
        assert count in (0, -1)  # 0 en Windows, -1 si hay error
