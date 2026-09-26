#!/usr/bin/env python3
"""DevAurora Code — quita el sistema de key del script deofuscado.

Parches (todos quirúrgicos, el resto del script queda intacto):
  A) Cabecera: bloque de config del bypass (modo full/lite) para tocar a mano.
  B) `fn28(function()` (línea 4641): se sustituye por el shim de estado que
     replica el commit de W() sin pasar por AUTH/MODE_SELECT ni llamar al
     servidor. El callback del payload pasa a ser `local DevAuroraPayload`.
  C) Última línea `end)`: cierre del payload + launch directo diferido
     (pcall + limpieza en fallo, igual que el defer de W). Sin fn27
     (monitor de revalidación contra el servidor) y sin UI de key.
  D) Arranque del event collector desactivado: se autentica con la key
     contra la Cokeboys Event API; sin key real solo puede fallar.
"""
import sys

SRC = "/home/z/my-project/download/deobfuscated_main.lua"
DST = "/home/z/my-project/download/deobfuscated_main_nokey.lua"

with open(SRC, encoding="utf-8", newline="") as f:
    text = f.read()

# ---------- A) cabecera de config ----------
HEADER_ANCHOR = "-- Local names are inferred from use (the original names are not in the bytecode)\n"
assert text.count(HEADER_ANCHOR) == 1, "ancla de cabecera no única"

CONFIG_BLOCK = HEADER_ANCHOR + """
-- ============================================================================
-- DevAurora Code — KEY SYSTEM REMOVED
-- This copy launches directly on execution: no key prompt, no /validatekey
-- request, no revalidation monitor, no telemetry collector.
-- Mode config: "full" = complete runtime | "lite" = lite runtime
-- (set getgenv().__CokeboysBypassMode = "lite" before executing for lite)
-- ============================================================================
getgenv().__CokeboysBypassMode = getgenv().__CokeboysBypassMode or "full"
"""
text = text.replace(HEADER_ANCHOR, CONFIG_BLOCK, 1)

# ---------- B) shim de estado en el punto de launch ----------
LAUNCH_ANCHOR = "\nfn28(function()\n"
assert text.count(LAUNCH_ANCHOR) == 1, "ancla de launch no única"

SHIM = """-- ============================================================================
-- DevAurora Code — key system bypass (replaces the fn28 authenticated launch)
-- Replicates the loader's own commit path (W) with a local, always-valid
-- state: VALIDATING -> INITIALIZING with the launch table resolved, so the
-- runtime's auth checks and __CokeboysMarkRuntimeReady work unchanged.
-- ============================================================================
do
  local bypassMode = (getgenv().__CokeboysBypassMode == "lite") and "lite" or "full"
  fn20({success = true, permanent = true})
  cokeboysLoaderController2.authenticatedKey = "DevAurora-Bypass"
  cokeboysLoaderController2.validationGeneration = cokeboysLoaderController2.validationGeneration + 1
  cokeboysLoaderController2.authenticationGeneration = cokeboysLoaderController2.validationGeneration
  if cokeboysLoaderController2.state == "BOOT" or cokeboysLoaderController2.state == "AUTH" or cokeboysLoaderController2.state == "AUTH_ERROR" then
    cokeboysLoaderController2:transition("VALIDATING", cokeboysLoaderController2.state)
  end
  cokeboysLoaderController2.selectionCommitted = true
  cokeboysLoaderController2.initializationCommitted = true
  cokeboysLoaderController2.resolvedExperience = bypassMode
  cokeboysLoaderController2:transition("INITIALIZING", "VALIDATING")
  genv.__CokeboysResolvedExperienceLaunch = {
    authenticated = true,
    generation = cokeboysLoaderController2.launchGeneration,
    validationGeneration = cokeboysLoaderController2.authenticationGeneration,
    experience = bypassMode,
  }
end
local DevAuroraPayload = function()
"""
text = text.replace(LAUNCH_ANCHOR, SHIM, 1)

# ---------- C) cierre + launch directo ----------
if not text.endswith("end)\n"):
    sys.exit("el archivo no termina en 'end)' como se esperaba")

LAUNCHER = """end

-- ============================================================================
-- DevAurora Code — direct launch (no key UI, no server, no revalidation)
-- ============================================================================
task.defer(function()
  fn22()
  local devauroraOk, devauroraErr = pcall(DevAuroraPayload)
  if not devauroraOk then
    warn("Cokeboys initialization failed: " .. tostring(devauroraErr))
    genv.__CokeboysResolvedExperienceLaunch = nil
    local devauroraUnload = genv.CokeboysFullUnload
    if cokeboysLoaderController2.fullUnloadInstalled == true and type(devauroraUnload) == "function" then
      pcall(devauroraUnload)
    else
      genv.CokeboysScriptLoaded = false
    end
  end
end)
"""
text = text[:-len("end)\n")] + LAUNCHER

# ---------- D) desactivar el arranque del event collector ----------
COLL_ANCHOR = "local r = getgenv().__CokeboysStartPVPEventCollector;"
assert text.count(COLL_ANCHOR) == 1, "ancla del collector no única"
text = text.replace(
    COLL_ANCHOR,
    'local r = nil -- DevAurora: event collector disabled (authenticates with a key against the Cokeboys Event API)',
    1,
)

with open(DST, "w", encoding="utf-8", newline="") as f:
    f.write(text)

print("OK ->", DST)
print("líneas:", text.count("\n") + (0 if text.endswith("\n") else 1))
