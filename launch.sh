#!/bin/bash

set -e

if [ "$#" -ne 2 ]; then
    echo -e "\033[31musage: ./launch.sh <user_to_track> <logged|delogged>\033[0m"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$(uname)" = "Linux" ]; then
    REQ="requirements_linux.txt"
elif [ "$(uname)" = "Darwin" ]; then
    REQ="requirements_macos.txt"
else
    echo "Unsupported OS."
    exit 1
fi

VENV="$HOME/myvenv"
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
pip install --upgrade pip -q
pip install -r "$SCRIPT_DIR/$REQ" -q

python3 "$SCRIPT_DIR/tracker.py" "$1" "$2"
