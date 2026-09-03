#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MARLIN = ROOT / "Marlin-2.1.2.8" / "Marlin"
CFG = MARLIN / "Configuration.h"
ADV = MARLIN / "Configuration_adv.h"

if not CFG.exists() or not ADV.exists():
    raise SystemExit("No existe el fuente Marlin 2.1.2.8 importado")


def set_define(text, name, value=None, required=True):
    """Activa o sustituye un #define sin consumir saltos de línea vecinos."""
    val = "" if value is None else f" {value}"
    pattern = re.compile(
        rf"(?m)^[ \t]*(?://[ \t]*)?#define[ \t]+{re.escape(name)}(?:[ \t]+[^\n]*)?$"
    )
    new, n = pattern.subn(f"#define {name}{val}", text, count=1)
    if n == 0:
        if required:
            raise RuntimeError(f"No se encontro {name}")
        return text
    return new


def comment_define(text, name, required=False):
    """Comenta un #define activo sin alterar líneas adyacentes."""
    pattern = re.compile(
        rf"(?m)^[ \t]*#define[ \t]+{re.escape(name)}(?:[ \t]+[^\n]*)?$"
    )
    new, n = pattern.subn(lambda m: "//" + m.group(0).lstrip(), text, count=1)
    if n == 0 and required:
        raise RuntimeError(f"No se encontro define activo {name}")
    return new


# Autoprueba mínima: las expresiones regulares nunca deben tragarse una línea // vecina.
_probe = "//\n//#define PRUEBA 1\n// siguiente\n"
_probe = set_define(_probe, "PRUEBA", "2")
if _probe != "//\n#define PRUEBA 2\n// siguiente\n":
    raise SystemExit("FALLO INTERNO: set_define consume líneas vecinas")
_probe = comment_define(_probe, "PRUEBA", required=True)
if _probe != "//\n//#define PRUEBA 2\n// siguiente\n":
    raise SystemExit("FALLO INTERNO: comment_define consume líneas vecinas")


cfg = CFG.read_text(encoding="utf-8")
adv = ADV.read_text(encoding="utf-8")

# ============================================================================
# IDENTIDAD / PLACA / COMUNICACION BASE
# ============================================================================
cfg = set_define(cfg, "STRING_CONFIG_H_AUTHOR", '"SIRIUS 300x300 IDEX - odoslf - Marlin 2.1.2.8"')
cfg = set_define(cfg, "MOTHERBOARD", "BOARD_RUMBA")
cfg = set_define(cfg, "SERIAL_PORT", "0")
cfg = set_define(cfg, "BAUDRATE", "115200")
# La variante base NO habilita Wi-Fi. La rama Wi-Fi usara SERIAL_PORT_2=3.
cfg = comment_define(cfg, "SERIAL_PORT_2")
cfg = comment_define(cfg, "BAUDRATE_2")
cfg = set_define(cfg, "CUSTOM_MACHINE_NAME", '"SIRIUS 300 IDEX"')
cfg = set_define(cfg, "LCD_LANGUAGE", "es")

# Presets historicos de la Sirius.
cfg = set_define(cfg, "PREHEAT_1_TEMP_HOTEND", "190")
cfg = set_define(cfg, "PREHEAT_1_TEMP_BED", "60")
cfg = set_define(cfg, "PREHEAT_1_FAN_SPEED", "96")
cfg = set_define(cfg, "PREHEAT_2_TEMP_HOTEND", "225")
cfg = set_define(cfg, "PREHEAT_2_TEMP_BED", "90")
cfg = set_define(cfg, "PREHEAT_2_FAN_SPEED", "0")

# ============================================================================
# DRIVERS: TMC2209 V1.3 STANDALONE, SIN UART
# ============================================================================
for axis in ("X", "Y", "Z", "X2", "E0", "E1"):
    cfg = set_define(cfg, f"{axis}_DRIVER_TYPE", "TMC2209_STANDALONE")

# ============================================================================
# EXTRUSORES / OFFSETS
# ============================================================================
cfg = set_define(cfg, "EXTRUDERS", "2")
cfg = set_define(cfg, "DEFAULT_NOMINAL_FILAMENT_DIA", "3.00")
cfg = set_define(cfg, "HOTEND_OFFSET_X", "{ 0.0, 0.00 }")
cfg = set_define(cfg, "HOTEND_OFFSET_Y", "{ 0.0, 0.50 }")
cfg = set_define(cfg, "HOTEND_OFFSET_Z", "{ 0.0, 0.00 }")

