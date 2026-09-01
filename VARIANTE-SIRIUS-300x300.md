# Variante Moebyus Sirius 300×300

## Propósito

Esta configuración está destinada a una **Moebyus Sirius / SIRIUS11 con cama caliente cuadrada de 300×300 mm**, diferente de la configuración pública original con `Y_MAX_POS=205`.

No debe presentarse como firmware original de fábrica. Es una adaptación propia construida sobre el código publicado por Moebyus.

## Geometría configurada

| Parámetro | Valor |
|---|---:|
| Cama física X | 300 mm |
| Cama física Y | 300 mm |
| X_MIN_POS | -48 mm |
| Y_MIN_POS | -12 mm |
| Z_MIN_POS | 0 mm |
| X_MAX_POS | 295 mm |
| Y_MAX_POS | 295 mm |
| Z_MAX_POS | 275 mm |

### Motivo de los límites

- `X_MAX_POS=295` ya estaba en la configuración pública de la Sirius.
- `Y_MAX_POS=205` se amplía a `295` para la cama cuadrada 300×300.
- `Z_MAX_POS=275` se conserva porque el tamaño de la cama no demuestra que la altura mecánica haya aumentado.
- Los mínimos negativos se conservan porque forman parte de la geometría de homing y aparcamiento de los carros.

## Hardware mantenido

- `BOARD_RUMBA`
- ATmega2560
- 2 extrusores
- DUAL_X_CARRIAGE / IDEX
- Hotends MK8
- XY GT2
- Z husillos
- XMIN, XMAX, YMIN y ZMIN
- LCD RepRapDiscount Full Graphic
- SD
- EEPROM
- Protección térmica hotends y cama
- Termistor hotends tipo 5
- Termistor cama tipo 1

## Movimiento base conservado

```text
Steps/mm:      X 80.19 | Y 80.19 | Z 400 | E 96
Max feedrate:  X 250   | Y 150   | Z 15  | E 80
Max accel:     X 2000  | Y 900   | Z 100 | E 10000
Jerk:          X 20    | Y 20    | Z 0.4 | E 5
```

Estos valores proceden de la configuración pública de Moebyus y no se modifican en esta variante sin una calibración física específica.

## TMC2209

Los BIGTREETECH TMC2209 V1.3 se usan en **standalone STEP/DIR**, sin UART. Por tanto:

- Marlin no programa la corriente del driver.
- La corriente se ajusta mediante Vref físico.
- La lógica STEP/DIR y ENABLE de la configuración original se conserva.
- El microstepping previsto es 1/16.

## IDEX

Se mantiene la configuración original:

```text
DUAL_X_CARRIAGE = habilitado
X2_MIN_POS = 25
X2_MAX_POS = 359
X2_HOME_DIR = 1
DEFAULT_DUAL_X_CARRIAGE_MODE = DXC_AUTO_PARK_MODE
DEFAULT_DUPLICATION_X_OFFSET = 150
```

No se deben cambiar estos parámetros únicamente por ampliar la cama Y.

## Validación obligatoria en máquina

La compilación confirma que el firmware es sintáctica y técnicamente válido para ATmega2560/RUMBA. No puede demostrar recorridos mecánicos físicos.

Antes de usar el área completa:

- comprobar `M119`;
- homing individual X, Y y Z;
- validar Y de forma progresiva;
- comprobar que los cables de cama y termistor no se tensan;
- comprobar que el carro Y no golpea estructura ni motor;
- comprobar aparcamiento de X1/X2;
- confirmar que 295 mm de Y corresponden realmente a superficie imprimible.

## Identificación de la variante

El workflow modifica `Configuration.h` para que el firmware se identifique como una variante personalizada Sirius 300×300, evitando que quede etiquetado como `MoebyusMachines, default config`.
