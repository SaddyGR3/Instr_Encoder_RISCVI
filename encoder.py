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


R_INSTRUCTIONS = {
    # mnemonico: (funct3, funct7)
    "add": (0x0, 0x00),
    "sub": (0x0, 0x20),
    "and": (0x7, 0x00),
    "or":  (0x6, 0x00),
}


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


"""
Codificadores de instrucciones RISC-V

Cada funcion encode usa la misma logica; para acomodar los datos en 32 bits se utiliza:
<< que es un operador de desplazamiento izq y | que es un operador OR a nivel de bits.

En python los enteros tienen infinitos ceros a la izq.
por lo que al tomar un valor como por ejemplo rs2 y desplazarlo 20 bits a la izq, 
se obtiene un valor  rs2 << 20 : ...0000000 [00110] 00000 000 00000 0000000
con infinitos ceros a la izquierda y 20 ceros a la derecha.
Al hacer OR con los distintos valores desplazados, los 1 de cada uno de los valores, funct7,rs2,rs1, funct3, rd y opcode
se acomodan en la posicion correcta de los 32 bits de la instruccion final.

Con respecto a los inmediatos, se hace un AND con 0xFFF para asegurarse de que solo se tomen los 12 bits menos significativos.
asegurando que a partir del bit 12 hacia la izquierda sean cero.
"""


