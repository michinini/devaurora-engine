#!/usr/bin/env python3
"""DevAurora Code — quita el license key system del HopScript deofuscado.

Parche quirúrgico (una sola línea):
  `v3.showInterface(<saved key>)` (línea 1496) — que crea la UI de "License key"
  y espera a que el usuario introduzca una key válida contra
  https://103.69.96.168 — se sustituye por una llamada directa al propio
  handler de éxito del script (v3.onLicenseKeyAccepted) con un details
  local. El script arranca por su propio camino PendingStart (fn se asigna
  más abajo y el final hace task.spawn(fn)), con el guard Started contra
  dobles arranques. subscriptionTier "Pro" desbloquea la etiqueta PREMIUM.
  El validador de protocolo (init/start/HMAC) queda definido pero jamás se
  llama: cero llamadas al servidor de licencias.
"""
import sys

SRC = "/home/z/my-project/engine/test/HopScript_deob.luau"
DST = "/home/z/my-project/download/HopScript_deobfuscated_nokey.lua"

with open(SRC, encoding="utf-8", newline="") as f:
    text = f.read()

ANCHOR = 'v3.showInterface(type(value) == "string" and value or nil)'
assert text.count(ANCHOR) == 1, "ancla showInterface no única"

BYPASS = """-- ============================================================================
-- DevAurora Code — KEY SYSTEM REMOVED
-- Launches directly on execution: no license key UI, no request to the
-- license server, no HMAC challenge. The main starts through the script's
-- own PendingStart path with the Pro tier unlocked.
-- ============================================================================
v3.onLicenseKeyAccepted(nil, {valid = true, version = "NightHub", subscriptionTier = "Pro", expiresAt = nil, serverTime = os.time()})"""

text = text.replace(ANCHOR, BYPASS, 1)

with open(DST, "w", encoding="utf-8", newline="") as f:
    f.write(text)

print("OK ->", DST)
print("líneas:", text.count("\n") + (0 if text.endswith("\n") else 1))
