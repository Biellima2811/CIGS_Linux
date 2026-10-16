"""
Módulo de Atualização de WARs.

Responsabilidade: substituir TODOS os WARs de clientes pelo
WAR-base presente em /home/fortes/CIGS/atualizados/fortesrh.war.
"""

from __future__ import annotations
import shutil
from pathlib import Path

from .config import CONFIG
from .logger import CigsLogger

class WarUpdater:
    """
    Distribui o WAR-base para todos os clientes.

    Attributes:
        webapps (Path): Diretório webapps do Tomcat.
        logger (CigsLogger): Logger compartilhado.
    """

    # Construtor
    def __init__(self, logger: CigsLogger, webapps: Path | None = None):
        self.webapps = webapps or CONFIG.tomcat_webapps
        self.logger = logger

    # ------------------------------------------------------------------
    # Descoberta de clientes
    # ------------------------------------------------------------------

    def _listar_clientes(self) -> list[str]:
        """Retorna lista de arquivos do tipo fortesrh*.war."""
        padrao = f"{CONFIG.PREFIXO_CLIENTES}*.war"
        return [p.name for p in self.webapps.glob(padrao)]

    def _limpar_ambiente(self) -> None:
        """Remove arquivos antigos fortesrh* (WARs e diretórios explodidos)."""
        self.logger.info("Limpando ambiente (Removendo arquivos antigos)...")
        for item in self.webapps.glob(f"{CONFIG.PREFIXO_CLIENTES}*"):
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def atualizar(self) -> int:
        """
        Executa a atualização completa.

        Returns:
            Quantidade de clientes atualizados.

        Raises:
            FileNotFoundError: Se o WAR-base não existir.
            RuntimeError: Se nenhum cliente for encontrado.
        """
        arquivo_base = CONFIG.arquivo_base

        self.logger.info("Verificando arquivo base disponibilizado...")
        if not arquivo_base.is_file():
            raise FileNotFoundError(f"Arquivo {arquivo_base} nao encontrado!")

        self.logger.info("Mapeando clientes em webapps...")
        clientes = self._listar_clientes()
        if not clientes:
            raise RuntimeError("Nenhum cliente encontrado no webapps.")

        self._limpar_ambiente()

        self.logger.info("Realizando a distribuição dos novos arquivos: ")
        for cliente in clientes:
            destino = self.webapps / cliente
            shutil.copy2(arquivo_base, destino)
            self.logger.info(f" -> Atualizando: {cliente}")

        self.logger.raw("------------------------------------------")
        self.logger.ok("Operacao de copia finalizada.")
        self.logger.raw(f" -> TOTAL DE CLIENTES ATUALIZADOS: {len(clientes)}")
        self.logger.raw("------------------------------------------")
        return len(clientes)