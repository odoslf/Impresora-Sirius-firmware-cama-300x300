# 01 - LEGACY Marlin 1.1.1 / Sirius 300x300

Esta carpeta contiene nuestra versión de conservación basada en el código histórico SIRIUS11 de Moebyus.

## Identidad
- Base: Marlin 1.1.1 / configuración SIRIUS11 publicada por Moebyus.
- NO es un firmware de fábrica específico 300x300 publicado por Moebyus.
- Nuestra modificación principal adapta la geometría a la cama cuadrada física 300x300.

## Geometría
- X_MIN_POS = -48
- Y_MIN_POS = -12
- Z_MIN_POS = 0
- X_MAX_POS = 295
- Y_MAX_POS = 295
- Z_MAX_POS = 275

## Funciones conservadas
- BOARD_RUMBA.
- ATmega2560.
- 2 extrusores MK8.
- DUAL_X_CARRIAGE / IDEX.
- X1 home a MIN y X2 al lado MAX según la lógica original.
- LCD gráfico RepRapDiscount.
- SD.
- EEPROM.
- Termistores y protecciones térmicas de la configuración Sirius.

## Drivers
La máquina actual usa TMC2209 en modo standalone. Esta rama legacy no usa UART ni control de corriente por software. Vref se ajusta físicamente en los módulos.

## Uso recomendado
Firmware de respaldo, recuperación y referencia para comparar la migración moderna.

El HEX de esta carpeta pertenece exclusivamente a esta versión legacy. No debe confundirse con el HEX de Marlin 2.1.2.8.