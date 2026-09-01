#!/usr/bin/env python3
from pathlib import Path

ROOT = Path('02-MODERNO-MARLIN-2.1.2.8-SIRIUS-300x300')
p = ROOT / 'migrar_configuracion.py'
s = p.read_text(encoding='utf-8')

# Evita que el patrón del migrador consuma accidentalmente la línea siguiente.
s = s.replace(r'(?:\s+[^\n]*)?$', r'(?:[ \t]+[^\n]*)?$')

# Nomenclatura actual de Marlin 2.1.2.8.
s = s.replace(
    'adv = set_define(adv, "DEFAULT_STEPPER_DEACTIVE_TIME", "120")',
    'adv = set_define(adv, "DEFAULT_STEPPER_TIMEOUT_SEC", "120")\n'
    'for _n in ("DISABLE_IDLE_X", "DISABLE_IDLE_Y", "DISABLE_IDLE_Z", "DISABLE_IDLE_E"):\n'
    '    adv = set_define(adv, _n)'
)

# Presets térmicos históricos seguros de la Sirius. No se eleva MAXTEMP.
anchor = 'cfg = set_define(cfg, "LCD_LANGUAGE", "es")'
preheats = '''cfg = set_define(cfg, "PREHEAT_1_TEMP_HOTEND", "190")
cfg = set_define(cfg, "PREHEAT_1_TEMP_BED", "60")
cfg = set_define(cfg, "PREHEAT_1_FAN_SPEED", "96")
cfg = set_define(cfg, "PREHEAT_2_TEMP_HOTEND", "225")
cfg = set_define(cfg, "PREHEAT_2_TEMP_BED", "90")
cfg = set_define(cfg, "PREHEAT_2_FAN_SPEED", "0")'''
if preheats not in s:
    s = s.replace(anchor, anchor + '\n' + preheats)

p.write_text(s, encoding='utf-8')
exec(compile(s, str(p), 'exec'), {'__name__': '__main__', '__file__': str(p)})
