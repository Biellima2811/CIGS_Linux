"""
Módulo de Agendamento via comando `at`.

Responsável por enfileirar a execução automática do binário
(com flag --auto) em um horário definido pelo operador.
"""
from __future__ import annotations

import subprocess

from .config import CONFIG
from .logger import CigsLogger


class AtScheduler:
    """
    Encapsula chamadas ao `at`.

    Attributes:
        executavel (str): Caminho do binário compilado no servidor.
        logger (CigsLogger): Logger compartilhado.
    """

    # ------------------------------------------------------------------
    # Construtor
    # ------------------------------------------------------------------
    def __init__(self, logger: CigsLogger, executavel: str | None = None) -> None:
        """
        Args:
            logger: Logger compartilhado.
            executavel: Caminho do binário a agendar. Se None, usa
                        CONFIG.EXECUTAVEL_PATH.
        """
        self.executavel = executavel or CONFIG.EXECUTAVEL_PATH
        self.logger = logger

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------
    def agendar(self, horario: str) -> bool:
        """
        Agenda execução no horário informado (formato HH:MM).

        Args:
            horario: Hora no formato 24h, ex: "19:30".

        Returns:
            True em caso de sucesso, False caso contrário.

        Nota: usamos check=False (e não check=True) para que o
        returncode possa ser inspecionado manualmente. Com check=True
        o subprocess lançaria CalledProcessError antes de chegarmos
        ao `if proc.returncode == 0`, derrubando a aplicação.
        """
        comando = f"{self.executavel} --auto"

        try:
            proc = subprocess.run(
                ["at", horario],
                input=comando + "\n",
                text=True,
                capture_output=True,
                check=False,   # <- não explode; inspecionamos o returncode
            )

            if proc.returncode == 0:
                self.logger.ok(f"Operacao agendada para as {horario}")
                return True

            self.logger.error(
                f"Falha ao agendar: {proc.stderr.strip() or 'erro desconhecido'}"
            )
            return False

        except FileNotFoundError:
            self.logger.error(
                "Comando 'at' nao encontrado. Instale com 'apt install at'."
            )
            return False

    def listar(self) -> str:
        """
        Retorna a saída do comando `atq` (fila atual).

        Returns:
            Texto com os agendamentos pendentes, ou mensagem
            informativa caso a fila esteja vazia ou o comando
            não exista.
        """
        try:
            proc = subprocess.run(
                ["atq"],
                capture_output=True,
                text=True,
                check=False,
            )
            return proc.stdout or "(nenhum agendamento pendente)"
        except FileNotFoundError:
            return "Comando 'atq' nao encontrado."