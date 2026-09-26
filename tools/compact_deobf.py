#!/usr/bin/env python3
"""Compactador de scripts deobfuscados (16MB -> ~2MB).

El output del devirtualizador escribe una sentencia por línea con indentación
por tabuladores (anidamiento profundo = hasta ~87% del tamaño en tabs).
Esta pasada quita SOLO el espacio inicial y las líneas vacías:

- No toca el contenido de ninguna línea (strings, comentarios inline, código).
- Seguro porque: no hay strings multilínea (sin [[..]]), no hay comentarios de
  bloque, cada string está en una sola línea con escapes.

Uso: python3 compact_deobf.py <in.lua> <out.lua> [...]
"""
import sys


def compact(src, dst):
    with open(src, encoding="utf-8") as f:
        lines = f.read().split("\n")
    out = []
    for ln in lines:
        stripped = ln.lstrip(" \t")
        if not stripped:
            continue                      # línea vacía: solo layout
        # solo se elimina espacio inicial (tabs/espacios), el contenido no se toca
        out.append(stripped)
    text = "\n".join(out) + "\n"
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return len(lines), len(out), len(text.encode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) < 3 or (len(sys.argv) - 1) % 2:
        sys.exit("uso: compact_deobf.py <in.lua> <out.lua> [<in2> <out2> ...]")
    for i in range(1, len(sys.argv), 2):
        src, dst = sys.argv[i], sys.argv[i + 1]
        n_in, n_out, b_out = compact(src, dst)
        b_in = sum(len(l.encode("utf-8")) + 1 for l in open(src, encoding="utf-8"))
        print(f"{dst}: {n_in} -> {n_out} líneas, {b_in/1e6:.2f} -> {b_out/1e6:.2f} MB "
              f"({100*b_out/b_in:.1f}%)")
