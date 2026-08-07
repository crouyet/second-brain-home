# health-receiver — setup (una vez, ~10 min)

Recibe automáticamente sueño/ciclo/medicación desde Health Auto Export, corriendo en segundo plano en tu Mac — sin necesitar que la app del iPhone esté abierta (Apple solo exige que el iPhone se haya desbloqueado en algún momento, no que la app esté al frente).

Ya está corriendo en tu Mac (LaunchAgent instalado). Lo que falta es configurar las "REST API Automations" en la app del iPhone para que le manden los datos.

## Datos de conexión

- **URL**: `http://<YOUR-MAC-LAN-IP>:9001/`
- **Header**: `X-API-Key` → el valor está en `~/.hestia/health-receiver.env` de tu Mac (no lo repito acá, es secreto)

## Qué protege esto y qué no (leelo antes de activarlo)

El receiver abre un puerto en tu red local. La API key es todo el auth que hay:

- **Protege** contra que alguien de tu red te escriba datos de salud falsos (sin la key, 401).
- **No protege** el tráfico: es HTTP plano, **sin TLS**. Quien esté en la misma WiFi y sepa mirar
  puede leer lo que manda el iPhone. La app no maneja bien certificados self-signed, así que si tu
  red no es de confianza el camino es un reverse proxy con TLS adelante — no cambia nada de acá.
- Los datos quedan **en claro en el disco** de la Mac, en `vault/Raw/health/` (directorio `700`, solo
  tu usuario). Nunca se commitean: están en `.gitignore`.
- Esos archivos los leen **rutinas autónomas** de Claude, sin nadie mirando. Por eso el receiver
  rechaza con `400` cualquier body que no sea JSON válido: texto libre en el vault sería una vía
  directa para meterle instrucciones a un agente.

Las dos perillas, ambas opcionales en `~/.hestia/health-receiver.env`:

```
ALLOW_CIDR=192.168.1.0/24   # solo acepta requests de tu red; el resto, 403
BIND=0.0.0.0                # default; 127.0.0.1 solo si probás desde la misma Mac
```

Para `ALLOW_CIDR` usá la subred de tu casa: corré `ipconfig getifaddr en0` y reemplazá el último
número por `0/24` (ej. IP `192.168.1.37` → `192.168.1.0/24`).

Si nada de esto te cierra, **no hace falta usar Apple Health**: en `/setup` podés elegir
`manual-notion` para mood, ciclo, sueño y medicación, y cargar esas señales a mano.

## Crear las automations en la app

Repetí esto **3 veces** (una por cada tipo de dato — la app solo permite un tipo por automation):

1. Health Auto Export → Automated Exports → **New Automation** → tipo **REST API**.
2. Nombre: `cycle-tracking` / `medications` / `sleep` (uno por automation, así se guardan en archivos separados).
3. **URL**: `http://<YOUR-MAC-LAN-IP>:9001/`
4. **HTTP Headers** → Add Headers → key `X-API-Key`, value: el que está en `~/.hestia/health-receiver.env` (copialo del archivo, no te lo mando por acá).
5. **Data Type**:
   - Automation 1 → **Cycle Tracking**
   - Automation 2 → **Medications** (requiere iOS 26+, ya lo tenés)
   - Automation 3 → **Health Metrics** → seleccioná solo **Sleep Analysis** (no selecciones "todas las métricas", tira demasiado dato y puede fallar en background)

<img width="275" alt="image" src="https://github.com/user-attachments/assets/c443914f-02f4-45c1-86ad-27f6722785dc" />

6. **Export Format**: JSON
7. **Date Range**: `Since Last Sync` (manda solo lo nuevo cada vez)
8. **Sync Cadence**: cada 6 horas está bien (no hace falta más seguido)
9. Guardá y **activá** (toggle ON) cada una.
10. Agregá el **widget "Automations"** a tu pantalla de inicio ([[Atajos Apple]] ya lo menciona) — ayuda a que iOS le dé más tiempo de background al sync.

## Probar

En la app, abrí una automation y tocá **Manual Export** una vez — así confirmás que llega. En tu Mac:

```
cat "$VAULT_ROOT"/vault/Raw/health/cycle-tracking.json
```

Si aparece un JSON con datos, está andando.

## Si la Mac cambia de IP

Las Macs en WiFi doméstico a veces cambian de IP. Si dejan de llegar datos, corré esto para ver la IP actual:

```
ipconfig getifaddr en0
```

Y actualizá la URL en las 3 automations de la app.
