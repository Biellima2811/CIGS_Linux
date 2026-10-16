"""
Logger centralizado.

Responsabilidade única: escrever mensagens simultaneamente no
console (stdout) e no arquivo de log da operação.

Cada linha é formatada como:
    [NIVEL - HH:MM:SS] - mensagem
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path


class CigsLogger:
    """
    Logger simples com níveis (INFO, OK, ERRO).

    Attributes:
        _log_file (Path): Arquivo onde os logs são acumulados.
    """

    def __init__(self, log_file: Path) -> None:
        """
        Inicializa o logger.

        Args:
            log_file: Caminho do arquivo de log. As pastas-pai
                      são criadas automaticamente caso não existam.
        """
        self._log_file = log_file
        self._log_file.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------
    def _write(self, level: str, message: str) -> None:
        """
        Escreve a mensagem formatada no console E no arquivo.

        Diferente da versão anterior (que gravava apenas `message`
        no arquivo), aqui gravamos a LINHA COMPLETA — incluindo
        nível e timestamp — para permitir auditoria posterior.
        """
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{level} - {ts}] - {message}"

        # Console
        print(line, flush=True)

        # Arquivo (linha completa, não apenas a mensagem)
        with self._log_file.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def raw(self, message: str) -> None:
        """Escreve uma linha crua (sem timestamp) — usado em banners."""
        print(message, flush=True)
        with self._log_file.open("a", encoding="utf-8") as fh:
            fh.write(message + "\n")

    # ------------------------------------------------------------------
    # API pública — níveis de log
    # ------------------------------------------------------------------
    def info(self, msg: str) -> None:
        """Log de informação."""
        self._write("INFO", msg)

    def ok(self, msg: str) -> None:
        """Log de sucesso."""
        self._write("OK", msg)

    def error(self, msg: str) -> None:
        """Log de erro."""
        self._write("ERRO", msg)