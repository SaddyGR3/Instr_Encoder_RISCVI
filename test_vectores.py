#!/usr/bin/env python3
"""
Script de verificacion contra vectores_ejemplo.txt
"""
import sys
from encoder import encode_instruction


def run_tests(filepath="vectores_ejemplo.txt"):
    total = 0
    passed = 0
    failed = 0

    print(f"=== Ejecutando pruebas desde {filepath} ===\n")

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            # Ignorar líneas vacías y comentarios
            if not line or line.startswith("#"):
                continue

            if ";" not in line:
                continue

            inst_str, expected_hex = [part.strip() for part in line.split(";")]
            expected_val = int(expected_hex, 16)

            total += 1
            try:
                word = encode_instruction(inst_str) & 0xFFFFFFFF
                actual_hex = f"0x{word:08x}"

                if word == expected_val:
                    passed += 1
                    print(f" [PASS] {inst_str:<25} -> {actual_hex}")
                else:
                    failed += 1
                    print(f" [FAIL] {inst_str:<25} -> Obtenido: {actual_hex}, Esperado: {expected_hex}")
            except Exception as e:
                failed += 1
                print(f" [ERROR] {inst_str:<25} -> Excepción: {e}")

    print("\n" + "=" * 50)
    print(f"Resultado final: {passed}/{total} pruebas superadas.")
    if failed == 0:
        print(" ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print(f" {failed} pruebas fallaron.")
    print("=" * 50)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
