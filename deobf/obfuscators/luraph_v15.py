"""
Luraph v15 front end.

NOTE: the uploaded zip did not include obfuscators/luraph_v15.py; this is the
plugin reconstructed to the interface base.py/CLAUDE.md define, running the
shipped engine pieces (harness.py + envlog.luau, which already carry Luraph's
capture machinery: CHAIN.*, __PA/__PF/__SKIPP).

detect(source), the cheap signatures CLAUDE.md prescribes ("header comment,
signature strings, VM shape regex"):
  - the LPH_* preprocessor macros; LPH_ENCBUF and LPH_PRECHECK only exist in
    the v15 generation (lura.ph docs) -> confirmed v15;
  - an explicit v13/v14 banner -> an older generation: not v15, 0.0;
  - the Luraph / lura.ph watermark, also hidden as \\ddd escapes
    ("\\76\\117\\114\\97\\112\\104" is "Luraph").

deobfuscate(job): the documented first stage of a plugin -- run the protected
script in the fake Roblox/executor environment and write the behaviour trace
("Start with the trace (copy generic.py)"), with the spin watchdog Luraph's
driver always runs with ("Luraph's driver runs with --cfg spin=N from run 1").
The lifter half of the plugin (devirtualization: devirt.py + structure.py +
variables.py + spacing.py + tidy.py) was not part of the upload, so no
devirtualized output is produced here; dropping those modules in restores it
(backend.lower / backend.polish / backend.finish_text are all shipped).
"""
import re
import sys

import harness
import traceout as trace
from obfuscators.base import Obfuscator

# macros of Luraph's preprocessor; the last two only exist in v15
V15_MACROS = ("LPH_ENCBUF", "LPH_PRECHECK")
ANY_MACROS = ("LPH_JIT", "LPH_NOVIRTUALIZE", "LPH_ENCSTR", "LPH_ENCBUF",
              "LPH_PRECHECK", "LPH_CRASH", "LPH_OBFUSCATED", "LPH_ALLOWCONST")
OLD_BANNER = re.compile(r"luraph\s*v(?:13|14)\b", re.I)
WATERMARK = re.compile(r"lura\.ph|luraph", re.I)
DEC_ESCAPE = re.compile(r"\\(\d{1,3})")

# the spin watchdog (envlog CFG.spin): N idle dispatch-loop checks in a row
# end the run like a budget abort, keeping the trace. Luraph's anti-tamper
# response is exactly such a spin, so the driver always runs with it on.
SPIN = 200


def _escaped_watermark(source, limit=262144):
    """The watermark hidden in decimal escapes: \\76\\117\\114\\97\\112\\104."""
    try:
        text = DEC_ESCAPE.sub(lambda m: chr(int(m.group(1)) & 0xFF), source[:limit])
    except ValueError:
        return False
    return bool(WATERMARK.search(text))


class LuraphV15(Obfuscator):
    name = "luraph_v15"
    label = "Luraph v15"
    doc = "LURAPH.md"

    def detect(self, source):
        head = source[:262144]          # cheap: the header region carries the banners
        if OLD_BANNER.search(head):
            return 0.0                  # an explicitly older Luraph generation
        conf = 0.0
        if any(m in source for m in V15_MACROS):
            conf = 0.95                 # v15-only macros: confirmed
        elif any(m in source for m in ANY_MACROS):
            conf = 0.65                 # Luraph, generation not pinned by the macros
        if WATERMARK.search(head) or _escaped_watermark(source):
            conf = conf or 0.5
            conf = min(0.99, conf + 0.1)
        return conf

    def deobfuscate(self, job):
        args = job.args
        cache_path = harness.load_p2d_cache(job.input, args.studio)
        runner = harness.Runner(job)
        cfg = harness.user_cfg(args, harness.base_cfg(args))
        cfg.setdefault("spin", SPIN)
        print("[*] tracing %s..." % job.input, file=sys.stderr)
        body, err = runner.run(job.source, cfg)
        if body is None:
            harness.save_raw(args.raw)
            runner.finish()
            sys.exit("[!] " + err)
        runner.finish()
        harness.save_raw(args.raw)
        body = harness.take_p2d(body, cache_path, args.studio)
        body = harness.p2d_miss(body, cache_path)
        _, body = harness.take_chunks(body)
        body, strings = trace.take_strings(body)
        # preamble=True: Luraph's probe block would be stripped by tidy.py
        # (not in the upload); raw-trace render keeps it, commented as such.
        text = trace.render(job.credit_header() + trace.header(job.input) + body,
                            args, preamble=True)
        job.write(job.trace_path, text)
        if strings is not None:
            job.write(job.path(".strings.txt"), strings)
        trace.status_line(body)
        return job.trace_path
