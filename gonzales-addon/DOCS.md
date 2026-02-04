# Gonzales Speed Monitor - Documentation

**[Deutsche Dokumentation weiter unten](#deutsche-dokumentation)**

---

## What Does This Add-on Do?

Gonzales automatically tests your internet speed and keeps track of the results. Think of it like having someone check your internet speed every hour and write down the results for you.

**What you get:**
- A dashboard showing your current internet speed
- History of all past speed tests
- Alerts when your internet is slower than it should be
- Statistics to see if your ISP is giving you what you pay for

---

## First Time Setup

After installing the add-on, here's what happens:

1. **First start**: By using this add-on, you agree to the [Ookla Speedtest CLI EULA](https://www.speedtest.net/about/eula) (auto-accepted on first run)
2. **Integration auto-install**: The addon automatically copies the Gonzales integration to your Home Assistant
3. **⚠️ Restart required**: **Restart Home Assistant** for the integration to become available
4. **Integration setup**: Go to **Settings → Devices & Services → Add Integration → Gonzales** and confirm
5. **First test**: Within a few minutes, the first speed test runs
6. **Dashboard access**: Click "Gonzales" in your sidebar to see results

> **Important**: After the first addon start (or after an update), you must **restart Home Assistant** for the integration changes to take effect. The sensors will only appear after this restart.

That's it! Everything else is automatic.

---

## Understanding the Dashboard

### Main Screen (Dashboard)

When you open Gonzales, you see:

- **Download Speed**: How fast you can receive data (streaming, downloads)
- **Upload Speed**: How fast you can send data (video calls, uploads)
- **Ping**: How quickly your connection responds (important for gaming)

**Colors explained:**
- **Green**: Your speed is good (above your threshold)
- **Red**: Your speed is below what you should be getting

### History

Shows all past speed tests in a list. You can:
- See when each test ran
- Filter by date range
- Delete old measurements if needed

### Statistics

Shows averages and trends:
- How your speed varies throughout the day
- Your ISP's overall performance score
- Compliance rate (how often you get the speed you pay for)

### Export

Download your data as:
- **CSV**: For spreadsheets (Excel, Google Sheets)
- **PDF**: For printing or sharing

### Settings

- Change test interval
- Set your expected speeds
- Adjust tolerance
- Choose a specific test server

---

## Configuration Options Explained

### Test Interval (test_interval_minutes)

How often Gonzales runs a speed test.

- **Default**: 60 minutes
- **Range**: 1 to 1440 minutes (1 minute to 24 hours)
- **Recommendation**: 60 minutes is usually enough for most users

**Why not test more often?**
- Speed tests use bandwidth (a few hundred MB each)
- Too frequent tests can affect your normal internet use
- More data doesn't necessarily mean better insights

### Download/Upload Threshold

Enter the speed your ISP promises you.

**Example:**
- Your plan says "1000 Mbps download, 500 Mbps upload"
- Set download_threshold_mbps = 1000
- Set upload_threshold_mbps = 500

**How to find your plan's speed:**
- Check your ISP contract or bill
- Look at your router's admin page
- Contact your ISP

### Tolerance Percent

How much slower than your plan is still acceptable.

**Default**: 15% (meaning 85% of your plan speed is OK)

**Why have tolerance?**
- Internet speeds naturally fluctuate
- Wi-Fi adds some overhead
- Distance to test server matters
- A measurement of 920 Mbps on a 1000 Mbps plan is normal

**Examples:**
| Plan | Tolerance | Minimum OK Speed |
|------|-----------|------------------|
| 1000 Mbps | 15% | 850 Mbps |
| 500 Mbps | 15% | 425 Mbps |
| 100 Mbps | 20% | 80 Mbps |

### Preferred Server ID

Which Ookla test server to use.

- **Default**: 0 (auto-select nearest server)
- **When to change**: If auto-selection picks a bad server

**How to find server IDs:**
1. Go to speedtest.net
2. Click "Change Server"
3. The ID is in the URL when you select a server

### Log Level

How much detail to show in logs.

- **INFO** (default): Normal operation messages
- **DEBUG**: Very detailed (for troubleshooting)
- **WARNING**: Only potential problems
- **ERROR**: Only actual errors

---

## Your Data

### Where is data stored?

All data stays on your Home Assistant device in the `/data/` folder:

| File | What it contains |
|------|------------------|
| `gonzales.db` | All your speed test results |
| `config.json` | Your settings |
| `.api_key` | Security key (auto-generated) |

### Is my data private?

**Yes.** Gonzales does not send your data anywhere except:
- The speed test itself connects to Ookla's servers (to measure speed)
- No analytics, no tracking, no cloud storage

### Can I backup my data?

Yes! The data is stored in `/data/gonzales.db`. You can:
- Use Home Assistant's backup feature (includes add-on data)
- Manually copy the file via SSH or Samba

---

## Troubleshooting

### "The web interface shows a blank page"

1. Go to **Settings → Add-ons → Gonzales**
2. Click **Restart**
3. Wait 30 seconds
4. Clear your browser cache (Ctrl+Shift+R or Cmd+Shift+R)
5. Try again

### "Speed test failed" in the logs

Common causes:
- **No internet**: Check your connection
- **Firewall**: Speed test needs to connect to Ookla servers
- **Ookla servers busy**: Wait and try again
- **Bad server**: Try setting a specific preferred_server_id

### "My speeds are much lower than expected"

Things to check:
1. **WiFi vs Cable**: Wired connections are faster and more reliable
2. **Time of day**: Internet is slower when many people are online (evening)
3. **Router location**: Far from your Home Assistant device?
4. **Other devices**: Are others streaming or downloading?

### "Sensors show unavailable"

The sensors need at least one completed speed test:
1. Open the Gonzales dashboard
2. Click "Run Test" to start a manual test
3. Wait for it to complete
4. Sensors should update within 60 seconds

### "Add-on keeps restarting"

Check the logs for errors:
1. Go to **Settings → Add-ons → Gonzales → Log**
2. Look for error messages
3. Common issues:
   - Corrupted database (delete `gonzales.db` and restart)
   - Out of disk space

---

## Standalone Integration

If you run Gonzales on a separate machine (Raspberry Pi, server, NAS), you can still see the data in Home Assistant.

### Setup

1. Install HACS if you haven't already
2. Add custom repository: `https://github.com/akustikrausch/gonzales-ha`
3. Install the Gonzales integration
4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration → Gonzales**
6. Enter:
   - **Host**: IP address of your Gonzales server (e.g., `192.168.1.50`)
   - **Port**: `8099` (default Gonzales port)
   - **API Key**: If you set one on the server (optional)

### Difference from Add-on

| Feature | Add-on | Standalone Integration |
|---------|--------|------------------------|
| Speed tests | Runs on HA device | Runs on separate device |
| Dashboard | In HA sidebar | On the separate device |
| Sensors | Yes | Yes |
| Data storage | On HA device | On separate device |

---

## Using Sensors in Home Assistant Dashboards

Gonzales creates these sensors in Home Assistant:

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Download Speed | `sensor.gonzales_download_speed` | Latest download in Mbps |
| Upload Speed | `sensor.gonzales_upload_speed` | Latest upload in Mbps |
| Ping | `sensor.gonzales_ping_latency` | Latency in ms |
| Jitter | `sensor.gonzales_ping_jitter` | Jitter in ms |
| Packet Loss | `sensor.gonzales_packet_loss` | Packet loss % |
| ISP Score | `sensor.gonzales_isp_score` | Overall rating 0-100 |
| Last Test | `sensor.gonzales_last_test_time` | Timestamp of last test |

### Dashboard Examples

**Entities Card:**
```yaml
type: entities
title: Internet Speed
entities:
  - entity: sensor.gonzales_download_speed
    name: Download
  - entity: sensor.gonzales_upload_speed
    name: Upload
  - entity: sensor.gonzales_ping_latency
    name: Ping
```

**Gauge Card:**
```yaml
type: gauge
entity: sensor.gonzales_download_speed
name: Download Speed
min: 0
max: 1000
severity:
  green: 850
  yellow: 500
  red: 0
```

**History Graph:**
```yaml
type: history-graph
title: Speed History
hours_to_show: 24
entities:
  - sensor.gonzales_download_speed
  - sensor.gonzales_upload_speed
```

### Automation Examples

**Notify when internet is slow:**
```yaml
automation:
  - alias: "Slow Internet Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.gonzales_download_speed
      below: 100
    action:
      service: notify.mobile_app_your_phone
      data:
        title: "Slow Internet"
        message: "Speed: {{ states('sensor.gonzales_download_speed') }} Mbps"
```

**Daily speed report:**
```yaml
automation:
  - alias: "Daily Speed Report"
    trigger:
      platform: time
      at: "08:00:00"
    action:
      service: notify.mobile_app_your_phone
      data:
        title: "Daily Internet Report"
        message: >
          Download: {{ states('sensor.gonzales_download_speed') }} Mbps
          Upload: {{ states('sensor.gonzales_upload_speed') }} Mbps
          ISP Score: {{ states('sensor.gonzales_isp_score') }}
```

---

## Technical Details (Advanced)

### Architecture

```
Browser → Home Assistant → Ingress Proxy → Gonzales (port 8099)
                                              ↓
                              FastAPI + SQLite + Scheduler
                                              ↓
                              Ookla Speedtest CLI
```

### Accessibility

Gonzales is designed to be accessible to all users:

- **Keyboard Navigation**: All features accessible via keyboard
- **Screen Reader Support**: ARIA landmarks and live regions
- **Focus Indicators**: Clear visual feedback for keyboard users
- **Reduced Motion**: Respects system preference for reduced animations

**Keyboard Shortcuts:**
- `Tab` / `Shift+Tab`: Navigate between elements
- `Enter` / `Space`: Activate buttons and links
- Skip link available at page top for quick navigation

### Security

- **API Key**: Auto-generated on first start, stored in `/data/.api_key`
- **Rate Limiting**: 100 requests per minute per IP address
- **AppArmor**: Restrictive profile limits container access
- **No open ports**: Web UI only accessible through Home Assistant Ingress
- **No external dependencies**: Everything runs locally

### Performance

- Memory: ~100-200 MB during speed tests
- Disk: ~50 KB per test (database grows slowly)
- Network: Uses your full bandwidth during tests (2-3 minutes)

---

---

# Deutsche Dokumentation

## Was macht dieses Add-on?

Gonzales testet automatisch deine Internetgeschwindigkeit und speichert die Ergebnisse. Stell es dir vor wie einen Assistenten, der jede Stunde dein Internet prüft und die Ergebnisse aufschreibt.

**Was du bekommst:**
- Ein Dashboard mit deiner aktuellen Internetgeschwindigkeit
- Historie aller vergangenen Speedtests
- Warnungen, wenn dein Internet langsamer ist als es sein sollte
- Statistiken, um zu sehen, ob dein Anbieter liefert, was du bezahlst

---

## Erste Einrichtung

Nach der Installation passiert Folgendes:

1. **Erster Start**: Mit der Nutzung dieses Add-ons akzeptierst du die [Ookla Speedtest CLI EULA](https://www.speedtest.net/about/eula) (wird beim ersten Start automatisch akzeptiert)
2. **Integration Auto-Install**: Das Addon kopiert automatisch die Gonzales-Integration in dein Home Assistant
3. **⚠️ Neustart erforderlich**: **Starte Home Assistant neu**, damit die Integration verfügbar wird
4. **Integration einrichten**: Gehe zu **Einstellungen → Geräte & Dienste → Integration hinzufügen → Gonzales** und bestätige
5. **Erster Test**: Innerhalb weniger Minuten läuft der erste Speedtest
6. **Dashboard**: Klicke auf "Gonzales" in deiner Seitenleiste

> **Wichtig**: Nach dem ersten Addon-Start (oder nach einem Update) musst du **Home Assistant neu starten**, damit die Integration-Änderungen wirksam werden. Die Sensoren erscheinen erst nach diesem Neustart.

Das war's! Alles andere läuft automatisch.

---

## Das Dashboard verstehen

### Hauptbildschirm (Dashboard)

Wenn du Gonzales öffnest, siehst du:

- **Download-Geschwindigkeit**: Wie schnell du Daten empfangen kannst (Streaming, Downloads)
- **Upload-Geschwindigkeit**: Wie schnell du Daten senden kannst (Videoanrufe, Uploads)
- **Ping**: Wie schnell deine Verbindung reagiert (wichtig fürs Gaming)

**Farben erklärt:**
- **Grün**: Deine Geschwindigkeit ist gut (über deinem Schwellwert)
- **Rot**: Deine Geschwindigkeit ist unter dem, was du bekommen solltest

### History (Verlauf)

Zeigt alle vergangenen Speedtests in einer Liste. Du kannst:
- Sehen, wann jeder Test lief
- Nach Datum filtern
- Alte Messungen löschen

### Statistics (Statistiken)

Zeigt Durchschnitte und Trends:
- Wie deine Geschwindigkeit über den Tag variiert
- Gesamtbewertung deines Anbieters
- Compliance-Rate (wie oft du die bezahlte Geschwindigkeit bekommst)

### Export

Lade deine Daten herunter als:
- **CSV**: Für Tabellenkalkulationen (Excel, Google Sheets)
- **PDF**: Zum Drucken oder Teilen

### Settings (Einstellungen)

- Testintervall ändern
- Erwartete Geschwindigkeiten einstellen
- Toleranz anpassen
- Bestimmten Testserver wählen

---

## Konfigurationsoptionen erklärt

### Testintervall (test_interval_minutes)

Wie oft Gonzales einen Speedtest durchführt.

- **Standard**: 60 Minuten
- **Bereich**: 1 bis 1440 Minuten (1 Minute bis 24 Stunden)
- **Empfehlung**: 60 Minuten reicht für die meisten Nutzer aus

**Warum nicht öfter testen?**
- Speedtests verbrauchen Bandbreite (einige hundert MB pro Test)
- Zu häufige Tests können deine normale Internetnutzung beeinflussen
- Mehr Daten bedeuten nicht unbedingt bessere Erkenntnisse

### Download/Upload Schwellwert

Trage die Geschwindigkeit ein, die dein Anbieter verspricht.

**Beispiel:**
- Dein Tarif sagt "1000 Mbit/s Download, 500 Mbit/s Upload"
- Setze download_threshold_mbps = 1000
- Setze upload_threshold_mbps = 500

**Wie findest du die Geschwindigkeit deines Tarifs:**
- Schau in deinen Vertrag oder auf die Rechnung
- Sieh in die Admin-Seite deines Routers
- Frag deinen Anbieter

### Toleranz in Prozent

Wie viel langsamer als dein Tarif noch akzeptabel ist.

**Standard**: 15% (bedeutet 85% deiner Tarifgeschwindigkeit ist OK)

**Warum Toleranz?**
- Internetgeschwindigkeiten schwanken natürlich
- WLAN hat etwas Overhead
- Entfernung zum Testserver spielt eine Rolle
- Eine Messung von 920 Mbps bei einem 1000 Mbps Tarif ist normal

**Beispiele:**
| Tarif | Toleranz | Minimale OK-Geschwindigkeit |
|-------|----------|----------------------------|
| 1000 Mbps | 15% | 850 Mbps |
| 500 Mbps | 15% | 425 Mbps |
| 100 Mbps | 20% | 80 Mbps |

### Bevorzugter Server (preferred_server_id)

Welchen Ookla-Testserver verwenden.

- **Standard**: 0 (automatisch nächsten Server wählen)
- **Wann ändern**: Wenn die Automatik einen schlechten Server wählt

**Wie finde ich Server-IDs:**
1. Gehe zu speedtest.net
2. Klicke auf "Server ändern"
3. Die ID steht in der URL, wenn du einen Server auswählst

---

## Deine Daten

### Wo werden Daten gespeichert?

Alle Daten bleiben auf deinem Home Assistant Gerät im `/data/` Ordner:

| Datei | Was sie enthält |
|-------|-----------------|
| `gonzales.db` | Alle deine Speedtest-Ergebnisse |
| `config.json` | Deine Einstellungen |
| `.api_key` | Sicherheitsschlüssel (automatisch generiert) |

### Sind meine Daten privat?

**Ja.** Gonzales sendet deine Daten nirgendwohin außer:
- Der Speedtest selbst verbindet sich mit Ooklas Servern (um Geschwindigkeit zu messen)
- Keine Analysen, kein Tracking, keine Cloud-Speicherung

### Kann ich meine Daten sichern?

Ja! Die Daten sind in `/data/gonzales.db` gespeichert. Du kannst:
- Home Assistants Backup-Funktion nutzen (beinhaltet Add-on Daten)
- Die Datei manuell per SSH oder Samba kopieren

---

## Problemlösung

### "Die Weboberfläche zeigt eine leere Seite"

1. Gehe zu **Einstellungen → Add-ons → Gonzales**
2. Klicke **Neustart**
3. Warte 30 Sekunden
4. Leere deinen Browser-Cache (Strg+Umschalt+R oder Cmd+Shift+R)
5. Versuche es erneut

### "Speedtest fehlgeschlagen" in den Logs

Häufige Ursachen:
- **Kein Internet**: Prüfe deine Verbindung
- **Firewall**: Speedtest muss sich mit Ookla-Servern verbinden können
- **Ookla-Server ausgelastet**: Warte und versuche es später
- **Schlechter Server**: Versuche eine bestimmte preferred_server_id einzustellen

### "Meine Geschwindigkeiten sind viel niedriger als erwartet"

Dinge zum Prüfen:
1. **WLAN vs Kabel**: Kabelverbindungen sind schneller und zuverlässiger
2. **Tageszeit**: Internet ist langsamer, wenn viele online sind (abends)
3. **Router-Position**: Weit weg von deinem Home Assistant Gerät?
4. **Andere Geräte**: Streamen oder laden andere gerade herunter?

### "Sensoren zeigen nicht verfügbar"

Die Sensoren brauchen mindestens einen abgeschlossenen Speedtest:
1. Öffne das Gonzales Dashboard
2. Klicke "Run Test" um einen manuellen Test zu starten
3. Warte bis er fertig ist
4. Sensoren sollten sich innerhalb von 60 Sekunden aktualisieren

### "Add-on startet immer wieder neu"

Prüfe die Logs auf Fehler:
1. Gehe zu **Einstellungen → Add-ons → Gonzales → Log**
2. Suche nach Fehlermeldungen
3. Häufige Probleme:
   - Beschädigte Datenbank (lösche `gonzales.db` und starte neu)
   - Kein Speicherplatz mehr

---

## Eigenständige Integration (Standalone)

Wenn du Gonzales auf einem separaten Gerät betreibst (Raspberry Pi, Server, NAS), kannst du die Daten trotzdem in Home Assistant sehen.

### Einrichtung

1. Installiere HACS falls noch nicht geschehen
2. Füge Custom Repository hinzu: `https://github.com/akustikrausch/gonzales-ha`
3. Installiere die Gonzales Integration
4. Starte Home Assistant neu
5. Gehe zu **Einstellungen → Geräte & Dienste → Integration hinzufügen → Gonzales**
6. Gib ein:
   - **Host**: IP-Adresse deines Gonzales-Servers (z.B. `192.168.1.50`)
   - **Port**: `8099` (Standard-Gonzales-Port)
   - **API Key**: Falls du einen auf dem Server gesetzt hast (optional)

### Unterschied zum Add-on

| Funktion | Add-on | Eigenständige Integration |
|----------|--------|---------------------------|
| Speedtests | Laufen auf HA-Gerät | Laufen auf separatem Gerät |
| Dashboard | In HA-Seitenleiste | Auf dem separaten Gerät |
| Sensoren | Ja | Ja |
| Datenspeicherung | Auf HA-Gerät | Auf separatem Gerät |

---

## Sensoren im Home Assistant Dashboard nutzen

Gonzales erstellt diese Sensoren in Home Assistant:

| Sensor | Entity ID | Beschreibung |
|--------|-----------|--------------|
| Download Speed | `sensor.gonzales_download_speed` | Aktueller Download in Mbps |
| Upload Speed | `sensor.gonzales_upload_speed` | Aktueller Upload in Mbps |
| Ping | `sensor.gonzales_ping_latency` | Latenz in ms |
| Jitter | `sensor.gonzales_ping_jitter` | Jitter in ms |
| Packet Loss | `sensor.gonzales_packet_loss` | Paketverlust % |
| ISP Score | `sensor.gonzales_isp_score` | Gesamtbewertung 0-100 |
| Letzter Test | `sensor.gonzales_last_test_time` | Zeitstempel des letzten Tests |

### Dashboard-Beispiele

**Entitäten-Karte:**
```yaml
type: entities
title: Internet Geschwindigkeit
entities:
  - entity: sensor.gonzales_download_speed
    name: Download
  - entity: sensor.gonzales_upload_speed
    name: Upload
  - entity: sensor.gonzales_ping_latency
    name: Ping
```

**Gauge-Karte:**
```yaml
type: gauge
entity: sensor.gonzales_download_speed
name: Download Speed
min: 0
max: 1000
severity:
  green: 850
  yellow: 500
  red: 0
```

**Verlaufsgraph:**
```yaml
type: history-graph
title: Geschwindigkeitsverlauf
hours_to_show: 24
entities:
  - sensor.gonzales_download_speed
  - sensor.gonzales_upload_speed
```

### Automations-Beispiele

**Benachrichtigung bei langsamem Internet:**
```yaml
automation:
  - alias: "Langsames Internet Warnung"
    trigger:
      platform: numeric_state
      entity_id: sensor.gonzales_download_speed
      below: 100
    action:
      service: notify.mobile_app_dein_handy
      data:
        title: "Langsames Internet"
        message: "Geschwindigkeit: {{ states('sensor.gonzales_download_speed') }} Mbps"
```

**Täglicher Geschwindigkeitsbericht:**
```yaml
automation:
  - alias: "Täglicher Internet-Bericht"
    trigger:
      platform: time
      at: "08:00:00"
    action:
      service: notify.mobile_app_dein_handy
      data:
        title: "Täglicher Internet-Bericht"
        message: >
          Download: {{ states('sensor.gonzales_download_speed') }} Mbps
          Upload: {{ states('sensor.gonzales_upload_speed') }} Mbps
          ISP Score: {{ states('sensor.gonzales_isp_score') }}
```

---

## Technische Details (Fortgeschritten)

### Architektur

```
Browser → Home Assistant → Ingress Proxy → Gonzales (Port 8099)
                                              ↓
                              FastAPI + SQLite + Scheduler
                                              ↓
                              Ookla Speedtest CLI
```

### Barrierefreiheit

Gonzales ist für alle Nutzer zugänglich gestaltet:

- **Tastaturnavigation**: Alle Funktionen per Tastatur erreichbar
- **Screenreader-Unterstützung**: ARIA-Landmarks und Live-Regionen
- **Fokus-Indikatoren**: Klare visuelle Rückmeldung für Tastaturnutzer
- **Reduzierte Bewegung**: Respektiert Systemeinstellung für weniger Animationen

**Tastaturkürzel:**
- `Tab` / `Shift+Tab`: Zwischen Elementen navigieren
- `Enter` / `Leertaste`: Schaltflächen und Links aktivieren
- Skip-Link am Seitenanfang für schnelle Navigation

### Sicherheit

- **API-Schlüssel**: Automatisch beim ersten Start generiert, gespeichert in `/data/.api_key`
- **Rate Limiting**: 100 Anfragen pro Minute pro IP-Adresse
- **AppArmor**: Restriktives Profil begrenzt Container-Zugriff
- **Keine offenen Ports**: Web-UI nur über Home Assistant Ingress erreichbar
- **Keine externen Abhängigkeiten**: Alles läuft lokal

### Leistung

- Speicher: ~100-200 MB während Speedtests
- Festplatte: ~50 KB pro Test (Datenbank wächst langsam)
- Netzwerk: Nutzt deine volle Bandbreite während Tests (2-3 Minuten)

---

## License / Lizenz

**Gonzales** is MIT licensed open source software.

**Ookla Speedtest CLI** is proprietary third-party software by Ookla, LLC. By using this add-on, you accept the [Ookla Speedtest CLI EULA](https://www.speedtest.net/about/eula):
- Personal, non-commercial use: Permitted
- Commercial use: Requires separate license from Ookla
- The CLI is downloaded from Ookla's servers during add-on installation

Speedtest® is a registered trademark of Ookla, LLC. This project is not affiliated with or endorsed by Ookla.

---

**Gonzales** ist MIT-lizenzierte Open-Source-Software.

**Ookla Speedtest CLI** ist proprietäre Drittanbieter-Software von Ookla, LLC. Mit der Nutzung dieses Add-ons akzeptierst du die [Ookla Speedtest CLI EULA](https://www.speedtest.net/about/eula):
- Persönliche, nicht-kommerzielle Nutzung: Erlaubt
- Kommerzielle Nutzung: Erfordert separate Lizenz von Ookla
- Die CLI wird während der Add-on-Installation von Ookla-Servern heruntergeladen

Speedtest® ist eine eingetragene Marke von Ookla, LLC. Dieses Projekt ist nicht mit Ookla verbunden oder von Ookla unterstützt.
