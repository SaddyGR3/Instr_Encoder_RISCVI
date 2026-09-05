.text
.globl _start

_start:
    # --- 1. add ---
    add x1, x2, x3
    add x0, x5, x6
    add x31, x31, x31

    # --- 2. sub ---
    sub x10, x11, x12
    sub x5, x0, x7
    sub x31, x30, x0

    # --- 3. and ---
    and x5, x6, x7
    and x8, x0, x9
    and x31, x31, x0

    # --- 4. or ---
    or x1, x2, x3
    or x4, x5, x0
    or x31, x1, x30

    # --- 5. addi ---
    addi x1, x2, 100
    addi x5, x6, -50
    addi x31, x0, 2047

    # --- 6. andi ---
    andi x10, x11, 255
    andi x12, x13, -1
    andi x31, x0, -2048

    # --- 7. lw ---
    lw x5, 16(x6)
    lw x7, -32(x8)
    lw x31, 2047(x0)

    # --- 8. lb ---
    lb x1, 4(x2)
    lb x3, -8(x4)
    lb x0, 0(x0)

    # --- 9. sw ---
    sw x5, 12(x6)
    sw x7, -24(x8)
    sw x31, -2048(x0)

    # --- 10. sb ---
    sb x1, 2(x2)
    sb x3, -10(x4)
    sb x0, 0(x31)

    # --- 11. beq ---
    beq x1, x2, .+16
    beq x3, x4, .-32
    beq x0, x0, .+0

    # --- 12. bne ---
    bne x5, x6, .+8
    bne x7, x8, .-16
    bne x31, x0, .-4096
