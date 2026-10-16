#!/usr/bin/env bash
# =====================================================================
# build.sh — Compila o CIGS para binário Linux (rodar no WSL/Ubuntu)
# =====================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/4] Criando ambiente virtual..."
python3 -m venv .venv
source .venv/bin/activate

echo "[2/4] Atualizando pip e instalando PyInstaller..."
pip install --upgrade pip
pip install pyinstaller

echo "[3/4] Compilando binario com PyInstaller..."
pyinstaller \
    --onefile \
    --name cigs_master \
    --strip \
    --console \
    --paths . \
    main.py

echo "[4/4] Concluido."
echo "  -> Binario: $SCRIPT_DIR/dist/cigs_master"
echo "  -> Envie para: /home/fortes/CIGS/cigs_master (via WinSCP)"