def encode_r(funct7, rs2, rs1, funct3, rd, opcode):
    word = (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    return word


def encode_i(imm, rs1, funct3, rd, opcode):
    imm_12 = imm & 0xFFF  # Garantiza exactamente 12 bits (positivo o negativo)
    word = (imm_12 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
    return word


def encode_s(imm, rs2, rs1, funct3, opcode):
    imm_12 = imm & 0xFFF
    imm_4_0 = imm_12 & 0x1F
    imm_11_5 = (imm_12 >> 5) & 0x7F
    
    word = (imm_11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm_4_0 << 7) | opcode
    return word


def encode_b(imm, rs2, rs1, funct3, opcode):
    imm_13 = imm & 0x1FFF
    
    imm_12   = (imm_13 >> 12) & 0x1
    imm_11   = (imm_13 >> 11) & 0x1
    imm_10_5 = (imm_13 >> 5)  & 0x3F
    imm_4_1  = (imm_13 >> 1)  & 0xF

    word = (
        (imm_12   << 31) |
        (imm_10_5 << 25) |
        (rs2      << 20) |
        (rs1      << 15) |
        (funct3   << 12) |
        (imm_4_1  << 8)  |
        (imm_11   << 7)  |
        opcode
    )
    return word


def encode_instruction(instruction: str) -> int:
    """
    Funcion principal que recibe la instruccion en lenguaje ensamblador
    Primero tokeniza la instruccion eliminando comas,parentesis y espacios y luego usa split para hacer una lista con los tokens.
    Luego define el nemonico como el primer elemento de esa lista y lo pasa a minuscula para estandarizar.
    Por ultimo verifica que es el nemonico y llama a la funcion correspondiente para codificar la instruccion.
    """
    # 1.Limpieza y tokenizacion
    tokens = instruction.replace(",", " ").replace("(", " ").replace(")", " ").split()
    if not tokens:
        raise ValueError("Instrucción vacía")

    mnemonic = tokens[0].lower()

    # 2.Verificación del nemonico

    # add, sub, and, or son instrucciones de tipo R
    # Eso implica que siempre siguen el mismo formato: nemonico rd, rs1, rs2
    if mnemonic in ["add", "sub", "and", "or"]:
        rd = parse_register(tokens[1])
        rs1 = parse_register(tokens[2])
        rs2 = parse_register(tokens[3])
        funct3, funct7 = R_INSTRUCTIONS[mnemonic]
        return encode_r(funct7, rs2, rs1, funct3, rd, 0x33)

    # addi y andi son instrucciones de tipo I
    # Siguen el formato: nemonico rd, rs1, imm
    elif mnemonic in ["addi", "andi"]:
        rd = parse_register(tokens[1])
        rs1 = parse_register(tokens[2])
        imm = parse_immediate(tokens[3])
        funct3 = 0x0 if mnemonic == "addi" else 0x7
        return encode_i(imm, rs1, funct3, rd, 0x13)

    # lw y lb son instrucciones de tipo I de carga desde memoria
    # Siguen el formato: nemonico rd, imm(rs1)
    elif mnemonic in ["lw", "lb"]:
        rd = parse_register(tokens[1])
        imm = parse_immediate(tokens[2])
        rs1 = parse_register(tokens[3])
        funct3 = 0x2 if mnemonic == "lw" else 0x0
        return encode_i(imm, rs1, funct3, rd, 0x03)

    # sw y sb son instrucciones de tipo S de almacenamiento en memoria
    # Siguen el formato: nemonico rs2, imm(rs1)
    elif mnemonic in ["sw", "sb"]:
        rs2 = parse_register(tokens[1])
        imm = parse_immediate(tokens[2])
        rs1 = parse_register(tokens[3])
        funct3 = 0x2 if mnemonic == "sw" else 0x0
        return encode_s(imm, rs2, rs1, funct3, 0x23)
    
    # beq y bne son instrucciones de tipo B de salto condicional
    # Siguen el formato: nemonico rs1, rs2, imm
    elif mnemonic in ["beq", "bne"]:
        rs1 = parse_register(tokens[1])
        rs2 = parse_register(tokens[2])
        imm = parse_immediate(tokens[3])
        funct3 = 0x0 if mnemonic == "beq" else 0x1
        return encode_b(imm, rs2, rs1, funct3, 0x63)

    # error si el nemonico no pertenece a las 12 instrucciones soportadas
    else:
        raise ValueError(f"Instrucción no soportada: {mnemonic}")


def explain_instruction(instruction: str, word: int) -> str:
    """
    Retorna la representación visual y la explicacion de cada campo de la instruccion.
    """
    tokens = instruction.replace(",", " ").replace("(", " ").replace(")", " ").split()
    mnemonic = tokens[0].lower()

    hex_str = f"0x{word:08X}"

    lines = []
    lines.append("=" * 80)
    lines.append(f"Instrucción : {instruction.strip()}")

    # -----------------------------------------------------------------------
    # 1. Formato R
    # -----------------------------------------------------------------------
    if mnemonic in ["add", "sub", "and", "or"]:
        rd = parse_register(tokens[1])
        rs1 = parse_register(tokens[2])
        rs2 = parse_register(tokens[3])
        funct3, funct7 = R_INSTRUCTIONS[mnemonic]
        opcode = 0x33

        f7_bin = f"{funct7:07b}"
        rs2_bin = f"{rs2:05b}"
        rs1_bin = f"{rs1:05b}"
        f3_bin = f"{funct3:03b}"
        rd_bin = f"{rd:05b}"
        op_bin = f"{opcode:07b}"

        lines.append("Formato     : Tipo R (Aritmética registro-registro)")
        lines.append(f"Codificación: {hex_str}")
        lines.append(f"Binario (32): {f7_bin} {rs2_bin} {rs1_bin} {f3_bin} {rd_bin} {op_bin}")
        lines.append("=" * 80)
        lines.append("Desglose de campos:")
        lines.append("+-------------+----------+----------+----------+----------+----------+----------+")
        lines.append("| Campo       | funct7   | rs2      | rs1      | funct3   | rd       | opcode   |")
        lines.append("| Bits        | [31:25]  | [24:20]  | [19:15]  | [14:12]  | [11:7]   | [6:0]    |")
        lines.append(f"| Binario     | {f7_bin:<8} | {rs2_bin:<8} | {rs1_bin:<8} | {f3_bin:<8} | {rd_bin:<8} | {op_bin:<8} |")
        lines.append(f"| Valor       | 0x{funct7:02X}     | {rs2:<2} (x{rs2:<2}) | {rs1:<2} (x{rs1:<2}) | 0x{funct3:X}      | {rd:<2} (x{rd:<2}) | 0x{opcode:02X}     |")
        lines.append("+-------------+----------+----------+----------+----------+----------+----------+")

        op_desc = {"add": "Suma (ADD)", "sub": "Resta (SUB)", "and": "AND lógico", "or": "OR lógico"}[mnemonic]
        lines.append("Explicación de campos:")
        lines.append(f"- opcode (0b{op_bin} / 0x{opcode:02X}): Operación aritmética entre registros RV32I.")
        lines.append(f"- rd (x{rd}): Registro destino donde se almacenará el resultado.")
        lines.append(f"- funct3 (0b{f3_bin}): Código de función de 3 bits para la familia {mnemonic.upper()}.")
        lines.append(f"- rs1 (x{rs1}): Primer registro fuente (primer operando).")
        lines.append(f"- rs2 (x{rs2}): Segundo registro fuente (segundo operando).")
        lines.append(f"- funct7 (0b{f7_bin}): Código de 7 bits que especifica la operación {op_desc}.")

    # -----------------------------------------------------------------------
    # 2. Formato I
    # -----------------------------------------------------------------------
    elif mnemonic in ["addi", "andi", "lw", "lb"]:
        if mnemonic in ["addi", "andi"]:
            rd = parse_register(tokens[1])
            rs1 = parse_register(tokens[2])
            imm = parse_immediate(tokens[3])
            opcode = 0x13
            funct3 = 0x0 if mnemonic == "addi" else 0x7
            subtipo = "Aritmética con inmediato"
        else:
            rd = parse_register(tokens[1])
            imm = parse_immediate(tokens[2])
            rs1 = parse_register(tokens[3])
            opcode = 0x03
            funct3 = 0x2 if mnemonic == "lw" else 0x0
            subtipo = "Carga desde memoria (Load)"

        imm_12 = imm & 0xFFF
        imm_bin = f"{imm_12:012b}"
        rs1_bin = f"{rs1:05b}"
        f3_bin = f"{funct3:03b}"
        rd_bin = f"{rd:05b}"
        op_bin = f"{opcode:07b}"

        lines.append(f"Formato     : Tipo I ({subtipo})")
        lines.append(f"Codificación: {hex_str}")
        lines.append(f"Binario (32): {imm_bin} {rs1_bin} {f3_bin} {rd_bin} {op_bin}")
        lines.append("=" * 80)
        lines.append("Desglose de campos:")
        lines.append("+-------------+--------------+----------+----------+----------+----------+")
        lines.append("| Campo       | imm[11:0]    | rs1      | funct3   | rd       | opcode   |")
        lines.append("| Bits        | [31:20]      | [19:15]  | [14:12]  | [11:7]   | [6:0]    |")
        lines.append(f"| Binario     | {imm_bin:<12} | {rs1_bin:<8} | {f3_bin:<8} | {rd_bin:<8} | {op_bin:<8} |")
        lines.append(f"| Valor       | {imm:<12} | {rs1:<2} (x{rs1:<2}) | 0x{funct3:X}      | {rd:<2} (x{rd:<2}) | 0x{opcode:02X}     |")
        lines.append("+-------------+--------------+----------+----------+----------+----------+")

        lines.append("Explicación de campos:")
        lines.append(f"- opcode (0b{op_bin} / 0x{opcode:02X}): Identifica la categoría {subtipo}.")
        lines.append(f"- rd (x{rd}): Registro destino donde se guardará el resultado.")
        lines.append(f"- funct3 (0b{f3_bin}): Función que especifica la instrucción ({mnemonic.upper()}).")
        if mnemonic in ["addi", "andi"]:
            lines.append(f"- rs1 (x{rs1}): Registro fuente que aporta el valor base para la operación.")
            lines.append(f"- imm[11:0] ({imm}): Valor inmediato con signo de 12 bits.")
        else:
            lines.append(f"- rs1 (x{rs1}): Registro base que contiene la dirección de memoria.")
            lines.append(f"- imm[11:0] ({imm}): Desplazamiento (offset) con signo sumado a la dirección base.")

    # -----------------------------------------------------------------------
    # 3. Formato S
    # -----------------------------------------------------------------------
    elif mnemonic in ["sw", "sb"]:
        rs2 = parse_register(tokens[1])
        imm = parse_immediate(tokens[2])
        rs1 = parse_register(tokens[3])
        opcode = 0x23
        funct3 = 0x2 if mnemonic == "sw" else 0x0

        imm_12 = imm & 0xFFF
        imm_4_0 = imm_12 & 0x1F
        imm_11_5 = (imm_12 >> 5) & 0x7F

        imm_11_5_bin = f"{imm_11_5:07b}"
        rs2_bin = f"{rs2:05b}"
        rs1_bin = f"{rs1:05b}"
        f3_bin = f"{funct3:03b}"
        imm_4_0_bin = f"{imm_4_0:05b}"
        op_bin = f"{opcode:07b}"

        lines.append("Formato     : Tipo S (Almacenamiento en memoria)")
        lines.append(f"Codificación: {hex_str}")
        lines.append(f"Binario (32): {imm_11_5_bin} {rs2_bin} {rs1_bin} {f3_bin} {imm_4_0_bin} {op_bin}")
        lines.append("=" * 80)
        lines.append("Desglose de campos:")
        lines.append("+-------------+------------+----------+----------+----------+-----------+----------+")
        lines.append("| Campo       | imm[11:5]  | rs2      | rs1      | funct3   | imm[4:0]  | opcode   |")
        lines.append("| Bits        | [31:25]    | [24:20]  | [19:15]  | [14:12]  | [11:7]    | [6:0]    |")
        lines.append(f"| Binario     | {imm_11_5_bin:<10} | {rs2_bin:<8} | {rs1_bin:<8} | {f3_bin:<8} | {imm_4_0_bin:<9} | {op_bin:<8} |")
        lines.append(f"| Valor       | 0b{imm_11_5_bin:<8} | {rs2:<2} (x{rs2:<2}) | {rs1:<2} (x{rs1:<2}) | 0x{funct3:X}      | 0b{imm_4_0_bin:<7} | 0x{opcode:02X}     |")
        lines.append("+-------------+------------+----------+----------+----------+-----------+----------+")

        op_name = "SW (Store Word, 32 bits)" if mnemonic == "sw" else "SB (Store Byte, 8 bits)"
        lines.append("Explicación de campos:")
        lines.append(f"- opcode (0b{op_bin} / 0x{opcode:02X}): Instrucción de almacenamiento en memoria (Store).")
        lines.append(f"- imm (ensamblado): {imm} (offset de 12 bits dividido en imm[11:5] e imm[4:0]).")
        lines.append(f"- funct3 (0b{f3_bin}): Identifica la operación {op_name}.")
        lines.append(f"- rs1 (x{rs1}): Registro base que contiene la dirección base en memoria.")
        lines.append(f"- rs2 (x{rs2}): Registro fuente cuyo dato se escribirá en memoria.")

    # -----------------------------------------------------------------------
    # 4. Formato B
    # -----------------------------------------------------------------------
    elif mnemonic in ["beq", "bne"]:
        rs1 = parse_register(tokens[1])
        rs2 = parse_register(tokens[2])
        imm = parse_immediate(tokens[3])
        opcode = 0x63
        funct3 = 0x0 if mnemonic == "beq" else 0x1

        imm_13 = imm & 0x1FFF
        imm_12   = (imm_13 >> 12) & 0x1
        imm_11   = (imm_13 >> 11) & 0x1
        imm_10_5 = (imm_13 >> 5)  & 0x3F
        imm_4_1  = (imm_13 >> 1)  & 0xF

        upper_7 = (imm_12 << 6) | imm_10_5
        lower_5 = (imm_4_1 << 1) | imm_11

        upper_7_bin = f"{upper_7:07b}"
        rs2_bin = f"{rs2:05b}"
        rs1_bin = f"{rs1:05b}"
        f3_bin = f"{funct3:03b}"
        lower_5_bin = f"{lower_5:05b}"
        op_bin = f"{opcode:07b}"

        lines.append("Formato     : Tipo B (Salto condicional)")
        lines.append(f"Codificación: {hex_str}")
        lines.append(f"Binario (32): {upper_7_bin} {rs2_bin} {rs1_bin} {f3_bin} {lower_5_bin} {op_bin}")
        lines.append("=" * 80)
        lines.append("Desglose de campos:")
        lines.append("+-------------+---------------+----------+----------+----------+---------------+----------+")
        lines.append("| Campo       | imm[12|10:5]  | rs2      | rs1      | funct3   | imm[4:1|11]   | opcode   |")
        lines.append("| Bits        | [31:25]       | [24:20]  | [19:15]  | [14:12]  | [11:7]        | [6:0]    |")
        lines.append(f"| Binario     | {upper_7_bin:<13} | {rs2_bin:<8} | {rs1_bin:<8} | {f3_bin:<8} | {lower_5_bin:<13} | {op_bin:<8} |")
        lines.append(f"| Valor       | 0b{upper_7_bin:<11} | {rs2:<2} (x{rs2:<2}) | {rs1:<2} (x{rs1:<2}) | 0x{funct3:X}      | 0b{lower_5_bin:<11} | 0x{opcode:02X}     |")
        lines.append("+-------------+---------------+----------+----------+----------+---------------+----------+")

        cond_desc = "si rs1 == rs2" if mnemonic == "beq" else "si rs1 != rs2"
        lines.append("Explicación de campos:")
        lines.append(f"- opcode (0b{op_bin} / 0x{opcode:02X}): Instrucción de salto condicional (Branch).")
        lines.append(f"- imm (ensamblado): {imm} bytes (offset relativo al PC de 13 bits con signo, imm[0]=0 implícito).")
        lines.append(f"- funct3 (0b{f3_bin}): Condición de salto {mnemonic.upper()} ({cond_desc}).")
        lines.append(f"- rs1 (x{rs1}): Primer registro a comparar.")
        lines.append(f"- rs2 (x{rs2}): Segundo registro a comparar.")

    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print(f'Uso: {sys.argv[0]} "<instruccion>"', file=sys.stderr)
        print(f'Ejemplo: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]
    word = encode_instruction(instruction) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")


if __name__ == "__main__":
    main()
