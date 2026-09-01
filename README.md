# Moebyus Sirius 300×300 — firmware personalizado

Este repositorio **NO es el firmware original de fábrica sin modificar**. Es una variante mantenida específicamente para una **Moebyus Sirius / SIRIUS11 fabricada con cama caliente cuadrada de 300×300 mm**.

La base procede del firmware público de Moebyus, pero esta variante adapta el área de trabajo y deja identificada la máquina de forma explícita para evitar confundirla con la Sirius estándar 300×200.

## Máquina objetivo

- Fabricante original: Moebyus
- Familia: Sirius / SIRIUS11
- Electrónica: RUMBA / RUMBA+
- MCU: ATmega2560
- Alimentación: 12 V
- Cama caliente física: **300×300 mm**
- Área lógica configurada: **295×295×275 mm**
- X mínimo mecánico conservado: **-48 mm**
- Y mínimo mecánico conservado: **-12 mm**
- Z mínimo: **0 mm**
- Doble carro X / IDEX
- 2 extrusores MK8
- XY por correa GT2
- Z por husillos
- LCD RepRapDiscount Full Graphic Smart Controller
- Drivers actuales: BIGTREETECH TMC2209 V1.3 en modo standalone STEP/DIR
- Microstepping previsto: 1/16

## Base original

Fuente de partida:

`Moebyus/Firmwares/SIRIUS11/SIRIUS11-Rumba-MK8-XYGT2-ZHusillo-lcdFull`

El código original publicado por Moebyus tenía estos límites:

```text
X_MIN_POS = -48
Y_MIN_POS = -12
Z_MIN_POS = 0
X_MAX_POS = 295
Y_MAX_POS = 205
Z_MAX_POS = 275
```

Ese `Y_MAX_POS=205` corresponde a la configuración publicada para la variante estrecha. Esta rama personalizada cambia **Y_MAX_POS a 295** para la Sirius con cama cuadrada 300×300, manteniendo por ahora X=295 y Z=275.

## Cambios propios de esta variante

1. `Y_MAX_POS`: **205 → 295 mm**.
2. Se conserva `X_MAX_POS=295`.
3. Se conserva `Z_MAX_POS=275` hasta disponer de evidencia mecánica de un recorrido Z mayor.
4. Se conservan los offsets de homing originales `X_MIN_POS=-48` y `Y_MIN_POS=-12`.
5. Se conserva la configuración IDEX original, incluido el segundo carro X y su homing a X-MAX.
6. Se identifica el firmware como **SIRIUS 300x300 CUSTOM** dentro de `Configuration.h`.
7. El CI verifica que placa, límites, IDEX, pasos/mm, sensores y protecciones clave no se alteren accidentalmente.
8. El `.hex` se compila automáticamente para ATmega2560/RUMBA.

## Firmware compilado

Archivo listo para flashear:

`SIRIUS11-RUMBA-TMC2209-300x300-295x295x275.hex`

> El nombre TMC2209 indica el hardware actualmente instalado. Los TMC2209 trabajan en **standalone**, así que Marlin los gobierna mediante STEP/DIR como los drivers anteriores. La corriente no se programa en firmware: se ajusta físicamente mediante Vref.

## Seguridad antes del primer movimiento

El firmware compila y las comprobaciones automáticas validan la configuración lógica. La ampliación de Y de 205 a 295 mm debe verificarse también físicamente en la máquina real.

Antes de ordenar un movimiento hasta Y=295:

1. Hacer `M119` y comprobar todos los finales de carrera.
2. Hacer homing de cada eje por separado.
3. Mover Y primero a 220, 240, 260 y 280 mm observando cables, carro, correa y estructura.
4. Solo después probar 290–295 mm.
5. Confirmar que ambos carros X aparcan correctamente antes de imprimir con IDEX.

## Compilación automática

`.github/workflows/build-firmware.yml`:

- verifica la identidad de esta variante;
- aplica/valida los límites 295×295×275;
- comprueba la configuración crítica de la Sirius;
- instala AVR + U8glib;
- compila para `arduino:avr:mega:cpu=atmega2560`;
- genera el `.hex`;
- publica un artefacto de GitHub Actions;
- conserva el `.hex` actualizado en la raíz del repositorio.

## Documentación

- `VARIANTE-SIRIUS-300x300.md`: ficha técnica y diferencias frente al firmware público.
- `CHANGELOG.md`: historial de esta variante.
- `CambiosPlantillaFirmware-original.txt`: notas originales de Moebyus conservadas como referencia histórica.

## Estado

**Compilación CI: funcional.**

**Configuración lógica objetivo: 295×295×275 mm.**

**Validación mecánica pendiente exclusivamente para confirmar que la máquina real alcanza Y=295 sin colisiones.**
