# Changelog — Sirius 300×300

## v1-custom-300x300

- Base tomada del firmware público `Moebyus/Firmwares` para `SIRIUS11-Rumba-MK8-XYGT2-ZHusillo-lcdFull`.
- Adaptación específica para cama caliente cuadrada de 300×300 mm.
- `Y_MAX_POS` cambiado de 205 mm a 295 mm.
- `X_MAX_POS` conservado en 295 mm.
- `Z_MAX_POS` conservado en 275 mm.
- Conservados `X_MIN_POS=-48`, `Y_MIN_POS=-12`, `Z_MIN_POS=0`.
- Conservada configuración IDEX / DUAL_X_CARRIAGE.
- Conservados pasos/mm, velocidades, aceleraciones, termistores, LCD, EEPROM y protecciones térmicas originales.
- Compatibilidad documentada con BIGTREETECH TMC2209 V1.3 en modo standalone STEP/DIR.
- Añadida compilación automática para RUMBA/ATmega2560.
- Añadidas verificaciones automáticas de geometría y parámetros críticos.
- Firmware compilado: `SIRIUS11-RUMBA-TMC2209-300x300-295x295x275.hex`.

### Pendiente de validación física

- Confirmar recorrido real de Y hasta 295 mm sin colisión ni tensión de cableado.
- Confirmar que toda la zona 295×295 corresponde a superficie realmente imprimible con ambos carros.

No se amplía Z a 290/300 mm mientras no exista una medición mecánica que lo justifique.
