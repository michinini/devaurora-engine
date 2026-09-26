# devaurora-engine (PRIVATE)

Motor de desofuscación Luraph v15 + herramientas del pipeline.

- `deobf/` — motor completo (deob.py). Uso:
  `cd devaurora-engine && python3 deobf/deob.py <script.lua> --detect`
  `python3 deobf/deob.py <script.lua> -o out.lua --timeout 90`
- `samples/` — ejemplos para probar el motor.
- `tools/make_nokey.py` — parcha un main desofuscado para quitar el key system.
- `tools/compact_deobf.py` — compacta (quita indentación) manteniendo el código intacto.
- `tools/make_hop_nokey.py` — variante nokey del HopScript.
- `tools/batch_deobf.sh` — runner por lotes (ajustar rutas absolutas al usar).
- `tools/build_luau_ast.sh` — compila luau-ast para validar sintaxis.

NO compartir este repo: contiene el motor con el que se desofuscan los scripts.
