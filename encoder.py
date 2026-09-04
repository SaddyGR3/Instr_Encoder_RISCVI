#!/usr/bin/env python3
"""
Implementación del codificador de instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

El programa recibe una instrucción en lenguaje ensamblador y la codifica en su representación binaria.
Después, imprime una explicación detallada en formato ASCII de cada campo de la instrucción codificada.
Que incluye el formato de la instrucción, los valores de cada campo, y su significado.

Tambien da la representacion hexa de la instruccion codificada, que es la salida final.

se ejecuta con el run.sh.   ./run.sh "<instruccion>"
ejemplo: ./run.sh "add x5, x6, x7"
"""
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",  # instrucciones soportadas por el codificador.
              "lw", "lb", "sw", "sb", "beq", "bne"]


def parse_register(reg: str) -> int:
    """
    Recibe un registro como string, ejemplo: "x5"
    y lo retorna como entero. Ademas haciendo verificaciones como
    que se encuentre en rango valido de registro(0 <= valor < 32).
    """
    reg = reg.strip().lower()
    if not reg.startswith("x"):
        raise ValueError(f"Registro inválido: {reg}")
    try:
        reg_num = int(reg[1:])  # 'x7'[1:] toma solo '7'
    except ValueError:
        raise ValueError(f"Registro inválido: {reg}")
    if not (0 <= reg_num <= 31):
        raise ValueError(f"Registro fuera de rango(0-31): {reg}")
    return reg_num


def parse_immediate(imm: str) -> int:
    """
    Recibe un inmediato como string, ejemplo: "100", "-12", "0x10"
    y lo retorna como entero. Puede ser negativo.
    Python permite convertir strings a enteros con cualquier base usando int(string, base),
    donde base=0 permite detectar automaticamente la base (decimal, hexadecimal, octal).
    """
    try:
        return int(imm.strip(), 0)
    except ValueError:
        raise ValueError(f"Inmediato inválido: {imm}")


def encode_instruction(instruction: str) -> int:
    """
    Funcion principal que recibe la instruccion en lenguaje ensamblador.
    Primero tokeniza la instruccion eliminando comas, parentesis y espacios y luego usa split
    para hacer una lista con los tokens.
    Luego define el nemonico como el primer elemento de esa lista y lo pasa a minuscula para estandarizar.
    Por ultimo verifica que es el nemonico y llama a la funcion correspondiente para codificar la instruccion.
    """
    # 1. Limpieza y tokenizacion
    tokens = instruction.replace(",", " ").replace("(", " ").replace(")", " ").split()
    if not tokens:
        raise ValueError("Instrucción vacía")

    mnemonic = tokens[0].lower()

    if mnemonic not in SOPORTADAS:
        raise ValueError(f"Instrucción no soportada: {mnemonic}")

    # TODO: Despachar a los codificadores de bits en el siguiente commit
    raise NotImplementedError(f"Codificador de bits pendiente para: {mnemonic}")


def explain_instruction(instruction: str, word: int) -> str:
    # TODO: Generador visual de tabla pendiente
    return ""


def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
