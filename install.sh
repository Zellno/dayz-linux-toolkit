#!/bin/bash
set -e

PROJECT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")" &&
    pwd
)"

COMMAND="$HOME/.local/bin/dayz-join"
CONFIG="$HOME/.config/dayz-linux-toolkit/servers"
LOGS="$HOME/.local/state/dayz-linux-toolkit/logs"

command -v python3 >/dev/null 2>&1 || {
    echo "ERRO: Python 3 não encontrado."
    exit 1
}

command -v steam >/dev/null 2>&1 || {
    echo "ERRO: comando steam não encontrado."
    exit 1
}

mkdir -p     "$HOME/.local/bin"     "$CONFIG"     "$LOGS"

chmod +x "$PROJECT_DIR/dayz_join.py"

ln -sfn     "$PROJECT_DIR/dayz_join.py"     "$COMMAND"

echo "Zellno DayZ Linux Toolkit instalado."
echo "Comando: $COMMAND"
echo
echo "Para entrar no Zellno:"
echo "  dayz-join zellno"
