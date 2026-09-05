# Codificador Educativo de Instrucciones RISC-V (RV32I)

Herramienta de codificación y análisis visual de instrucciones del subconjunto RISC-V RV32I 
para el curso CE4301 Arquitectura de Computadores I (TEC, 2026-II).

---

## 1. Requisitos y Preparación del Entorno

La herramienta está desarrollada en **Python 3** y utiliza únicamente módulos de la biblioteca estándar (`sys`). No requiere la instalación de librerías externas ni dependencias vía `pip`.

### Requisitos mínimos:
- **Python 3.8** o superior instalado en el sistema.
- Intérprete accesible mediante el comando `python3`.
- Shell compatible con Bash para la ejecución de `run.sh`.

---

## 2. Modo de Operación (Punto de Entrada Obligatorio)

El punto de entrada del proyecto es el script ejecutable `run.sh`, el cual recibe **una única instrucción** como argumento entre comillas:

```bash
./run.sh "<instruccion>"
```

### Ejemplos de uso:

```bash
./run.sh "add x5, x6, x7"
./run.sh "addi x10, x1, -12"
./run.sh "lw x5, 8(x6)"
./run.sh "sw x8, -4(x2)"
./run.sh "beq x1, x2, 8"
```

### Formato de salida:
El programa imprime:
1. Una tabla visual en formato ASCII con el desglose de los campos (bits, valores y significado).
2. La línea estandarizada para verificación automática: `HEX: 0xXXXXXXXX`.

---

## 3. Comprobación y Autoevaluación

Para verificar el funcionamiento de la herramienta contra la suite de 36 instrucciones de prueba provistas en `vectores_ejemplo.txt`:

```bash
python3 test_vectores.py
```

---

## 4. Validación Cruzada con Toolchain Oficial de RISC-V (GNU)

Para verificar y contrastar los 36 casos contra el ensamblador y desensamblador oficial de GNU (`as` / `objdump`):

### Instalación del toolchain:
* **En Arch Linux / CachyOS:**
  ```bash
  sudo pacman -S riscv64-elf-binutils
  ```
* **En Ubuntu / Debian:**
  ```bash
  sudo apt update && sudo apt install binutils-riscv64-unknown-elf
  ```

### Ejecución de la validación:
```bash
./validar_objdump.sh
```
El script compila `pruebas_36.s` y genera el desensamblado con `objdump -d` para comparar la codificación binaria de cada instrucción.
