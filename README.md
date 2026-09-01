# Firmware Moebyus Sirius 300x300 IDEX

Este repositorio contiene DOS firmwares distintos para la misma impresora Sirius fabricada por Moebyus con cama caliente física 300x300 mm, electrónica RUMBA/RUMBA+, doble carro X (IDEX), dos extrusores MK8 y Z por husillos.

## Estructura

### 01-LEGACY-MARLIN-1.1.1-CAMA-300x300
Versión de conservación / recuperación basada en el firmware histórico SIRIUS11 de Moebyus (Marlin 1.1.1), adaptado por nosotros a la cama cuadrada.

- Base: código histórico Moebyus SIRIUS11.
- Cambio principal: área lógica X=295, Y=295, Z=275 conservando X_MIN=-48, Y_MIN=-12 y Z_MIN=0.
- Mantiene IDEX, 2 extrusores, RUMBA, LCD, SD y comportamiento original.
- Drivers actuales: TMC2209 instalados en modo standalone; el firmware legacy conserva la lógica de STEP/DIR y microstepping externo.
- Uso: respaldo / recuperación y referencia de configuración original.

### 02-MODERNO-MARLIN-2.1.2.8-SIRIUS-300x300
Migración completa de la personalidad de la Sirius a Marlin 2.1.2.8 estable.

- RUMBA / ATmega2560.
- TMC2209_STANDALONE en X, X2, Y, Z, E0 y E1 (sin UART).
- DUAL_X_CARRIAGE activo.
- X1 home a MIN y X2 home a MAX.
- X2_MIN_POS=25, X2_MAX_POS=359.
- Auto-Park por defecto.
- Duplicación M605 S2 con offset inicial 150 mm.
- Modo espejo M605 S3 disponible.
- Área lógica 295x295x275.
- Termistores T0=5, T1=5, cama=1.
- Protección térmica hotends y cama activa.
- EEPROM, SD y LCD gráfico conservados.

## Qué firmware usar

- Para volver a una base conocida y próxima al firmware histórico: `01-LEGACY-MARLIN-1.1.1-CAMA-300x300`.
- Para la actualización moderna: `02-MODERNO-MARLIN-2.1.2.8-SIRIUS-300x300`.

NO mezclar `Configuration.h`, `Configuration_adv.h` ni HEX entre las dos carpetas.

## Estado de seguridad

Ambos firmwares compilan. La versión moderna ha pasado las comprobaciones de configuración y CI, pero antes de imprimir debe validarse físicamente la máquina: temperaturas en frío, M119, sentido de motores, X2, calentadores/termistores y recorridos progresivos. Tras cambiar de Marlin 1.1.1 a 2.1.2.8 ejecutar M502, M500 y M503 para evitar arrastrar EEPROM antigua.

## Geometría de esta variante

- Cama física: 300x300 mm.
- Área lógica configurada: 295x295 mm.
- Z máximo configurado: 275 mm.
- X: -48 .. 295.
- Y: -12 .. 295.
- Z: 0 .. 275.

Este repositorio NO representa un firmware de fábrica publicado por Moebyus para una Sirius 300x300. Es nuestra variante documentada, construida a partir del código histórico disponible y de la migración posterior a Marlin 2.1.2.8.