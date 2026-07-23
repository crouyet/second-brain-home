# health-receiver — setup (una vez, ~10 min)

Recibe automáticamente sueño/ciclo/medicación desde Health Auto Export, corriendo en segundo plano en tu Mac — sin necesitar que la app del iPhone esté abierta (Apple solo exige que el iPhone se haya desbloqueado en algún momento, no que la app esté al frente).

Ya está corriendo en tu Mac (LaunchAgent instalado). Lo que falta es configurar las "REST API Automations" en la app del iPhone para que le manden los datos.

## Datos de conexión

- **URL**: `http://<YOUR-MAC-LAN-IP>:9001/`
- **Header**: `X-API-Key` → el valor está en `~/.hestia/health-receiver.env` de tu Mac (no lo repito acá, es secreto)

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
