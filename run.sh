#!/usr/bin/env bash
# Punto de entrada fijo requerido por la especificación.
# Uso: ./run.sh "<instruccion>"
# Ejemplo: ./run.sh "add x5, x6, x7"
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo 'Uso: ./run.sh "<instruccion>"' >&2
    echo 'Ejemplo: ./run.sh "add x5, x6, x7"' >&2
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/encoder.py" "$1"
