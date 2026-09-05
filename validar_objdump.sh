#!/usr/bin/env bash
# Script para ensamblar pruebas_36.s y comparar contra objdump
set -euo pipefail

# Detectar el binario disponible en el sistema
if command -v riscv64-elf-as &>/dev/null; then
    AS="riscv64-elf-as"
    OBJDUMP="riscv64-elf-objdump"
elif command -v riscv64-unknown-elf-as &>/dev/null; then
    AS="riscv64-unknown-elf-as"
    OBJDUMP="riscv64-unknown-elf-objdump"
elif command -v riscv32-unknown-elf-as &>/dev/null; then
    AS="riscv32-unknown-elf-as"
    OBJDUMP="riscv32-unknown-elf-objdump"
else
    echo "ERROR: No se encontró el toolchain de RISC-V."
    echo "En CachyOS/Arch, instálelo con:"
    echo "  sudo pacman -S riscv64-elf-binutils"
    exit 1
fi

echo "=== 1. Ensamblando pruebas_36.s con $AS (RV32I) ==="
$AS -march=rv32i -mabi=ilp32 pruebas_36.s -o pruebas_36.o

echo "=== 2. Desensamblando con $OBJDUMP -d ==="
$OBJDUMP -d pruebas_36.o

echo ""
echo "=== El archivo objeto pruebas_36.o fue desensamblado correctamente ==="
