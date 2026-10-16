"""
Módulo de configuração central.

Responsabilidade única: concentrar TODOS os caminhos e constantes
do sistema em um único ponto. Se o Tomcat mudar de versão, você
edita APENAS este arquivo.

Suporta override por variáveis de ambiente — útil para testes
locais (ex: no Windows) sem alterar os caminhos de produção:

    CIGS_BASE          -> raiz de trabalho
    CIGS_TOMCAT_HOME   -> raiz do Tomcat
    CIGS_EXECUTAVEL    -> caminho do binário usado pelo `at`
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


def _env_path(var: str, default: str) -> Path:
    """
    Lê uma variável de ambiente como Path ou usa o default.

    Args:
        var: Nome da variável de ambiente.
        default: Valor padrão (string) caso a variável não exista.

    Returns:
        Path correspondente.
    """
    return Path(os.environ.get(var, default))


@dataclass(frozen=True)
class CigsConfig:
    """
    Configurações imutáveis do CIGS.

    Attributes:
        CIGS_BASE: Raiz de trabalho do CIGS.
        TOMCAT_HOME: Diretório raiz da instalação do Tomcat.
        EXECUTAVEL_PATH: Caminho do binário compilado no servidor
                         (usado pelo agendador `at`).
        PREFIXO_CLIENTES: Prefixo dos arquivos .war dos clientes.
        ARQUIVO_BASE_NOME: Nome do WAR que será distribuído.
    """

    # ------------------------------------------------------------------
    # Caminhos base — sobrescrevíveis por variáveis de ambiente
    # ------------------------------------------------------------------
    CIGS_BASE: Path = field(
        default_factory=lambda: _env_path("CIGS_BASE", "/home/fortes/CIGS")
    )
    TOMCAT_HOME: Path = field(
        default_factory=lambda: _env_path(
            "CIGS_TOMCAT_HOME",
            "/home/fortes/RH/bin/ProgramasFortesRH/apache-tomcat-9.0.105",
        )
    )
    EXECUTAVEL_PATH: str = field(
        default_factory=lambda: os.environ.get(
            "CIGS_EXECUTAVEL", "/home/fortes/CIGS/cigs_master"
        )
    )

    # ------------------------------------------------------------------
    # Constantes de negócio
    # ------------------------------------------------------------------
    PREFIXO_CLIENTES: str = "fortesrh"
    ARQUIVO_BASE_NOME: str = "fortesrh.war"

    # ------------------------------------------------------------------
    # Propriedades derivadas (evitam caminhos "hard-coded" espalhados)
    # ------------------------------------------------------------------
    @property
    def tomcat_bin(self) -> Path:
        """Diretório dos scripts startup.sh / shutdown.sh."""
        return self.TOMCAT_HOME / "bin"

    @property
    def tomcat_webapps(self) -> Path:
        """Diretório de deploy das aplicações."""
        return self.TOMCAT_HOME / "webapps"

    @property
    def atualizados(self) -> Path:
        """Onde fica o WAR-base a ser distribuído."""
        return self.CIGS_BASE / "atualizados"

    @property
    def logs(self) -> Path:
        """Onde os logs serão gravados."""
        return self.CIGS_BASE / "logs"

    @property
    def arquivo_base(self) -> Path:
        """Caminho completo do WAR-base."""
        return self.atualizados / self.ARQUIVO_BASE_NOME

    def log_filename(self) -> Path:
        """Gera nome único de log usando timestamp."""
        ts = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        return self.logs / f"operacao_{ts}.log"


# Singleton — importado pelos outros módulos
CONFIG = CigsConfig()