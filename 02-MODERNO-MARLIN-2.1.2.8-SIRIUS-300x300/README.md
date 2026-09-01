# 02 - MODERNO Marlin 2.1.2.8 / Sirius 300x300 IDEX

Esta carpeta contiene la migración de la configuración de la Sirius a Marlin 2.1.2.8 estable.

## Objetivo
Mantener la personalidad y funciones especiales de la máquina original, pero sobre una base Marlin moderna, sin convertirla en una cartesiana genérica.

## Configuración migrada
- MOTHERBOARD = BOARD_RUMBA.
- ATmega2560 / entorno mega2560.
- SERIAL_PORT 0 / 115200.
- EXTRUDERS = 2.
- X/Y/Z/E0/E1 y X2 con TMC2209_STANDALONE.
- Sin UART y sin corriente controlada por firmware.
- DUAL_X_CARRIAGE activo.
- X1_MIN_POS = X_MIN_POS.
- X1_MAX_POS = X_BED_SIZE.
- X2_MIN_POS = 25.
- X2_MAX_POS = 359.
- X2_HOME_POS = 359.
- Auto-Park por defecto.
- Duplicación: M605 S2, offset inicial 150 mm.
- Espejo: M605 S3 disponible.
- HOTEND_OFFSET_Y segundo hotend = 0.50 mm.
- X_BED_SIZE = 295.
- Y_BED_SIZE = 295.
- X = -48 .. 295.
- Y = -12 .. 295.
- Z = 0 .. 275.
- Steps/mm = 80.19, 80.19, 400, 96.
- Max feedrate = 250, 150, 15, 80.
- Max acceleration = 2000, 900, 100, 10000.
- Classic jerk X20 / Y20 / Z0.4.
- TEMP_SENSOR_0 = 5.
- TEMP_SENSOR_1 = 5.
- TEMP_SENSOR_BED = 1.
- Hotend PID = 22.2 / 1.08 / 114.
- Cama en bang-bang.
- THERMAL_PROTECTION_HOTENDS y THERMAL_PROTECTION_BED activos.
- PREVENT_COLD_EXTRUSION a 150 C.
- RepRapDiscount Full Graphic Smart Controller.
- SD y EEPROM.

## Contenido
- `Marlin-2.1.2.8/`: fuente completo usado para compilar.
- `migrar_configuracion.py`: script que aplicó la migración controlada.
- `firmware/`: HEX compilado y SHA256.
- `BUILD_INFO.txt`: resumen técnico de la build.

## Antes del primer uso real
1. Flashear con la máquina vigilada y posibilidad de cortar alimentación.
2. No ejecutar G28 completo inmediatamente.
3. Comprobar temperaturas en frío de T0, T1 y cama.
4. Ejecutar M119 y accionar manualmente XMIN, XMAX, YMIN y ZMIN.
5. Verificar movimientos de pocos milímetros y sentido de X, X2, Y y Z.
6. Verificar por separado heater0/T0, heater1/T1 y cama/termistor de cama.
7. Tras migrar desde Marlin 1.1.1: M502, M500, M503.
8. Verificar recorridos progresivamente antes de usar Y=295 o el aparcamiento X2=359.

El HEX moderno es `firmware/SIRIUS-300x300-IDEX-Marlin-2.1.2.8-RUMBA-TMC2209-standalone.hex`.

Esta es una migración personalizada. NO es firmware original de fábrica de Moebyus.