# ============================================================================
# TEMPERATURAS Y SEGURIDAD
# ============================================================================
cfg = set_define(cfg, "TEMP_SENSOR_0", "5")
cfg = set_define(cfg, "TEMP_SENSOR_1", "5")
cfg = set_define(cfg, "TEMP_SENSOR_BED", "1")
cfg = set_define(cfg, "HEATER_0_MINTEMP", "5")
cfg = set_define(cfg, "HEATER_1_MINTEMP", "5")
cfg = set_define(cfg, "BED_MINTEMP", "5")
cfg = set_define(cfg, "HEATER_0_MAXTEMP", "250")
cfg = set_define(cfg, "HEATER_1_MAXTEMP", "250")
cfg = set_define(cfg, "BED_MAXTEMP", "120")
cfg = set_define(cfg, "THERMAL_PROTECTION_HOTENDS")
cfg = set_define(cfg, "THERMAL_PROTECTION_BED")
cfg = set_define(cfg, "PIDTEMP")
cfg = set_define(cfg, "DEFAULT_KP", "22.2")
cfg = set_define(cfg, "DEFAULT_KI", "1.08")
cfg = set_define(cfg, "DEFAULT_KD", "114")
cfg = comment_define(cfg, "PIDTEMPBED")
cfg = set_define(cfg, "MAX_BED_POWER", "255")
cfg = set_define(cfg, "PREVENT_COLD_EXTRUSION")
cfg = set_define(cfg, "EXTRUDE_MINTEMP", "150")
cfg = set_define(cfg, "PREVENT_LENGTHY_EXTRUDE")
cfg = set_define(cfg, "EXTRUDE_MAXLENGTH", "200")

# ============================================================================
# ENDSTOPS: X1=XMIN, X2=XMAX, Y=YMIN, Z=ZMIN. NC + pullups como origen.
# ============================================================================
for name in ("USE_XMIN_PLUG", "USE_XMAX_PLUG", "USE_YMIN_PLUG", "USE_ZMIN_PLUG"):
    cfg = set_define(cfg, name)
for name in ("USE_YMAX_PLUG", "USE_ZMAX_PLUG"):
    cfg = comment_define(cfg, name)
for name in ("X_MIN_ENDSTOP_HIT_STATE", "X_MAX_ENDSTOP_HIT_STATE", "Y_MIN_ENDSTOP_HIT_STATE", "Z_MIN_ENDSTOP_HIT_STATE"):
    cfg = set_define(cfg, name, "LOW", required=False)
for name in ("X_MIN_ENDSTOP_INVERTING", "X_MAX_ENDSTOP_INVERTING", "Y_MIN_ENDSTOP_INVERTING", "Z_MIN_ENDSTOP_INVERTING"):
    cfg = set_define(cfg, name, "false", required=False)

# ============================================================================
# GEOMETRIA: cama fisica 300x300, area logica conservadora 295x295x275.
# ============================================================================
cfg = set_define(cfg, "X_BED_SIZE", "295")
cfg = set_define(cfg, "Y_BED_SIZE", "295")
cfg = set_define(cfg, "X_MIN_POS", "-48")
cfg = set_define(cfg, "Y_MIN_POS", "-12")
cfg = set_define(cfg, "Z_MIN_POS", "0")
cfg = set_define(cfg, "X_MAX_POS", "295")
cfg = set_define(cfg, "Y_MAX_POS", "295")
cfg = set_define(cfg, "Z_MAX_POS", "275")
cfg = set_define(cfg, "MIN_SOFTWARE_ENDSTOPS")
cfg = set_define(cfg, "MAX_SOFTWARE_ENDSTOPS")
cfg = set_define(cfg, "X_HOME_DIR", "-1")
cfg = set_define(cfg, "Y_HOME_DIR", "-1")
cfg = set_define(cfg, "Z_HOME_DIR", "-1")
cfg = set_define(cfg, "HOMING_FEEDRATE_MM_M", "{ (75*60), (75*60), (10*60) }")
cfg = set_define(cfg, "INVERT_X_DIR", "false")
cfg = set_define(cfg, "INVERT_Y_DIR", "true")
cfg = set_define(cfg, "INVERT_Z_DIR", "false")
cfg = set_define(cfg, "INVERT_E0_DIR", "false")
cfg = set_define(cfg, "INVERT_E1_DIR", "false")

