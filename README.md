# Sirius 300×300 — Firmware personalizado

Firmware para impresora 3D **Moebyus Sirius / SIRIUS11** con:

- Placa RUMBA / RUMBA+
- 12 V
- Doble carro X (IDEX)
- 2 extrusores MK8
- XY por GT2
- Z por husillos
- LCD RepRapDiscount Full Graphic Smart Controller
- Cama física 300×300 mm
- Área de trabajo objetivo inicial: **295×295×275 mm**
- Drivers TMC2209 en modo standalone (STEP/DIR), manteniendo microstepping 1/16

## Base

La base se importa del firmware oficial publicado por Moebyus:
`Moebyus/Firmwares/SIRIUS11/SIRIUS11-Rumba-MK8-XYGT2-ZHusillo-lcdFull`.

## Cambios de esta variante

Se conserva la configuración específica de la Sirius y se modifica el límite Y de 205 mm a 295 mm para aprovechar la cama cuadrada 300×300. X se mantiene en 295 mm y Z en 275 mm hasta validar físicamente un recorrido mayor.

Se conservan los offsets mecánicos originales `X_MIN_POS=-48`, `Y_MIN_POS=-12`, la configuración IDEX y el resto de parámetros originales de Moebyus.

## Compilación

GitHub Actions importa el fuente oficial, aplica los cambios, compila para ATmega2560/RUMBA y publica el `.hex` como artefacto. El workflow también conserva el fuente modificado y el `.hex` generado dentro del repositorio.
