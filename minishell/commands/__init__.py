"""Comandos de la MiniShell.

Este módulo importa todos los comandos para que se registren automáticamente.
"""
from __future__ import annotations

# Importar todos los módulos de comandos para activar el auto-registro
from minishell.commands import filesystem
from minishell.commands import system
from minishell.commands import help

__all__ = ["filesystem", "system", "help"]