# ============================================================================
# MOVIMIENTO: valores originales Moebyus.
# ============================================================================
cfg = set_define(cfg, "DEFAULT_AXIS_STEPS_PER_UNIT", "{ 80.19, 80.19, 400, 96 }")
cfg = set_define(cfg, "DEFAULT_MAX_FEEDRATE", "{ 250, 150, 15, 80 }")
cfg = set_define(cfg, "DEFAULT_MAX_ACCELERATION", "{ 2000, 900, 100, 10000 }")
cfg = set_define(cfg, "DEFAULT_ACCELERATION", "2000")
cfg = set_define(cfg, "DEFAULT_RETRACT_ACCELERATION", "3000")
cfg = set_define(cfg, "DEFAULT_TRAVEL_ACCELERATION", "3000")
cfg = set_define(cfg, "CLASSIC_JERK")
cfg = set_define(cfg, "DEFAULT_XJERK", "20.0")
cfg = set_define(cfg, "DEFAULT_YJERK", "20.0")
cfg = set_define(cfg, "DEFAULT_ZJERK", "0.4")
cfg = set_define(cfg, "DEFAULT_EJERK", "5.0")

# ============================================================================
# EEPROM / SD / LCD. Se recupera el comportamiento que tenia la Sirius 1.1.1.
# ============================================================================
cfg = set_define(cfg, "EEPROM_SETTINGS")
cfg = set_define(cfg, "EEPROM_CHITCHAT", required=False)
cfg = set_define(cfg, "SDSUPPORT")
cfg = set_define(cfg, "SD_CHECK_AND_RETRY", required=False)
cfg = set_define(cfg, "REPRAP_DISCOUNT_FULL_GRAPHIC_SMART_CONTROLLER")
cfg = set_define(cfg, "PRINTJOB_TIMER_AUTOSTART")
cfg = set_define(cfg, "PRINTCOUNTER", required=False)
cfg = set_define(cfg, "ENCODER_PULSES_PER_STEP", "1", required=False)
cfg = set_define(cfg, "ENCODER_STEPS_PER_MENU_ITEM", "5", required=False)
cfg = set_define(cfg, "INDIVIDUAL_AXIS_HOMING_MENU", required=False)
cfg = set_define(cfg, "SPEAKER", required=False)

# ============================================================================
# ADVANCED: protecciones termicas y ventiladores.
# ============================================================================
adv = set_define(adv, "CONFIG_EXPORT", "2", required=False)
adv = set_define(adv, "THERMAL_PROTECTION_PERIOD", "40")
adv = set_define(adv, "THERMAL_PROTECTION_HYSTERESIS", "4")
adv = set_define(adv, "WATCH_TEMP_PERIOD", "20")
adv = set_define(adv, "WATCH_TEMP_INCREASE", "2")
adv = set_define(adv, "THERMAL_PROTECTION_BED_PERIOD", "20")
adv = set_define(adv, "THERMAL_PROTECTION_BED_HYSTERESIS", "2")
adv = set_define(adv, "WATCH_BED_TEMP_PERIOD", "60")
adv = set_define(adv, "WATCH_BED_TEMP_INCREASE", "2")
adv = set_define(adv, "FAN_KICKSTART_TIME", "100")
adv = set_define(adv, "E0_AUTO_FAN_PIN", "6")
adv = set_define(adv, "E1_AUTO_FAN_PIN", "8")
adv = set_define(adv, "EXTRUDER_AUTO_FAN_TEMPERATURE", "50")
adv = set_define(adv, "EXTRUDER_AUTO_FAN_SPEED", "255")

