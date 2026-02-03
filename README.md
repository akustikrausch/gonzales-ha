# Gonzales Speed Monitor for Home Assistant

Monitor your internet speed automatically and see results directly in Home Assistant.

**[Deutsche Anleitung weiter unten](#deutsche-anleitung)**

---

## What is Gonzales?

Gonzales is an internet speed monitor that:
- Runs automatic speed tests at regular intervals (e.g., every 30 minutes)
- Shows your download/upload speeds and ping in Home Assistant
- Alerts you when your internet is slower than expected
- Keeps a history of all tests so you can see trends over time

**No technical knowledge required** - just install and it works!

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
| Test interval | How often to run tests | Every 30 minutes |
| Download threshold | Your internet plan's download speed | 1000 Mbps |
| Upload threshold | Your internet plan's upload speed | 500 Mbps |
| Tolerance | How much slower is still "OK" | 15% |

### In the Gonzales Web Dashboard

Click **Gonzales** in the sidebar, then go to **Settings**. You can run manual tests, change the theme, and see system status.

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

Use these sensors in automations, dashboards, or to track your ISP's performance over time.

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

## Links

- [Main Gonzales Project](https://github.com/akustikrausch/gonzales) - Full documentation, standalone setup, API reference
- [Report Issues](https://github.com/akustikrausch/gonzales-ha/issues) - Bug reports and feature requests
- [Ookla Terms](https://www.speedtest.net/about/terms) - Speed test provider's terms of use

---

---

# Deutsche Anleitung

## Was ist Gonzales?

Gonzales ist ein Internet-Geschwindigkeitsmonitor, der:
- Automatisch regelmäßige Speedtests durchführt (z.B. alle 30 Minuten)
- Download/Upload-Geschwindigkeiten und Ping in Home Assistant anzeigt
- Dich warnt, wenn dein Internet langsamer ist als erwartet
- Eine Historie aller Tests speichert, damit du Trends erkennen kannst

**Keine technischen Kenntnisse erforderlich** - einfach installieren und es funktioniert!

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
| Test interval | Wie oft Tests laufen | Alle 30 Minuten |
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

## Lizenz

MIT (Gonzales Code). Die Ookla Speedtest CLI hat eine eigene Lizenz - durch die Nutzung akzeptierst du Ooklas [Nutzungsbedingungen](https://www.speedtest.net/about/terms).
