"""
Interface de linha de comando (CLI) do CIGS.

Responsabilidade: apresentar o menu e traduzir a escolha do
operador em chamadas aos módulos de negócio.
"""
from __future__ import annotations

from .logger import CigsLogger
from .scheduler import AtScheduler
from .tomcat import TomcatManager
from .updater import WarUpdater


class MenuCLI:
    """
    Menu interativo em loop.

    Diferença arquitetural em relação ao Bash: o loop `while True`
    mantém o programa vivo após cada operação. O operador só sai
    ao escolher a opção 6 — e só então um novo login é exigido.

    Nota importante: tratamos a entrada SEMPRE como string. Converter
    para int antes do try/except fazia o ValueError escapar do bloco
    de tratamento e, pior, tornava as comparações `== "1"` sempre
    falsas.
    """

    # ------------------------------------------------------------------
    # Construtor
    # ------------------------------------------------------------------
    def __init__(
        self,
        tomcat: TomcatManager,
        updater: WarUpdater,
        scheduler: AtScheduler,
        logger: CigsLogger,
    ) -> None:
        """
        Args:
            tomcat: Gerenciador do Tomcat (start/stop).
            updater: Distribuidor de WARs.
            scheduler: Agendador via `at`.
            logger: Logger compartilhado.
        """
        self.tomcat = tomcat
        self.updater = updater
        self.scheduler = scheduler
        self.logger = logger

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _render_banner(self) -> None:
        """Imprime o banner do menu principal."""
        print("===================================================")
        print("      C.I.G.S - CENTRAL DE OPERACOES LINUX")
        print("===================================================")
        print("1 - [MANUAL]    Apenas PARAR o Tomcat")
        print("2 - [MANUAL]    Apenas ATUALIZAR arquivos (Tomcat deve esta parado)")
        print("3 - [MANUAL]    Apenas INICIAR o Tomcat")
        print("4 - [AGENDADOR] Programar Missao Automatica")
        print("5 - [AGENDADOR] Listar agendamentos pendentes")
        print("6 - Sair")
        print("===================================================")

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------
    def _acao_agendar(self) -> None:
        """Solicita o horário e delega o agendamento ao AtScheduler."""
        hora = input("Digite o horario de execucao (Ex: 18:00): ").strip()

        if not hora:
            print(
                "[AVISO] - Horario vazio ou fora de parametro. "
                "Cancelando operacao."
            )
            return

        self.scheduler.agendar(hora)
        print(
            "Agendamento efetuado! - Encerramento do programa pode ser "
            "realizado. A missao ocorrera de forma automatica!"
        )

    def _acao_listar(self) -> None:
        """Lista os agendamentos pendentes na fila do `atq`."""
        print(20 * "=")
        print("Agendamentos pendentes na fila de execucao:")
        print(self.scheduler.listar())

    # ------------------------------------------------------------------
    # Loop principal
    # ------------------------------------------------------------------
    def executar(self) -> None:
        """
        Roda o menu até o usuário escolher sair (opção 6).

        Mantemos a entrada como STRING (sem converter para int):
        - input() sempre devolve str;
        - evita ValueError fora do try;
        - permite comparações diretas com "1", "2", etc.
        """
        while True:
            self._render_banner()
            opcao = input("Escolha a opcao (1 a 6): ").strip()

            try:
                if opcao == "1":
                    self.tomcat.parar()
                elif opcao == "2":
                    self.updater.atualizar()
                elif opcao == "3":
                    self.tomcat.iniciar()
                elif opcao == "4":
                    self._acao_agendar()
                elif opcao == "5":
                    self._acao_listar()
                elif opcao == "6":
                    print("Encerrando CIGS...")
                    return
                else:
                    print("[AVISO] Opcao invalida.")
            except FileNotFoundError as exc:
                self.logger.error(str(exc))
            except RuntimeError as exc:
                self.logger.error(str(exc))
            except Exception as exc:  # noqa: BLE001
                self.logger.error(f"Erro inesperado: {exc}")

            input("\nPressione ENTER para voltar ao menu...")