# ============================================================================
# IDEX: geometria y comportamiento de doble carro original.
# ============================================================================
adv = set_define(adv, "DUAL_X_CARRIAGE")
adv = set_define(adv, "X1_MIN_POS", "X_MIN_POS")
adv = set_define(adv, "X1_MAX_POS", "X_BED_SIZE")
adv = set_define(adv, "X2_MIN_POS", "25")
adv = set_define(adv, "X2_MAX_POS", "359")
adv = set_define(adv, "X2_HOME_POS", "X2_MAX_POS")
adv = set_define(adv, "DEFAULT_DUAL_X_CARRIAGE_MODE", "DXC_AUTO_PARK_MODE")
adv = set_define(adv, "DEFAULT_DUPLICATION_X_OFFSET", "150")
# En Marlin 2.x la elevacion de cambio de herramienta se unifica en TOOLCHANGE_ZRAISE.
adv = set_define(adv, "TOOLCHANGE_ZRAISE", "2", required=False)

# ============================================================================
# HOMING / STEPPERS / MICROSTEP.
# ============================================================================
adv = set_define(adv, "HOMING_BUMP_MM", "{ 3, 3, 2 }")
adv = set_define(adv, "HOMING_BUMP_DIVISOR", "{ 4, 4, 2 }")
adv = set_define(adv, "QUICK_HOME")
adv = set_define(adv, "DEFAULT_STEPPER_TIMEOUT_SEC", "120")
for name in ("DISABLE_IDLE_X", "DISABLE_IDLE_Y", "DISABLE_IDLE_Z", "DISABLE_IDLE_E"):
    adv = set_define(adv, name)
adv = set_define(adv, "MICROSTEP_MODES", "{ 16, 16, 16, 16, 16, 16 }")

# ============================================================================
# FUNCIONES HISTORICAS DE LA SIRIUS QUE DEBEN CONSERVARSE EN MARLIN 2.x.
# ============================================================================
adv = set_define(adv, "AUTOTEMP", required=False)
adv = set_define(adv, "AUTOTEMP_OLDWEIGHT", "0.98", required=False)
adv = set_define(adv, "USE_WATCHDOG", required=False)
adv = set_define(adv, "ARC_SUPPORT", required=False)
adv = set_define(adv, "N_ARC_CORRECTION", "25", required=False)
adv = set_define(adv, "MINIMUM_PLANNER_SPEED", "0.05", required=False)

# Movimiento manual del LCD original: X/Y 80, Z 10, E 6 mm/s.
adv = set_define(adv, "MANUAL_FEEDRATE", "{ 80*60, 80*60, 10*60, 6*60 }", required=False)

# Encoder original.
adv = set_define(adv, "ENCODER_RATE_MULTIPLIER", required=False)
adv = set_define(adv, "ENCODER_10X_STEPS_PER_SEC", "75", required=False)
adv = set_define(adv, "ENCODER_100X_STEPS_PER_SEC", "160", required=False)

# Pantalla / menus originales.
adv = set_define(adv, "LCD_INFO_MENU", required=False)
adv = set_define(adv, "LCD_DECIMAL_SMALL_XY", required=False)
adv = set_define(adv, "XYZ_HOLLOW_FRAME", required=False)
adv = set_define(adv, "MENU_HOLLOW_FRAME", required=False)
adv = set_define(adv, "USE_BIG_EDIT_FONT", required=False)

# Babystepping original, incluido doble clic para Z.
adv = set_define(adv, "BABYSTEPPING", required=False)
adv = set_define(adv, "BABYSTEP_XY", required=False)
adv = set_define(adv, "BABYSTEP_INVERT_Z", "false", required=False)
adv = set_define(adv, "BABYSTEP_MULTIPLICATOR_Z", "1", required=False)
adv = set_define(adv, "BABYSTEP_MULTIPLICATOR_XY", "1", required=False)
adv = set_define(adv, "DOUBLECLICK_FOR_Z_BABYSTEPPING", required=False)
adv = set_define(adv, "DOUBLECLICK_MAX_INTERVAL", "1250", required=False)

# SD: conservar deteccion invertida y reintentos de la Sirius antigua.
# SD_DETECT_INVERTED de Marlin 1.1.x equivale a SD_DETECT_STATE HIGH en 2.x.
adv = set_define(adv, "SD_DETECT_STATE", "HIGH", required=False)
adv = set_define(adv, "SDCARD_RATHERRECENTFIRST", required=False)
# La Sirius no liberaba los steppers automaticamente al terminar una impresion SD.
adv = set_define(adv, "SD_FINISHED_STEPPERRELEASE", "false", required=False)
# No se ejecuta un homing automatico al abortar: podria mover los carros sobre una pieza.
adv = comment_define(adv, "EVENT_GCODE_SD_ABORT")

