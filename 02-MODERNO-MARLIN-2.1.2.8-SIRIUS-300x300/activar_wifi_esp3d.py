#!/usr/bin/env python3
"""Genera la variante Sirius + ESP3D sobre UART3 de RUMBA+.

Primero reaplica la configuración base canónica y después activa únicamente
el segundo puerto serie. No altera motores, IDEX, geometría ni térmicos.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CFG = ROOT / "Marlin-2.1.2.8" / "Marlin" / "Configuration.h"
BASE = ROOT / "migrar_configuracion.py"

subprocess.run([sys.executable, str(BASE)], check=True)


def set_define(text, name, value):
    pattern = re.compile(
        rf"(?m)^[ \t]*(?://[ \t]*)?#define[ \t]+{re.escape(name)}(?:[ \t]+[^\n]*)?$"
    )
    new, n = pattern.subn(f"#define {name} {value}", text, count=1)
    if n != 1:
        raise RuntimeError(f"No se pudo configurar {name}")
    return new


cfg = CFG.read_text(encoding="utf-8")
cfg = set_define(cfg, "SERIAL_PORT_2", "3")
cfg = set_define(cfg, "BAUDRATE_2", "115200")
CFG.write_text(cfg, encoding="utf-8")

check = CFG.read_text(encoding="utf-8")
required = (
    "#define SERIAL_PORT 0",
    "#define BAUDRATE 115200",
    "#define SERIAL_PORT_2 3",
    "#define BAUDRATE_2 115200",
)
for needle in required:
    if needle not in check:
        raise SystemExit(f"FALLO WIFI: falta {needle}")

if re.search(r"(?m)^[ \t]*#define[ \t]+BLUETOOTH\b", check):
    raise SystemExit("FALLO WIFI: BLUETOOTH no debe habilitarse para ESP3D")

print("Variante ESP3D UART3 aplicada: USB UART0 + Wi-Fi UART3 a 115200")
