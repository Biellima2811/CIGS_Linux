"""
Módulo Tomcat.

Encapsula as operações de start/stop do serviço, isolando
detalhes do shell (subprocess) do resto da aplicação.
"""
from __future__ import annotations

import subprocess
import time
from pathlib import Path

from .config import CONFIG
from .logger import CigsLogger


class TomcatManager:
    """
    Gerencia o ciclo de vida do Tomcat.

    Attributes:
        bin_dir (Path): Diretório dos scripts .sh (…/tomcat/bin).
        logger (CigsLogger): Logger compartilhado.
    """

    def __init__(self, logger: CigsLogger, bin_dir: Path | None = None) -> None:
        """
        Args:
            logger: Logger compartilhado.
            bin_dir: Diretório dos scripts. Se None, usa CONFIG.tomcat_bin
                     (…/apache-tomcat-9.0.105/bin).
        """
        self.bin_dir = bin_dir or CONFIG.tomcat_bin
        self.logger = logger

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------
    def _executar(self, script: str) -> None:
        """
        Executa um script do Tomcat dentro de seu diretório.

        Args:
            script: Nome do script (ex: "startup.sh").
        """
        self.logger.info(f"Executando operacao {script} ...")
        subprocess.run(
            ["./" + script],
            cwd=str(self.bin_dir),
            check=False,
            capture_output=True,
            text=True,
        )

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def parar(self) -> None:
        """Para o serviço Tomcat e aguarda 10s (igual ao Bash)."""
        self.logger.info("Parando o servico Tomcat. Aguarde ....")
        self._executar("shutdown.sh")
        time.sleep(10)
        self.logger.ok("Tomcat parado. - Operacao executada.")

    def iniciar(self) -> None:
        """Inicia o serviço Tomcat."""
        self.logger.info("Iniciando o servico Tomcat. Aguarde...")
        self._executar("startup.sh")
        self.logger.ok("Tomcat iniciado. - Operacao executada.")