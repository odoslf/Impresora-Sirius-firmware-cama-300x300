# Variante Wi-Fi ESP3D para Sirius / RUMBA+

Esta documentación corresponde **solo** a la rama `wifi-esp3d-uart3`. La rama `main` permanece sin Wi-Fi.

## Decisión técnica

Se recomienda un **ESP32 DevKit / ESP32-WROOM-32** con ESP3D 3.1 antes que un ESP-01 antiguo. ESP3D 3.1 mantiene soporte para ESP8266 y ESP32, y su configuración actual usa `esp32dev` como entorno por defecto. La versión estable publicada por el proyecto en el momento de esta auditoría es 3.1.0.

Referencias públicas:

- ESP3D oficial: https://github.com/luc-github/ESP3D
- RUMBA+ oficial: https://github.com/Aus3D/RUMBA-Plus
- Confirmación UART3/EXP3 de RUMBA+: https://github.com/Aus3D/RUMBA-Plus/issues/11

## Puerto serie correcto de RUMBA+

El desarrollador de RUMBA+ confirma en el issue #11:

- UART0: interfaz USB de la RUMBA+.
- UART1: EXP1.
- UART2: pines compartidos/usados por drivers; no es la elección adecuada.
- UART3: EXP3.
- UART3 RX = PJ0 = pin 11 de EXP3.
- UART3 TX = PJ1 = pin 12 de EXP3.

También confirma que en Marlin la configuración adecuada para mantener el puerto principal y habilitar UART3 como segundo host es:

```cpp
#define SERIAL_PORT 0
#define BAUDRATE 115200
#define SERIAL_PORT_2 3
#define BAUDRATE_2 115200
```

No se activa `BLUETOOTH`. Un usuario del mismo issue confirmó que `SERIAL_PORT_2 3` funcionó y que su problema inicial era un baudrate distinto en el módulo Wi-Fi.

## Qué cambia en esta rama

Únicamente se añade el segundo puerto serie para ESP3D. No se tocan:

- cama 300x300 / área lógica 295x295x275;
- IDEX, X1/X2 o aparcamiento;
- TMC2209 standalone;
- Vref;
- pasos, velocidades o aceleraciones;
- finales de carrera;
- termistores, PID o protecciones térmicas;
- LCD, SD o EEPROM.

El generador `02-MODERNO-MARLIN-2.1.2.8-SIRIUS-300x300/activar_wifi_esp3d.py` reaplica primero la configuración base y después activa solo UART3.

## Cableado lógico

TX y RX siempre se cruzan:

- RUMBA+ UART3 TX (PJ1 / EXP3 pin 12) → adaptación de nivel → RX del ESP32.
- TX del ESP32 → adaptación de nivel → RUMBA+ UART3 RX (PJ0 / EXP3 pin 11).
- GND RUMBA+ ↔ GND ESP32.

### Niveles eléctricos

No conectar a ciegas una salida UART de 5 V a una entrada GPIO de ESP32. El ESP32 usa lógica de 3.3 V. Para una instalación robusta se recomienda un **adaptador de niveles lógicos 5 V ↔ 3.3 V** entre ambas UART, especialmente en RUMBA TX → ESP RX.

### Alimentación

Para un ESP32 DevKit, usar una alimentación 5 V regulada adecuada para la placa (por su pin 5V/VIN o USB, según el modelo concreto), preferiblemente mediante un convertidor DC-DC dedicado desde la fuente de la impresora. Compartir masa con RUMBA+.

No se asume que EXP3 pueda alimentar el ESP32 con margen suficiente hasta verificar el modelo exacto de RUMBA+ y el consumo del módulo. El Wi-Fi produce picos de corriente y una alimentación marginal causa reinicios y desconexiones difíciles de diagnosticar.

## Configuración ESP3D

- Firmware: ESP3D 3.1 estable.
- Baudrate UART hacia Marlin: **115200**.
- Configurar la red Wi-Fi en ESP3D, no en Marlin.
- Probar primero ESP3D por separado y después conectar la UART a RUMBA+.

## Sobre mostrar «Wi-Fi conectado» en el LCD

Esta rama **no muestra un mensaje falso de conexión**. Marlin únicamente sabe que existe un segundo puerto serie; no conoce por sí mismo si el ESP32 está asociado al punto de acceso, si obtuvo IP o si la red funciona.

Para mostrar un estado real habría que implementar un protocolo o notificación explícita ESP3D → Marlin (por ejemplo un G-code enviado solo después de una conexión confirmada). Eso se estudiaría como función adicional y no debe confundirse con la habilitación básica de ESP3D.

## Prueba segura

1. Con ESP32 desconectado de RUMBA+, comprobar la impresora con el firmware Wi-Fi: LCD, `M119`, movimientos y temperaturas deben comportarse igual que `main`.
2. Configurar ESP3D y confirmar su Wi-Fi de forma independiente.
3. Apagar todo antes de cablear UART y masas.
4. Conectar mediante adaptación de nivel y alimentación regulada.
5. Arrancar y verificar que USB sigue respondiendo a 115200.
6. Acceder a ESP3D y enviar primero comandos de solo lectura como `M115`, `M105` y `M119`.
7. Solo después probar movimientos cortos y una impresión de prueba vigilada.

## Estado

Esta rama es opcional. `main` seguirá siendo la referencia de firmware Sirius sin Wi-Fi.
