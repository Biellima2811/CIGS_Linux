"""
Orquestrador da aplicação.

Une todas as peças: cria logger, valida segurança, executa o
menu OU a missão automática (flag --auto).
"""
from __future__ import annotations

import sys

from .config import CONFIG
from .logger import CigsLogger
from .menu import MenuCLI
from .scheduler import AtScheduler
from .security import SecurityGuard
from .tomcat import TomcatManager
from .updater import WarUpdater


class CigsApplication:
    """Aplicação principal do CIGS."""

    def __init__(self, modo_auto: bool = False) -> None:
        self.modo_auto = modo_auto
        self._preparar_diretorios()
        self.logger = CigsLogger(CONFIG.log_filename())
        self.tomcat = TomcatManager(self.logger)
        self.updater = WarUpdater(self.logger)
        self.scheduler = AtScheduler(self.logger)

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def _preparar_diretorios(self) -> None:
        """Garante que as pastas de trabalho existam."""
        CONFIG.atualizados.mkdir(parents=True, exist_ok=True)
        CONFIG.logs.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Missão automática (executada pelo `at --auto`)
    # ------------------------------------------------------------------
    def executar_missao_completa(self) -> None:
        """Sequência: parar → atualizar → iniciar."""
        self.logger.raw("==========================================")
        self.logger.raw(" INICIANDO MISSAO TATICA")
        self.logger.raw("==========================================")

        self.tomcat.parar()
        try:
            self.updater.atualizar()
        except Exception as exc:  # noqa: BLE001
            self.logger.error(f"Falha na atualizacao: {exc}")
            self.tomcat.iniciar()  # garante Tomcat de volta no ar
            return
        self.tomcat.iniciar()

        self.logger.raw("==========================================")
        self.logger.raw(" MISSAO CONCLUIDA COM SUCESSO!")
        self.logger.raw("==========================================")

    # ------------------------------------------------------------------
    # Modo interativo
    # ------------------------------------------------------------------
    def executar_interativo(self) -> None:
        """Fluxo padrão: segurança → menu em loop."""
        SecurityGuard().autenticar()
        menu = MenuCLI(self.tomcat, self.updater, self.scheduler, self.logger)
        menu.executar()

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------
    def run(self) -> int:
        """Despacha para o modo correto conforme a flag --auto."""
        if self.modo_auto:
            self.executar_missao_completa()
        else:
            self.executar_interativo()
        return 0