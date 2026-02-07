```
 ██████╗  ██████╗ ███╗   ██╗███████╗ █████╗ ██╗     ███████╗███████╗
██╔════╝ ██╔═══██╗████╗  ██║╚══███╔╝██╔══██╗██║     ██╔════╝██╔════╝
██║  ███╗██║   ██║██╔██╗ ██║  ███╔╝ ███████║██║     █████╗  ███████╗
██║   ██║██║   ██║██║╚██╗██║ ███╔╝  ██╔══██║██║     ██╔══╝  ╚════██║
╚██████╔╝╚██████╔╝██║ ╚████║███████╗██║  ██║███████╗███████╗███████║
 ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
```

# Gonzales Speed Monitor for Home Assistant

**Professional internet monitoring, fully integrated with Home Assistant.** One-click installation, comprehensive web dashboard, and 20+ sensors for complete visibility into your connection quality.

**[Deutsche Anleitung weiter unten](#deutsche-anleitung)**

---

## Why Gonzales?

**Transparency & Documentation** — Continuous monitoring creates an objective record of your internet performance. Understand patterns, identify issues early, and have data when you need it.

**Professional Dashboard** — Real-time analytics with historical trends, hourly/daily/weekly breakdowns, per-server comparisons, ISP grading (A+ to F), and 7-day predictive forecasts. Accessible directly from your HA sidebar via Ingress.

**Deep Home Assistant Integration** — 20+ sensors including download, upload, ping, jitter, packet loss, ISP score, smart scheduler status, network health diagnostics, and outage detection. Build automations for notifications, router reboots, failover switching, and more.

**100% Local & Private** — All data stays on your Home Assistant. No cloud accounts, no subscriptions, no external dependencies.

**Developer-Friendly** — REST API with SSE streaming, MCP server for AI assistants, CLI with JSON output.

## Core Features

| Category | Features |
|----------|----------|
| **Installation** | One-click app install, auto-discovery integration, Ingress support (no port forwarding) |
| **Monitoring** | Scheduled tests (15-240 min), 10,000+ Ookla servers, server pinning, real-time progress |
| **Sensors** | Download/upload speed, ping, jitter, packet loss, ISP score, outage binary sensor, diagnostics |
| **Analytics** | Hourly/daily/weekly stats, server comparison, SLA compliance, reliability metrics, trend prediction |
| **Quality Analysis** | ISP grading (A+ to F), QoS profiles (gaming/streaming/video calls), network topology |
| **Detection** | Outage detection (3-strike retry), jitter monitoring, packet loss tracking |
| **Export** | CSV export, PDF reports with charts, unlimited data retention |
| **Automation** | Full sensor integration, binary sensors for triggers, diagnostic entities |
| **Accessibility** | WCAG 2.1 AA compliant, keyboard navigation, screen reader support |

---

## What is Gonzales?

Gonzales is a comprehensive internet monitoring system that:
- Runs automatic speed tests at regular intervals (default: every 60 minutes)
- Provides 20+ sensors for download/upload speeds, ping, jitter, packet loss, ISP quality score, smart scheduling, and network health diagnostics
- Detects internet outages automatically with smart 3-strike retry logic
- Tracks SLA compliance and calculates reliability percentages
- Analyzes QoS requirements for gaming, streaming, and video calls
- Generates professional PDF reports with charts and statistics
- Integrates fully with Home Assistant automations

**No technical knowledge required** — just install and it works!

---

## Quick Start (5 Minutes)

> **Note:** Home Assistant 2026.2+ renamed "Add-ons" to "Apps". This guide uses the new terminology. If you're on an older version, "Apps" = "Add-ons" and "App Store" = "Add-on Store".

### Step 1: Add the Repository

1. Open Home Assistant
2. Go to **Settings** (gear icon in the sidebar)
3. Click **Apps**
4. Click **App Store** (bottom right corner)
5. Click the **three dots** (⋮) in the top right corner
6. Select **Repositories**
7. Paste this URL: `https://github.com/akustikrausch/gonzales-ha`
8. Click **Add**
9. Click **Close**

### Step 2: Install Gonzales

1. Still in the App Store, search for **Gonzales Speed Monitor**
2. Click on it
3. Click **Install** (this may take 1-2 minutes)
4. After installation, click **Start**
5. Turn on **Show in sidebar** (optional but recommended)

### Step 3: Add the Integration (Sensors)

The app runs the speed tests, but you need the **integration** for Home Assistant sensors.

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for **Gonzales**
4. Click on it

**If auto-discovery works:** Click **Submit** — done!

**If auto-discovery fails:** You'll see a form asking for Host and Port. See the next section.

---

## Manual Integration Setup

If auto-discovery doesn't find the app, you need to enter the connection details manually.

### Step 1: Open the App Web Interface

1. Go to **Settings → Apps → Gonzales Speed Monitor**
2. Click **Open Web UI** (or click Gonzales in the sidebar)
3. The Gonzales dashboard opens in your browser

### Step 2: Find Your Slug in the URL

Look at your browser's address bar. You'll see something like:

```
http://homeassistant.local:8123/hassio/addon/546fc077_gonzales/ingress
                                            ^^^^^^^^^^^^^^^^
                                            This is YOUR slug
```

**Your slug is unique to your installation!** Common examples:
- `546fc077_gonzales` — installed from GitHub repository
- `a1b2c3d4_gonzales` — different repository hash
- `local_gonzales` — installed from local folder

### Step 3: Convert Slug to Hostname

Replace underscores `_` with dashes `-`:

| Your URL shows | Enter as Hostname |
|----------------|-------------------|
| `546fc077_gonzales` | `546fc077-gonzales` |
| `local_gonzales` | `local-gonzales` |
| `a1b2c3d4_gonzales` | `a1b2c3d4-gonzales` |

### Step 4: Enter Connection Settings

| Field | Value |
|-------|-------|
| **Host** | Your hostname with dashes (from Step 3) |
| **Port** | Usually `8470` — try `8099` if that doesn't work |
| **API key** | Leave empty |
| **Update interval** | `60` seconds |

### Common Mistakes

| Problem | Solution |
|---------|----------|
| Copied slug with underscore `_` | Must use dash `-` |
| Port doesn't work | Try both `8470` and `8099` |
| Generic hostname like "gonzales" | Use YOUR slug from the URL |
| App not started | Start the app first |

### Still Not Working?

1. **Check if app is running:** Settings → Apps → Gonzales → must show "Running"
2. **Verify your slug:** Open the web UI and check the URL again
3. **Check app logs:** Settings → Apps → Gonzales → Log tab
4. **Try different ports:** `8470`, `8099`, or check app configuration for the port

---

## Configuration (Optional)

You can change settings in two places:

### In Home Assistant App Settings

Go to **Settings → Apps → Gonzales Speed Monitor → Configuration**

| Setting | What it does | Default |
|---------|--------------|---------|
| Test interval | How often to run tests | Every 60 minutes |
| Download threshold | Your internet plan's download speed | 1000 Mbps |
| Upload threshold | Your internet plan's upload speed | 500 Mbps |
| Tolerance | How much slower is still "OK" | 15% |

### In the Gonzales Web Dashboard

Click **Gonzales** in the sidebar, then go to **Settings**. You can run manual tests, change the theme, and see system status.

### In-App Documentation

The web dashboard includes a built-in **Docs** page accessible from the sidebar. It covers all features, configuration options, troubleshooting tips, and Home Assistant integration examples - all without leaving the app.

### Understanding Tolerance

**Example:** You pay for a 1000 Mbps connection.
- With 15% tolerance, speeds above **850 Mbps** show as green (OK)
- Speeds below 850 Mbps show as red (problem)

This is useful because internet speeds normally fluctuate a bit. A measurement of 920 Mbps is fine - no need to alert you.

---

## Sensors in Home Assistant

After setup, you get these sensors automatically:

### Main Sensors

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Download Speed | `sensor.gonzales_download_speed` | Latest download speed in Mbps |
| Upload Speed | `sensor.gonzales_upload_speed` | Latest upload speed in Mbps |
| Ping Latency | `sensor.gonzales_ping_latency` | Ping latency in ms |
| Ping Jitter | `sensor.gonzales_ping_jitter` | Ping jitter in ms |
| Packet Loss | `sensor.gonzales_packet_loss` | Packet loss percentage |
| Last Test Time | `sensor.gonzales_last_test_time` | Timestamp of last speed test |
| ISP Score | `sensor.gonzales_isp_score` | ISP performance score (0-100 points) |

### Diagnostic Sensors

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Scheduler Status | `sensor.gonzales_scheduler_running` | running/stopped |
| Test in Progress | `sensor.gonzales_test_in_progress` | yes/no |
| Uptime | `sensor.gonzales_uptime` | Backend uptime in seconds |
| Total Measurements | `sensor.gonzales_total_measurements` | Total test count |
| Database Size | `sensor.gonzales_db_size` | Database size in bytes |

### Smart Scheduler Sensors (v3.7.0+)

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Smart Scheduler Phase | `sensor.gonzales_smart_scheduler_phase` | Current phase (learning/stable/aggressive) |
| Connection Stability | `sensor.gonzales_smart_scheduler_stability` | Stability score as percentage |
| Smart Scheduler Interval | `sensor.gonzales_smart_scheduler_interval` | Current adaptive interval in minutes |
| Data Budget Used | `sensor.gonzales_smart_scheduler_data_used` | Percentage of monthly data budget used |

### Root Cause Analysis Sensors (v3.7.0+)

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Network Health Score | `sensor.gonzales_network_health_score` | Overall network health (0-100 points) |
| Primary Network Issue | `sensor.gonzales_primary_issue` | Category of main detected issue |
| DNS Health | `sensor.gonzales_dns_health` | DNS layer health score (0-100) |
| Local Network Health | `sensor.gonzales_local_network_health` | Local network score (0-100) |
| ISP Backbone Health | `sensor.gonzales_isp_backbone_health` | ISP backbone score (0-100) |
| ISP Last Mile Health | `sensor.gonzales_isp_lastmile_health` | ISP last mile score (0-100) |

### Binary Sensor

| Sensor | Entity ID | Description |
|--------|-----------|-------------|
| Internet Outage | `binary_sensor.gonzales_internet_outage` | ON when outage detected |

### Button

| Entity | Entity ID | Description |
|--------|-----------|-------------|
| Run Speed Test | `button.gonzales_run_speed_test` | Trigger manual speed test |

Use these sensors in automations, dashboards, or to track your ISP's performance over time.

---

## Services

Gonzales provides two services you can call from automations or the Developer Tools:

| Service | Description |
|---------|-------------|
| `gonzales.run_speedtest` | Trigger a speed test (optional: `entry_id`) |
| `gonzales.set_interval` | Set test interval in minutes 1-1440 (required: `interval`, optional: `entry_id`) |

### Service Examples

**Trigger a speed test from an automation:**
```yaml
automation:
  - alias: "Morning Speed Test"
    trigger:
      - platform: time
        at: "06:00:00"
    action:
      - service: gonzales.run_speedtest
```

**Change the test interval dynamically:**
```yaml
automation:
  - alias: "Test More Often During Peak Hours"
    trigger:
      - platform: time
        at: "18:00:00"
    action:
      - service: gonzales.set_interval
        data:
          interval: 30
```

---

## Using Sensors in Home Assistant Dashboards

### Simple Dashboard Card

Add a quick overview to any dashboard. Go to **Edit Dashboard → Add Card → Entities** and add these:

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
  - entity: sensor.gonzales_isp_score
    name: ISP Score
```

### Gauge Cards for Visual Display

Create eye-catching speed gauges:

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

### History Graph

Track your internet performance over time:

```yaml
type: history-graph
title: Internet Speed History
hours_to_show: 24
entities:
  - entity: sensor.gonzales_download_speed
    name: Download
  - entity: sensor.gonzales_upload_speed
    name: Upload
```

### ApexCharts (Advanced)

If you have [ApexCharts Card](https://github.com/RomRider/apexcharts-card) installed (via HACS):

```yaml
type: custom:apexcharts-card
header:
  title: Speed Trend
  show: true
series:
  - entity: sensor.gonzales_download_speed
    name: Download
    stroke_width: 2
  - entity: sensor.gonzales_upload_speed
    name: Upload
    stroke_width: 2
```

---

## Example: Get Notified When Internet is Slow

Add this automation to get a phone notification when your internet drops below 50 Mbps:

```yaml
automation:
  - alias: "Slow Internet Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.gonzales_download_speed
        below: 50
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "Slow Internet!"
          message: "Download speed is only {{ states('sensor.gonzales_download_speed') }} Mbps"
```

---

## Internet Outage Detection

Gonzales automatically detects internet outages using smart retry logic:

1. **First failure**: Wait 1 minute, retry
2. **Second failure**: Wait 1 minute, retry again
3. **Third consecutive failure**: Outage confirmed!

When an outage is detected, the `binary_sensor.gonzales_internet_outage` turns **ON**.

### Outage Automation Example

```yaml
automation:
  - alias: "Internet Outage Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.gonzales_internet_outage
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "⚠️ Internet Outage!"
          message: "Your internet connection has been down for multiple consecutive tests."
      # Optional: Restart router via smart plug
      - service: switch.turn_off
        entity_id: switch.router_plug
      - delay: "00:00:30"
      - service: switch.turn_on
        entity_id: switch.router_plug

  - alias: "Internet Restored"
    trigger:
      - platform: state
        entity_id: binary_sensor.gonzales_internet_outage
        to: "off"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "✅ Internet Restored"
          message: "Your internet connection is working again."
```

---

## Frequently Asked Questions

### Where is my data stored?
All data stays on your Home Assistant device. Nothing is sent to external servers (except the speed test itself, which connects to Ookla's test servers).

### Can I export my data?
Yes! In the Gonzales dashboard, go to **Export** to download your history as CSV or PDF.

### The speed test shows wrong results
Try setting a specific test server:
1. Open Gonzales dashboard → Settings
2. Look for "Preferred Server ID"
3. Set it to a server near you (you can find IDs at speedtest.net)

### How do I update Gonzales?
Home Assistant updates apps automatically. You can also manually update in **Settings → Apps → Gonzales → Update**.

### My speeds seem lower than expected
Internet speeds can vary based on:
- Time of day (evening = more users = slower)
- WiFi vs wired connection
- Distance to the test server
- Your router's performance

For accurate results, test with a wired connection if possible.

---

## Troubleshooting

### "Web UI not loading"
1. Go to **Settings → Apps → Gonzales**
2. Click **Restart**
3. Wait 30 seconds, then try again

### "Sensors show unavailable"
The sensors need at least one completed test. Wait a few minutes or run a manual test in the dashboard.

### "Speed test keeps failing"
Check the app logs: **Settings → Apps → Gonzales → Log**. Common causes:
- No internet connection
- Firewall blocking the speed test
- Temporary Ookla server issues (try again later)

---

## Advanced: Standalone Integration

If you run Gonzales on a separate device (like a Raspberry Pi), you can still connect it to Home Assistant. See the [Integration Setup Guide](gonzales-addon/DOCS.md#standalone-integration) for details.

---

## What's New in v3.7.0

### Smart Scheduler
- **Adaptive test intervals**: Gonzales learns your connection patterns and adjusts test frequency automatically
- **Three phases**: Learning (collects baseline data), Stable (optimized intervals), Aggressive (frequent tests when issues detected)
- **Data budget**: Set a monthly data limit and the scheduler stays within it
- **Connection stability tracking**: Monitors how stable your connection is over time

### Root Cause Analysis
- **Network health scoring**: Overall health score (0-100) broken down by network layer
- **Automatic issue detection**: Identifies whether problems are in DNS, local network, ISP backbone, or last mile
- **Layer-by-layer diagnostics**: Individual health scores for DNS, local network, ISP backbone, and ISP last mile
- **Primary issue identification**: Pinpoints the most likely cause of network problems

### New Entities
- 4 Smart Scheduler sensors (phase, stability, interval, data budget)
- 6 Root Cause Analysis sensors (health score, primary issue, DNS/local/backbone/last mile health)
- 1 button entity to trigger speed tests directly from Home Assistant
- 2 services (`gonzales.run_speedtest`, `gonzales.set_interval`)

---

## What's New in v3.5.0

### AI Agent Integration
- **MCP Server**: Native integration with Claude Desktop and other MCP-compatible AI tools
- **Summary API**: New `/api/v1/summary` endpoint designed for AI agents and LLMs
- **AGENTS.md**: Machine-readable documentation for AI agents

### Developer Experience
- Improved OpenAPI documentation with examples
- Consistent `--json` output across all CLI commands

## What's New in v3.0.0

### Clean Architecture
- Domain-Driven Design with proper separation of concerns
- Pure Python entities and value objects
- Repository pattern for data access abstraction

### Accessibility (WCAG 2.1 AA)
- Full keyboard navigation
- Screen reader support with ARIA landmarks
- Focus indicators on all interactive elements

### Security
- Rate limiting (100 requests/minute per IP)
- Token bucket algorithm for fair resource distribution

---

## Links

- [Main Gonzales Project](https://github.com/akustikrausch/gonzales) - Full documentation, standalone setup, API reference
- [Report Issues](https://github.com/akustikrausch/gonzales-ha/issues) - Bug reports and feature requests
- [Ookla Terms](https://www.speedtest.net/about/terms) - Speed test provider's terms of use

---

---

# Deutsche Anleitung

## Warum Gonzales?

**Transparenz & Dokumentation** — Kontinuierliches Monitoring erstellt eine objektive Aufzeichnung deiner Internet-Performance. Verstehe Muster, erkenne Probleme frühzeitig und habe Daten, wenn du sie brauchst.

**Professionelles Dashboard** — Echtzeit-Analysen mit historischen Trends, stündlichen/täglichen/wöchentlichen Aufschlüsselungen, Server-Vergleichen, ISP-Bewertung (A+ bis F) und 7-Tage-Vorhersagen. Direkt über die HA-Seitenleiste via Ingress erreichbar.

**Tiefe Home Assistant Integration** — 20+ Sensoren inklusive Download, Upload, Ping, Jitter, Paketverlust, ISP-Score, Smart-Scheduler-Status, Netzwerk-Gesundheitsdiagnose und Ausfallerkennung. Erstelle Automationen für Benachrichtigungen, Router-Neustarts, Failover-Umschaltung und mehr.

**100% Lokal & Privat** — Alle Daten bleiben auf deinem Home Assistant. Keine Cloud-Konten, keine Abos, keine externen Abhängigkeiten.

**Entwicklerfreundlich** — REST API mit SSE-Streaming, MCP-Server für KI-Assistenten, CLI mit JSON-Ausgabe.

## Kernfunktionen

| Kategorie | Funktionen |
|-----------|------------|
| **Installation** | Ein-Klick-App-Installation, Auto-Discovery-Integration, Ingress-Support (kein Port-Forwarding) |
| **Monitoring** | Geplante Tests (15-240 Min), 10.000+ Ookla-Server, Server-Pinning, Echtzeit-Fortschritt |
| **Sensoren** | Download/Upload-Speed, Ping, Jitter, Paketverlust, ISP-Score, Ausfall-Binärsensor, Diagnose |
| **Analysen** | Stündliche/tägliche/wöchentliche Stats, Server-Vergleich, SLA-Compliance, Zuverlässigkeitsmetriken, Trend-Vorhersage |
| **Qualitätsanalyse** | ISP-Bewertung (A+ bis F), QoS-Profile (Gaming/Streaming/Videoanrufe), Netzwerk-Topologie |
| **Erkennung** | Ausfallerkennung (3-Strike-Retry), Jitter-Monitoring, Paketverlust-Tracking |
| **Export** | CSV-Export, PDF-Berichte mit Diagrammen, unbegrenzte Datenaufbewahrung |
| **Automation** | Volle Sensor-Integration, Binary Sensors für Trigger, Diagnose-Entities |
| **Barrierefreiheit** | WCAG 2.1 AA konform, Tastaturnavigation, Screenreader-Unterstützung |

---

## Was ist Gonzales?

Gonzales ist ein umfassendes Internet-Überwachungssystem, das:
- Automatisch regelmäßige Speedtests durchführt (Standard: alle 60 Minuten)
- 20+ Sensoren für Download/Upload, Ping, Jitter, Paketverlust, ISP-Qualitätsbewertung, Smart-Scheduling und Netzwerk-Gesundheitsdiagnose bereitstellt
- Internet-Ausfälle automatisch mit intelligenter 3-Strike-Retry-Logik erkennt
- SLA-Compliance trackt und Zuverlässigkeitsprozente berechnet
- QoS-Anforderungen für Gaming, Streaming und Videoanrufe analysiert
- Professionelle PDF-Berichte mit Diagrammen und Statistiken generiert
- Sich vollständig in Home Assistant Automationen integriert

**Keine technischen Kenntnisse erforderlich** — einfach installieren und es funktioniert!

---

## Schnellstart (5 Minuten)

> **Hinweis:** Home Assistant 2026.2+ hat "Add-ons" in "Apps" umbenannt. Diese Anleitung verwendet die neue Terminologie. Falls du eine ältere Version nutzt: "Apps" = "Add-ons" und "App Store" = "Add-on Store".

### Schritt 1: Repository hinzufügen

1. Öffne Home Assistant
2. Gehe zu **Einstellungen** (Zahnrad-Symbol in der Seitenleiste)
3. Klicke auf **Apps**
4. Klicke auf **App Store** (unten rechts)
5. Klicke auf die **drei Punkte** (⋮) oben rechts
6. Wähle **Repositories**
7. Füge diese URL ein: `https://github.com/akustikrausch/gonzales-ha`
8. Klicke **Hinzufügen**
9. Klicke **Schließen**

### Schritt 2: Gonzales installieren

1. Suche im App Store nach **Gonzales Speed Monitor**
2. Klicke darauf
3. Klicke **Installieren** (kann 1-2 Minuten dauern)
4. Nach der Installation klicke **Starten**
5. Aktiviere **In Seitenleiste anzeigen** (optional aber empfohlen)

### Schritt 3: Integration hinzufügen (Sensoren)

Die App führt die Speedtests durch, aber du brauchst die **Integration** für Home Assistant Sensoren.

1. Gehe zu **Einstellungen → Geräte & Dienste**
2. Klicke **+ Integration hinzufügen** (unten rechts)
3. Suche nach **Gonzales**
4. Klicke darauf

**Wenn Auto-Discovery funktioniert:** Klicke **Absenden** — fertig!

**Wenn Auto-Discovery fehlschlägt:** Du siehst ein Formular für Host und Port. Siehe nächsten Abschnitt.

---

## Manuelle Integration einrichten

Wenn Auto-Discovery die App nicht findet, musst du die Verbindungsdaten manuell eingeben.

### Schritt 1: App Web-Oberfläche öffnen

1. Gehe zu **Einstellungen → Apps → Gonzales Speed Monitor**
2. Klicke **Web-UI öffnen** (oder klicke Gonzales in der Seitenleiste)
3. Das Gonzales Dashboard öffnet sich im Browser

### Schritt 2: Deinen Slug in der URL finden

Schau in die Adresszeile deines Browsers. Du siehst so etwas wie:

```
http://homeassistant.local:8123/hassio/addon/546fc077_gonzales/ingress
                                            ^^^^^^^^^^^^^^^^
                                            Das ist DEIN Slug
```

**Dein Slug ist einzigartig für deine Installation!** Typische Beispiele:
- `546fc077_gonzales` — installiert vom GitHub-Repository
- `a1b2c3d4_gonzales` — anderer Repository-Hash
- `local_gonzales` — installiert aus lokalem Ordner

### Schritt 3: Slug in Hostname umwandeln

Ersetze Unterstriche `_` durch Bindestriche `-`:

| Deine URL zeigt | Als Hostname eingeben |
|-----------------|----------------------|
| `546fc077_gonzales` | `546fc077-gonzales` |
| `local_gonzales` | `local-gonzales` |
| `a1b2c3d4_gonzales` | `a1b2c3d4-gonzales` |

### Schritt 4: Verbindungseinstellungen eingeben

| Feld | Wert |
|------|------|
| **Host** | Dein Hostname mit Bindestrichen (aus Schritt 3) |
| **Port** | Normalerweise `8470` — probiere `8099` falls das nicht funktioniert |
| **API key** | Leer lassen |
| **Update interval** | `60` Sekunden |

### Häufige Fehler

| Problem | Lösung |
|---------|--------|
| Slug mit Unterstrich `_` kopiert | Muss Bindestrich `-` sein |
| Port funktioniert nicht | Probiere sowohl `8470` als auch `8099` |
| Generischer Hostname wie "gonzales" | Nutze DEINEN Slug aus der URL |
| App nicht gestartet | Erst App starten |

### Funktioniert immer noch nicht?

1. **Prüfe ob App läuft:** Einstellungen → Apps → Gonzales → muss "Gestartet" zeigen
2. **Slug nochmal prüfen:** Web-UI öffnen und URL nochmal anschauen
3. **App-Logs prüfen:** Einstellungen → Apps → Gonzales → Log-Tab
4. **Andere Ports probieren:** `8470`, `8099`, oder in der App-Konfiguration nach dem Port schauen

---

## Konfiguration (Optional)

### In den Home Assistant App-Einstellungen

Gehe zu **Einstellungen → Apps → Gonzales Speed Monitor → Konfiguration**

| Einstellung | Was sie bewirkt | Standard |
|-------------|-----------------|----------|
| Test interval | Wie oft Tests laufen | Alle 60 Minuten |
| Download threshold | Download-Geschwindigkeit deines Tarifs | 1000 Mbps |
| Upload threshold | Upload-Geschwindigkeit deines Tarifs | 500 Mbps |
| Tolerance | Wie viel langsamer noch "OK" ist | 15% |

### Toleranz verstehen

**Beispiel:** Du zahlst für eine 1000 Mbps Verbindung.
- Mit 15% Toleranz werden Geschwindigkeiten über **850 Mbps** grün angezeigt (OK)
- Geschwindigkeiten unter 850 Mbps werden rot angezeigt (Problem)

Das ist nützlich, weil Internetgeschwindigkeiten normal etwas schwanken. Eine Messung von 920 Mbps ist in Ordnung.

---

## Sensoren in Home Assistant

Nach der Einrichtung erhältst du diese Sensoren automatisch:

### Hauptsensoren

| Sensor | Entity ID | Beschreibung |
|--------|-----------|--------------|
| Download Speed | `sensor.gonzales_download_speed` | Aktuelle Download-Geschwindigkeit in Mbps |
| Upload Speed | `sensor.gonzales_upload_speed` | Aktuelle Upload-Geschwindigkeit in Mbps |
| Ping Latency | `sensor.gonzales_ping_latency` | Ping-Latenz in ms |
| Ping Jitter | `sensor.gonzales_ping_jitter` | Ping-Jitter in ms |
| Packet Loss | `sensor.gonzales_packet_loss` | Paketverlust in Prozent |
| Last Test Time | `sensor.gonzales_last_test_time` | Zeitstempel des letzten Speedtests |
| ISP Score | `sensor.gonzales_isp_score` | ISP-Leistungsbewertung (0-100 Punkte) |

### Diagnose-Sensoren

| Sensor | Entity ID | Beschreibung |
|--------|-----------|--------------|
| Scheduler Status | `sensor.gonzales_scheduler_running` | running/stopped |
| Test in Progress | `sensor.gonzales_test_in_progress` | yes/no |
| Uptime | `sensor.gonzales_uptime` | Backend-Laufzeit in Sekunden |
| Total Measurements | `sensor.gonzales_total_measurements` | Gesamtanzahl der Tests |
| Database Size | `sensor.gonzales_db_size` | Datenbankgroesse in Bytes |

### Smart-Scheduler-Sensoren (v3.7.0+)

| Sensor | Entity ID | Beschreibung |
|--------|-----------|--------------|
| Smart Scheduler Phase | `sensor.gonzales_smart_scheduler_phase` | Aktuelle Phase (learning/stable/aggressive) |
| Connection Stability | `sensor.gonzales_smart_scheduler_stability` | Stabilitaetsbewertung in Prozent |
| Smart Scheduler Interval | `sensor.gonzales_smart_scheduler_interval` | Aktuelles adaptives Intervall in Minuten |
| Data Budget Used | `sensor.gonzales_smart_scheduler_data_used` | Prozent des monatlichen Datenbudgets verbraucht |

### Root-Cause-Analyse-Sensoren (v3.7.0+)

| Sensor | Entity ID | Beschreibung |
|--------|-----------|--------------|
| Network Health Score | `sensor.gonzales_network_health_score` | Netzwerk-Gesundheitsbewertung (0-100 Punkte) |
| Primary Network Issue | `sensor.gonzales_primary_issue` | Kategorie des erkannten Hauptproblems |
| DNS Health | `sensor.gonzales_dns_health` | DNS-Gesundheitsbewertung (0-100) |
| Local Network Health | `sensor.gonzales_local_network_health` | Lokales Netzwerk Bewertung (0-100) |
| ISP Backbone Health | `sensor.gonzales_isp_backbone_health` | ISP-Backbone-Bewertung (0-100) |
| ISP Last Mile Health | `sensor.gonzales_isp_lastmile_health` | ISP-Last-Mile-Bewertung (0-100) |

### Binaerer Sensor

| Sensor | Entity ID | Beschreibung |
|--------|-----------|--------------|
| Internet Outage | `binary_sensor.gonzales_internet_outage` | AN wenn Ausfall erkannt |

### Button

| Entity | Entity ID | Beschreibung |
|--------|-----------|--------------|
| Run Speed Test | `button.gonzales_run_speed_test` | Manuellen Speedtest ausloesen |

---

## Services (Dienste)

Gonzales bietet zwei Dienste, die du in Automationen oder den Entwicklerwerkzeugen aufrufen kannst:

| Service | Beschreibung |
|---------|--------------|
| `gonzales.run_speedtest` | Speedtest ausloesen (optional: `entry_id`) |
| `gonzales.set_interval` | Testintervall in Minuten setzen, 1-1440 (erforderlich: `interval`, optional: `entry_id`) |

### Service-Beispiele

**Speedtest per Automation ausloesen:**
```yaml
automation:
  - alias: "Morgens Speedtest"
    trigger:
      - platform: time
        at: "06:00:00"
    action:
      - service: gonzales.run_speedtest
```

**Testintervall dynamisch aendern:**
```yaml
automation:
  - alias: "Haeufiger testen zu Stosszeiten"
    trigger:
      - platform: time
        at: "18:00:00"
    action:
      - service: gonzales.set_interval
        data:
          interval: 30
```

---

## Sensoren im Home Assistant Dashboard nutzen

### Einfache Dashboard-Karte

Füge eine schnelle Übersicht zu jedem Dashboard hinzu. Gehe zu **Dashboard bearbeiten → Karte hinzufügen → Entitäten** und füge hinzu:

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
  - entity: sensor.gonzales_isp_score
    name: ISP Bewertung
```

### Gauge-Karten für visuelle Anzeige

Erstelle auffällige Geschwindigkeits-Anzeigen:

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

### Verlaufsgraph

Verfolge deine Internetleistung über Zeit:

```yaml
type: history-graph
title: Internet Geschwindigkeitsverlauf
hours_to_show: 24
entities:
  - entity: sensor.gonzales_download_speed
    name: Download
  - entity: sensor.gonzales_upload_speed
    name: Upload
```

### ApexCharts (Fortgeschritten)

Wenn du [ApexCharts Card](https://github.com/RomRider/apexcharts-card) installiert hast (über HACS):

```yaml
type: custom:apexcharts-card
header:
  title: Geschwindigkeits-Trend
  show: true
series:
  - entity: sensor.gonzales_download_speed
    name: Download
    stroke_width: 2
  - entity: sensor.gonzales_upload_speed
    name: Upload
    stroke_width: 2
```

---

## Beispiel: Benachrichtigung bei langsamem Internet

Füge diese Automation hinzu, um eine Handy-Benachrichtigung zu erhalten, wenn dein Internet unter 50 Mbps fällt:

```yaml
automation:
  - alias: "Langsames Internet Warnung"
    trigger:
      - platform: numeric_state
        entity_id: sensor.gonzales_download_speed
        below: 50
    action:
      - service: notify.mobile_app_dein_handy
        data:
          title: "Langsames Internet!"
          message: "Download-Geschwindigkeit ist nur {{ states('sensor.gonzales_download_speed') }} Mbps"
```

---

## Internet-Ausfall-Erkennung

Gonzales erkennt automatisch Internet-Ausfälle mit intelligenter Retry-Logik:

1. **Erster Fehler**: 1 Minute warten, erneut versuchen
2. **Zweiter Fehler**: 1 Minute warten, nochmal versuchen
3. **Dritter aufeinanderfolgender Fehler**: Ausfall bestätigt!

Bei einem erkannten Ausfall schaltet `binary_sensor.gonzales_internet_outage` auf **ON**.

### Ausfall-Automation Beispiel

```yaml
automation:
  - alias: "Internet Ausfall Warnung"
    trigger:
      - platform: state
        entity_id: binary_sensor.gonzales_internet_outage
        to: "on"
    action:
      - service: notify.mobile_app_dein_handy
        data:
          title: "⚠️ Internet Ausfall!"
          message: "Deine Internetverbindung ist bei mehreren aufeinanderfolgenden Tests ausgefallen."
      # Optional: Router über Smart Plug neustarten
      - service: switch.turn_off
        entity_id: switch.router_steckdose
      - delay: "00:00:30"
      - service: switch.turn_on
        entity_id: switch.router_steckdose

  - alias: "Internet Wiederhergestellt"
    trigger:
      - platform: state
        entity_id: binary_sensor.gonzales_internet_outage
        to: "off"
    action:
      - service: notify.mobile_app_dein_handy
        data:
          title: "✅ Internet Wiederhergestellt"
          message: "Deine Internetverbindung funktioniert wieder."
```

---

## Häufig gestellte Fragen

### Wo werden meine Daten gespeichert?
Alle Daten bleiben auf deinem Home Assistant Gerät. Nichts wird an externe Server gesendet (außer dem Speedtest selbst, der sich mit Ookla's Testservern verbindet).

### Kann ich meine Daten exportieren?
Ja! Im Gonzales Dashboard gehe zu **Export**, um deine Historie als CSV oder PDF herunterzuladen.

### Der Speedtest zeigt falsche Ergebnisse
Versuche einen bestimmten Testserver einzustellen:
1. Öffne Gonzales Dashboard → Settings
2. Suche nach "Preferred Server ID"
3. Stelle einen Server in deiner Nähe ein

### Wie aktualisiere ich Gonzales?
Home Assistant aktualisiert Apps automatisch. Du kannst auch manuell aktualisieren unter **Einstellungen → Apps → Gonzales → Aktualisieren**.

### Meine Geschwindigkeiten scheinen niedriger als erwartet
Internetgeschwindigkeiten können variieren durch:
- Tageszeit (abends = mehr Nutzer = langsamer)
- WLAN vs. Kabelverbindung
- Entfernung zum Testserver
- Leistung deines Routers

Für genaue Ergebnisse teste mit einer Kabelverbindung, wenn möglich.

---

## Problemlösung

### "Web UI lädt nicht"
1. Gehe zu **Einstellungen → Apps → Gonzales**
2. Klicke **Neustart**
3. Warte 30 Sekunden, dann versuche es erneut

### "Sensoren zeigen nicht verfügbar"
Die Sensoren brauchen mindestens einen abgeschlossenen Test. Warte ein paar Minuten oder starte einen manuellen Test im Dashboard.

### "Speedtest schlägt immer fehl"
Prüfe die App-Logs: **Einstellungen → Apps → Gonzales → Log**. Häufige Ursachen:
- Keine Internetverbindung
- Firewall blockiert den Speedtest
- Temporäre Ookla Server-Probleme (später erneut versuchen)

---

## Was ist neu in v3.7.0

### Smart Scheduler
- **Adaptive Testintervalle**: Gonzales lernt deine Verbindungsmuster und passt die Testhaeufigkeit automatisch an
- **Drei Phasen**: Learning (Basisdaten sammeln), Stable (optimierte Intervalle), Aggressive (haeufige Tests bei erkannten Problemen)
- **Datenbudget**: Setze ein monatliches Datenlimit und der Scheduler haelt sich daran
- **Verbindungsstabilitaet**: Ueberwacht wie stabil deine Verbindung ueber die Zeit ist

### Root-Cause-Analyse
- **Netzwerk-Gesundheitsbewertung**: Gesamtbewertung (0-100) aufgeschluesselt nach Netzwerkschicht
- **Automatische Problemerkennung**: Identifiziert ob Probleme bei DNS, lokalem Netzwerk, ISP-Backbone oder Last Mile liegen
- **Schicht-fuer-Schicht-Diagnose**: Einzelne Gesundheitsbewertungen fuer DNS, lokales Netzwerk, ISP-Backbone und ISP-Last-Mile
- **Hauptproblem-Identifikation**: Findet die wahrscheinlichste Ursache von Netzwerkproblemen

### Neue Entities
- 4 Smart-Scheduler-Sensoren (Phase, Stabilitaet, Intervall, Datenbudget)
- 6 Root-Cause-Analyse-Sensoren (Gesundheitsbewertung, Hauptproblem, DNS/Lokal/Backbone/Last-Mile-Gesundheit)
- 1 Button-Entity zum Ausloesen von Speedtests direkt aus Home Assistant
- 2 Services (`gonzales.run_speedtest`, `gonzales.set_interval`)

---

## Was ist neu in v3.5.0

### KI-Agenten Integration
- **MCP Server**: Native Integration mit Claude Desktop und anderen MCP-kompatiblen KI-Tools
- **Summary API**: Neuer `/api/v1/summary` Endpoint für KI-Agenten und LLMs
- **AGENTS.md**: Maschinenlesbare Dokumentation für KI-Agenten

### Entwickler-Erfahrung
- Verbesserte OpenAPI-Dokumentation mit Beispielen
- Konsistente `--json` Ausgabe für alle CLI-Befehle

## Was ist neu in v3.0.0

### Clean Architecture
- Domain-Driven Design mit sauberer Trennung der Verantwortlichkeiten
- Reine Python-Entitäten und Value Objects
- Repository-Pattern für abstrahierten Datenzugriff

### Barrierefreiheit (WCAG 2.1 AA)
- Vollständige Tastaturnavigation
- Screenreader-Unterstützung mit ARIA-Landmarks
- Fokus-Indikatoren auf allen interaktiven Elementen

### Sicherheit
- Rate Limiting (100 Anfragen/Minute pro IP)
- Token-Bucket-Algorithmus für faire Ressourcenverteilung

---

## License / Lizenz

**Gonzales** is MIT licensed. The **Ookla Speedtest CLI** is proprietary third-party software. By using this add-on, you accept the [Ookla EULA](https://www.speedtest.net/about/eula). Personal use is free; commercial use requires a license from Ookla. Speedtest® is a trademark of Ookla, LLC. Not affiliated with Ookla.

**Gonzales** ist MIT-lizenziert. Die **Ookla Speedtest CLI** ist proprietäre Drittanbieter-Software. Mit der Nutzung akzeptierst du die [Ookla EULA](https://www.speedtest.net/about/eula). Persönliche Nutzung kostenlos; kommerzielle Nutzung erfordert Ookla-Lizenz. Speedtest® ist eine Marke von Ookla, LLC. Nicht mit Ookla verbunden.
