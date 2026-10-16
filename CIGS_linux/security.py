"""
Módulo de Segurança (Desafio-Resposta).

Mantém a MESMA lógica do Bash original:
    esperado = desafio * 1337 + 9842

A única mudança de comportamento é arquitetural: esta função é
chamada UMA VEZ ao iniciar o programa. Depois disso, o menu roda
em loop e o usuário não precisa digitar a chave novamente.
"""
from __future__ import annotations

import random
import sys
import time

# Constantes "ofuscadas" (equivalentes aos _R1/_R2 do Bash)
_k = 1337
_OFFSET = 9842

class SecurityGuard:
    """
    Valida o acesso do operador via desafio-resposta.

    Attributes:
        min_desafio (int): Menor número de desafio possível.
        max_desafio (int): Maior número de desafio possível.
    """

    def __init__(self, min_desafio: int = 1, max_desafio: int = 32767) -> None:
        self.min_desafio = min_desafio
        self.max_desafio = max_desafio

    # ------------------------------------------------------------------
    # Cálculo
    # ------------------------------------------------------------------
    def _calcular_esperado(self, desafio: int) -> int:
        """Aplica a fórmula do Bash: D * K + OFFSET."""
        return desafio * _k + _OFFSET

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def autenticar(self) -> None:
        """
        Solicita a chave do operador.

        Em caso de sucesso retorna silenciosamente; em caso de falha
        encerra o programa com código 1 (mesmo comportamento do Bash).
        """
        desafio = random.randint(self.min_desafio, self.max_desafio)

        print("\033[31m==========================================================")
        print("               ACESSO RESTRITO - SISTEMA CIGS")
        print("==========================================================")
        print()
        print("    ATENCAO: Sistema bloqueado por seguranca.")
        print("    Informe o codigo abaixo ao Administrador.")
        print()
        print(f"    CODIGO DE DESAFIO: [ {desafio} ]\033[0m")
        print()

        tentativa = input("     Digite a Chave de Atenticacao: ").strip()

        esperado = self._calcular_esperado(desafio)

        if tentativa == str(esperado):
            print("\n\033[32m    [  OK  ] Chave Valida! Acesso Concedido.\033[0m")
            time.sleep(1)
        else:
            print("\n\033[31m    [ ERRO ] Chave Invalida! Acesso Negado.\033[0m")
            time.sleep(2)
            sys.exit(1)