# Firmware Moebyus Sirius 300x300 IDEX

Repositorio de conservación y actualización para una **Moebyus Sirius / SIRIUS11 con cama física 300x300 mm**, electrónica RUMBA/RUMBA+, dos carros X independientes (IDEX), dos extrusores MK8 y Z por husillos.

Contiene dos líneas de firmware separadas. No se deben mezclar sus `Configuration.h`, `Configuration_adv.h` ni HEX.

## 01 - LEGACY Marlin 1.1.1 / Sirius 300x300

Versión de recuperación basada directamente en el firmware público de Moebyus `SIRIUS11-Rumba-MK8-XYGT2-ZHusillo-lcdFull`.

La CI compara el árbol LEGACY con el commit público de Moebyus `36a985e5aaa7ddff14b857c46ebdbf759720c2aa`. La auditoría demostró que el código se conserva sin cambios y que los únicos `#define` activos diferentes en `Configuration.h` son los intencionados:

- identificación de la variante;
- nombre de máquina `[SIRIUS 300]`;
- `Y_MAX_POS`: 205 mm en la publicación Moebyus → 295 mm en esta variante de cama 300x300.

Se conservan del original IDEX, dos extrusores, RUMBA, LCD, SD, EEPROM, pasos, velocidades, aceleraciones, termistores, protecciones térmicas y comportamiento de interfaz. Los TMC2209 actuales trabajan en standalone STEP/DIR; el firmware legacy no controla su corriente por UART.

La compilación auditada para ATmega2560 usa 133154 bytes de flash (52%) y 4951 bytes de RAM (60%).

## 02 - MODERNO Marlin 2.1.2.8 / Sirius 300x300

Migración de la personalidad Sirius al Marlin oficial 2.1.2.8. La CI compara todo el núcleo con el commit upstream `1cd56c4ccd483045eb5a92c99e3ad3b5ab1bea6d`; solo `Configuration.h` y `Configuration_adv.h` contienen la personalización de la máquina.

Configuración principal:

- RUMBA / ATmega2560.
- `TMC2209_STANDALONE` en X, X2, Y, Z, E0 y E1, sin UART de drivers.
- `DUAL_X_CARRIAGE`.
- X1 home a MIN y X2 home a MAX.
- X2: 25..359 mm.
- Auto-Park por defecto.
- Duplicación `M605 S2`, offset 150 mm; espejo `M605 S3` disponible.
- Cama física 300x300 mm; área lógica 295x295x275 mm.
- X=-48..295, Y=-12..295, Z=0..275.
- Termistores T0=5, T1=5, cama=1.
- Protección térmica, watchdog, prevención de extrusión fría, EEPROM, SD y LCD gráfico.
- Funciones históricas recuperadas: babystepping, home individual, speaker, velocidades manuales y comportamiento de encoder originales, menú de información y comprobaciones/reintentos de SD.
- Al abortar una impresión SD no se ejecuta un `G28XY` automático.
- Al terminar una impresión SD no se liberan automáticamente los steppers, como en la Sirius legacy.

La compilación auditada para ATmega2560 usa 146112 bytes de flash (57.5%) y 4848 bytes de RAM (59.2%). El HEX y su SHA256 están versionados dentro de `02-MODERNO.../firmware/`.

## Wi-Fi

**La rama principal no activa Wi-Fi.** La investigación de RUMBA+ confirma que UART3 está disponible en EXP3 y que Marlin puede mantener USB en `SERIAL_PORT 0` y añadir un segundo enlace con `SERIAL_PORT_2 3`. La opción prevista es ESP3D sobre un ESP32, pero se mantiene en una rama independiente para que el firmware base no dependa de ningún módulo Wi-Fi.

La conexión física debe respetar niveles lógicos: no se debe asumir que un ESP32 puede recibir directamente una señal UART de 5 V. La variante Wi-Fi debe documentar alimentación, masa común, cruce TX/RX y adaptación 5 V↔3.3 V antes de conectarla.

## Qué firmware usar

- Recuperación / máxima cercanía al firmware público histórico: `01-LEGACY-MARLIN-1.1.1-CAMA-300x300`.
- Uso actualizado: `02-MODERNO-MARLIN-2.1.2.8-SIRIUS-300x300`.
- Wi-Fi: únicamente la rama específica de ESP3D cuando el hardware esté conectado correctamente.

## Lo que el código NO puede demostrar

La auditoría de GitHub y la compilación no sustituyen una validación mecánica y eléctrica. Antes de imprimir hay que comprobar físicamente:

- `M119` y los cuatro finales XMIN/XMAX/YMIN/ZMIN;
- sentidos X, X2, Y y Z;
- Y progresivamente hasta 295 mm;
- aparcamiento X2 a 359 mm;
- que los cables de cama/termistores no se tensan;
- calentadores y termistores por separado;
- jumpers reales de microstepping 1/16 y Vref de los TMC2209;
- detección física de inserción/retirada de SD.

Tras pasar de Marlin 1.1.1 a 2.1.2.8: `M502`, `M500`, `M503`.

**Este repositorio no afirma que Moebyus publicara de fábrica una Sirius 300x300 con estos límites.** La carpeta LEGACY es una adaptación documentada del firmware público Moebyus y la carpeta MODERNO es su migración controlada a Marlin 2.1.2.8.
