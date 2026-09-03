# 02 - MODERNO Marlin 2.1.2.8 / Sirius 300x300 IDEX

Migración controlada de la personalidad de la Moebyus Sirius a Marlin 2.1.2.8 estable. No convierte la máquina en una cartesiana genérica y no modifica el núcleo de Marlin.

## Procedencia comprobada

El árbol `Marlin-2.1.2.8/` se compara en CI con el commit oficial de Marlin correspondiente a 2.1.2.8 (`1cd56c4ccd483045eb5a92c99e3ad3b5ab1bea6d`). Exceptuando `Marlin/Configuration.h` y `Marlin/Configuration_adv.h` —que contienen la personalidad Sirius— el código de firmware debe ser idéntico. La CI falla si aparece un parche oculto en el núcleo.

`migrar_configuracion.py` es la fuente reproducible de la personalización: la CI lo ejecuta y exige que no produzca diferencias respecto a los dos ficheros de configuración versionados.

## Configuración de máquina

- Placa: `BOARD_RUMBA`, ATmega2560.
- USB/serie base: `SERIAL_PORT 0`, 115200 baudios.
- Wi-Fi: **no activada en la versión base**.
- Extrusores: 2.
- Drivers: `TMC2209_STANDALONE` en X, X2, Y, Z, E0 y E1; sin UART para los drivers y corriente por Vref físico.
- Cama física: 300x300 mm.
- Área lógica: 295x295x275 mm.
- Límites: X=-48..295, Y=-12..295, Z=0..275.
- IDEX: `DUAL_X_CARRIAGE`, X1 a MIN, X2 a MAX.
- X2: mínimo 25, máximo/home 359.
- Auto-Park por defecto; duplicación `M605 S2` con offset 150 mm; espejo `M605 S3` disponible.
- Offset segundo hotend Y: 0.50 mm.
- Steps/mm: 80.19, 80.19, 400, 96.
- Max feedrate: 250, 150, 15, 80 mm/s.
- Max acceleration: 2000, 900, 100, 10000 mm/s².
- Classic Jerk: X20, Y20, Z0.4, E5.
- Homing XY: 4500 mm/min; Z: 600 mm/min; bump 3/3/2; `QUICK_HOME`.
- Termistores: T0=5, T1=5, cama=1.
- Límites térmicos: hotends 250 °C, cama 120 °C.
- PID hotend: 22.2 / 1.08 / 114; cama en bang-bang.
- `THERMAL_PROTECTION_HOTENDS`, `THERMAL_PROTECTION_BED`, watchdog y prevención de extrusión en frío activos.
- Auto-fan E0/E1: pines 6/8, activación 50 °C.
- LCD RepRapDiscount Full Graphic, SD, EEPROM y contador de impresión.

## Funciones históricas recuperadas en la auditoría final

Se comprobó la configuración pública de Moebyus y se recuperaron en Marlin 2.x las funciones que faltaban en la primera migración:

- `BABYSTEPPING`, incluido XY y doble clic para ajuste Z.
- Home individual X/Y/Z desde LCD.
- Speaker.
- Comportamiento del encoder original: 1 pulso/paso, 5 pasos/item y aceleración 75/160.
- Movimiento manual LCD: X/Y 80, Z 10, E 6 mm/s.
- `LCD_INFO_MENU`, coordenadas XY decimales y fuente grande de edición.
- `SD_CHECK_AND_RETRY`.
- Equivalencia moderna de `SD_DETECT_INVERTED`: `SD_DETECT_STATE HIGH`.
- No liberar automáticamente steppers al terminar una impresión SD.
- Eliminado el `G28XY` automático al abortar una impresión SD; no pertenecía a la Sirius original y podía provocar un movimiento no deseado sobre una pieza.
- `AUTOTEMP`, watchdog y soporte G2/G3 conservados.

## Compilación auditada

GitHub Actions compila esta configuración para `mega2560` con resultado correcto. En la auditoría del 2026-09-04:

- RAM: 4848 / 8192 bytes (59.2%).
- Flash: 146112 / 253952 bytes (57.5%).
- Resultado: `SUCCESS`.

La advertencia de autoasignación de X2 al siguiente driver E libre es esperada en la RUMBA: con E0/E1 ocupados, X2 usa el bloque E2.

El HEX versionado está en `firmware/SIRIUS-300x300-IDEX-Marlin-2.1.2.8-RUMBA-TMC2209-standalone.hex` y su huella se guarda en `firmware/SHA256SUMS.txt`.

## Validación física obligatoria

Una compilación y una auditoría de código no pueden demostrar la mecánica real. Antes de imprimir:

1. Comprobar temperaturas en frío de T0, T1 y cama.
2. Ejecutar `M119` y accionar manualmente XMIN, XMAX, YMIN y ZMIN.
3. Probar movimientos de pocos milímetros y el sentido de X, X2, Y y Z.
4. Verificar heater0/T0, heater1/T1 y cama/termistor por separado.
5. Tras migrar desde Marlin 1.1.1 ejecutar `M502`, `M500`, `M503`.
6. Validar Y progresivamente antes de llegar a 295 mm.
7. Validar físicamente el aparcamiento de X2 a 359 mm y la tensión del cableado.
8. Confirmar los jumpers 1/16 y Vref de cada TMC2209 en la placa real.
9. Confirmar inserción/retirada de SD en el LCD físico.

Esta es una migración personalizada. **No es firmware original de fábrica de Moebyus.**
