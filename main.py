#!/usr/bin/env python3
"""
Ponto de entrada do CIGS.

Este arquivo DEVE ficar na raiz do projeto (fora do pacote CIGS_linux),
caso contrário o interpretador Python não consegue resolver o import
`from CIGS_linux.app import ...`.

Uso:
    python main.py            -> modo interativo (pede chave de segurança)
    python main.py --auto     -> modo silencioso (usado pelo `at`)
"""
from __future__ import annotations

import sys

from CIGS_linux.app import CigsApplication


def main() -> int:
    """
    Entry point da aplicação.

    Returns:
        Código de saída do processo (0 = sucesso).
    """
    modo_auto = "--auto" in sys.argv[1:]
    app = CigsApplication(modo_auto=modo_auto)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())