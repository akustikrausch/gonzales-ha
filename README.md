```
 ██████╗  ██████╗ ███╗   ██╗███████╗ █████╗ ██╗     ███████╗███████╗
██╔════╝ ██╔═══██╗████╗  ██║╚══███╔╝██╔══██╗██║     ██╔════╝██╔════╝
██║  ███╗██║   ██║██╔██╗ ██║  ███╔╝ ███████║██║     █████╗  ███████╗
██║   ██║██║   ██║██║╚██╗██║ ███╔╝  ██╔══██║██║     ██╔══╝  ╚════██║
╚██████╔╝╚██████╔╝██║ ╚████║███████╗██║  ██║███████╗███████╗███████║
 ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
```

# Gonzales Speed Monitor for Home Assistant

**Professional internet monitoring, fully integrated with Home Assistant.** One-click installation, comprehensive web dashboard, and 10+ sensors for complete visibility into your connection quality.

**[Deutsche Anleitung weiter unten](#deutsche-anleitung)**

---

## Why Gonzales?

**Transparency & Documentation** — Continuous monitoring creates an objective record of your internet performance. Understand patterns, identify issues early, and have data when you need it.

**Professional Dashboard** — Real-time analytics with historical trends, hourly/daily/weekly breakdowns, per-server comparisons, ISP grading (A+ to F), and 7-day predictive forecasts. Accessible directly from your HA sidebar via Ingress.

**Deep Home Assistant Integration** — 10+ sensors including download, upload, ping, jitter, packet loss, ISP score, and outage detection. Build automations for notifications, router reboots, failover switching, and more.

**100% Local & Private** — All data stays on your Home Assistant. No cloud accounts, no subscriptions, no external dependencies.

**Developer-Friendly** — REST API with SSE streaming, MCP server for AI assistants, CLI with JSON output.

## Core Features

| Category | Features |
|----------|----------|
| **Installation** | One-click add-on install, auto-discovery integration, Ingress support (no port forwarding) |
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
- Provides 10+ sensors for download/upload speeds, ping, jitter, packet loss, and ISP quality score
- Detects internet outages automatically with smart 3-strike retry logic
- Tracks SLA compliance and calculates reliability percentages
- Analyzes QoS requirements for gaming, streaming, and video calls
- Generates professional PDF reports with charts and statistics
- Integrates fully with Home Assistant automations

**No technical knowledge required** — just install and it works!

---

## Quick Start (5 Minutes)

### Step 1: Add the Repository

1. Open Home Assistant
2. Go to **Settings** (gear icon in the sidebar)
3. Click **Add-ons**
4. Click **Add-on Store** (bottom right corner)
5. Click the **three dots** (⋮) in the top right corner
6. Select **Repositories**
7. Paste this URL: `https://github.com/akustikrausch/gonzales-ha`
8. Click **Add**
9. Click **Close**

### Step 2: Install Gonzales

1. Still in the Add-on Store, search for **Gonzales Speed Monitor**
2. Click on it
3. Click **Install** (this may take 1-2 minutes)
4. After installation, click **Start**
5. Turn on **Show in sidebar** (optional but recommended)

### Step 3: You're Done!

Click **Gonzales** in your sidebar to see the dashboard. The first speed test runs automatically within a few minutes.

A notification will appear asking to set up the integration - click **Configure** to add speed sensors to Home Assistant.

---

## Configuration (Optional)

You can change settings in two places:

### In Home Assistant Add-on Settings

Go to **Settings → Add-ons → Gonzales Speed Monitor → Configuration**

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

| Sensor | What it shows |
|--------|---------------|
| Download Speed | Your latest download speed in Mbps |
| Upload Speed | Your latest upload speed in Mbps |
| Ping | How fast your connection responds (lower = better) |
| ISP Score | Overall rating of your internet (0-100) |
| Last Test Time | When the last test ran |
| Internet Outage | Binary sensor: ON if outage detected |

Use these sensors in automations, dashboards, or to track your ISP's performance over time.

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
Home Assistant updates add-ons automatically. You can also manually update in **Settings → Add-ons → Gonzales → Update**.

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
1. Go to **Settings → Add-ons → Gonzales**
2. Click **Restart**
3. Wait 30 seconds, then try again

### "Sensors show unavailable"
The sensors need at least one completed test. Wait a few minutes or run a manual test in the dashboard.

### "Speed test keeps failing"
Check the add-on logs: **Settings → Add-ons → Gonzales → Log**. Common causes:
- No internet connection
- Firewall blocking the speed test
- Temporary Ookla server issues (try again later)

---

## Advanced: Standalone Integration

If you run Gonzales on a separate device (like a Raspberry Pi), you can still connect it to Home Assistant. See the [Integration Setup Guide](gonzales-addon/DOCS.md#standalone-integration) for details.

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

**Tiefe Home Assistant Integration** — 10+ Sensoren inklusive Download, Upload, Ping, Jitter, Paketverlust, ISP-Score und Ausfallerkennung. Erstelle Automationen für Benachrichtigungen, Router-Neustarts, Failover-Umschaltung und mehr.

**100% Lokal & Privat** — Alle Daten bleiben auf deinem Home Assistant. Keine Cloud-Konten, keine Abos, keine externen Abhängigkeiten.

**Entwicklerfreundlich** — REST API mit SSE-Streaming, MCP-Server für KI-Assistenten, CLI mit JSON-Ausgabe.

## Kernfunktionen

| Kategorie | Funktionen |
|-----------|------------|
| **Installation** | Ein-Klick-Add-on-Installation, Auto-Discovery-Integration, Ingress-Support (kein Port-Forwarding) |
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
- 10+ Sensoren für Download/Upload, Ping, Jitter, Paketverlust und ISP-Qualitätsbewertung bereitstellt
- Internet-Ausfälle automatisch mit intelligenter 3-Strike-Retry-Logik erkennt
- SLA-Compliance trackt und Zuverlässigkeitsprozente berechnet
- QoS-Anforderungen für Gaming, Streaming und Videoanrufe analysiert
- Professionelle PDF-Berichte mit Diagrammen und Statistiken generiert
- Sich vollständig in Home Assistant Automationen integriert

**Keine technischen Kenntnisse erforderlich** — einfach installieren und es funktioniert!

---

## Schnellstart (5 Minuten)

### Schritt 1: Repository hinzufügen

1. Öffne Home Assistant
2. Gehe zu **Einstellungen** (Zahnrad-Symbol in der Seitenleiste)
3. Klicke auf **Add-ons**
4. Klicke auf **Add-on Store** (unten rechts)
5. Klicke auf die **drei Punkte** (⋮) oben rechts
6. Wähle **Repositories**
7. Füge diese URL ein: `https://github.com/akustikrausch/gonzales-ha`
8. Klicke **Hinzufügen**
9. Klicke **Schließen**

### Schritt 2: Gonzales installieren

1. Suche im Add-on Store nach **Gonzales Speed Monitor**
2. Klicke darauf
3. Klicke **Installieren** (kann 1-2 Minuten dauern)
4. Nach der Installation klicke **Starten**
5. Aktiviere **In Seitenleiste anzeigen** (optional aber empfohlen)

### Schritt 3: Fertig!

Klicke auf **Gonzales** in der Seitenleiste, um das Dashboard zu sehen. Der erste Speedtest startet automatisch innerhalb weniger Minuten.

Eine Benachrichtigung erscheint, um die Integration einzurichten - klicke **Konfigurieren**, um Sensoren zu Home Assistant hinzuzufügen.

---

## Konfiguration (Optional)

### In den Home Assistant Add-on Einstellungen

Gehe zu **Einstellungen → Add-ons → Gonzales Speed Monitor → Konfiguration**

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

Nach der Einrichtung erhältst du diese Sensoren:

| Sensor | Was er anzeigt |
|--------|----------------|
| Download Speed | Deine letzte Download-Geschwindigkeit in Mbps |
| Upload Speed | Deine letzte Upload-Geschwindigkeit in Mbps |
| Ping | Reaktionszeit deiner Verbindung (niedriger = besser) |
| ISP Score | Gesamtbewertung deines Internets (0-100) |
| Last Test Time | Wann der letzte Test lief |
| Internet Outage | Binärer Sensor: AN wenn Ausfall erkannt |

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
Home Assistant aktualisiert Add-ons automatisch. Du kannst auch manuell aktualisieren unter **Einstellungen → Add-ons → Gonzales → Aktualisieren**.

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
1. Gehe zu **Einstellungen → Add-ons → Gonzales**
2. Klicke **Neustart**
3. Warte 30 Sekunden, dann versuche es erneut

### "Sensoren zeigen nicht verfügbar"
Die Sensoren brauchen mindestens einen abgeschlossenen Test. Warte ein paar Minuten oder starte einen manuellen Test im Dashboard.

### "Speedtest schlägt immer fehl"
Prüfe die Add-on Logs: **Einstellungen → Add-ons → Gonzales → Log**. Häufige Ursachen:
- Keine Internetverbindung
- Firewall blockiert den Speedtest
- Temporäre Ookla Server-Probleme (später erneut versuchen)

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