marker = """\n/**\n * ============================================================================\n * VARIANTE PERSONALIZADA: MOEBYUS SIRIUS CAMA 300x300 / IDEX\n * Migracion controlada desde SIRIUS11 Marlin 1.1.1 a Marlin 2.1.2.8 estable.\n * Cama fisica 300x300; area logica 295x295x275. TMC2209 standalone, sin UART.\n * Repositorio: odoslf/Impresora-Sirius-firmware-cama-300x300\n * NO ES EL FIRMWARE ORIGINAL DE FABRICA.\n * ============================================================================\n */\n"""
if "VARIANTE PERSONALIZADA: MOEBYUS SIRIUS" not in cfg:
    cfg = cfg.replace("#pragma once\n", "#pragma once\n" + marker, 1)
if "VARIANTE PERSONALIZADA: MOEBYUS SIRIUS" not in adv:
    adv = adv.replace("#pragma once\n", "#pragma once\n" + marker, 1)

CFG.write_text(cfg, encoding="utf-8")
ADV.write_text(adv, encoding="utf-8")

# Comprobaciones bloqueantes de la migracion. Si falta algo, no se da por buena.
checks = {
    CFG: [
        "#define MOTHERBOARD BOARD_RUMBA",
        "#define SERIAL_PORT 0",
        "#define BAUDRATE 115200",
        "#define X_DRIVER_TYPE TMC2209_STANDALONE",
        "#define X2_DRIVER_TYPE TMC2209_STANDALONE",
        "#define Y_DRIVER_TYPE TMC2209_STANDALONE",
        "#define Z_DRIVER_TYPE TMC2209_STANDALONE",
        "#define E0_DRIVER_TYPE TMC2209_STANDALONE",
        "#define E1_DRIVER_TYPE TMC2209_STANDALONE",
        "#define EXTRUDERS 2",
        "#define TEMP_SENSOR_0 5",
        "#define TEMP_SENSOR_1 5",
        "#define TEMP_SENSOR_BED 1",
        "#define X_BED_SIZE 295",
        "#define Y_BED_SIZE 295",
        "#define X_MIN_POS -48",
        "#define Y_MIN_POS -12",
        "#define X_MAX_POS 295",
        "#define Y_MAX_POS 295",
        "#define Z_MAX_POS 275",
        "#define DEFAULT_AXIS_STEPS_PER_UNIT { 80.19, 80.19, 400, 96 }",
        "#define THERMAL_PROTECTION_HOTENDS",
        "#define THERMAL_PROTECTION_BED",
        "#define SDSUPPORT",
        "#define REPRAP_DISCOUNT_FULL_GRAPHIC_SMART_CONTROLLER",
    ],
    ADV: [
        "#define DUAL_X_CARRIAGE",
        "#define X2_MIN_POS 25",
        "#define X2_MAX_POS 359",
        "#define X2_HOME_POS X2_MAX_POS",
        "#define DEFAULT_DUAL_X_CARRIAGE_MODE DXC_AUTO_PARK_MODE",
        "#define DEFAULT_DUPLICATION_X_OFFSET 150",
        "#define E0_AUTO_FAN_PIN 6",
        "#define E1_AUTO_FAN_PIN 8",
        "#define HOMING_BUMP_MM { 3, 3, 2 }",
        "#define MANUAL_FEEDRATE { 80*60, 80*60, 10*60, 6*60 }",
        "#define SD_FINISHED_STEPPERRELEASE false",
    ],
}
for path, needles in checks.items():
    data = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in data:
            raise SystemExit(f"FALLO DE MIGRACION: falta {needle} en {path.name}")

if re.search(r"(?m)^[ \t]*#define[ \t]+EVENT_GCODE_SD_ABORT\b", ADV.read_text(encoding="utf-8")):
    raise SystemExit("FALLO DE MIGRACION: EVENT_GCODE_SD_ABORT debe quedar desactivado")

print("Migracion Sirius 300x300 aplicada y verificada correctamente")
