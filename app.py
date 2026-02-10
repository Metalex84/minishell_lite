#!/usr/bin/env python3
"""Punto de entrada de la MiniShell educativa."""
from __future__ import annotations

from minishell import MiniShell


def main() -> None:
    """Función principal que inicia la shell."""
    shell = MiniShell()
    shell.run()


if __name__ == "__main__":
    main()
