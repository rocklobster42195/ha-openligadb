Hier ist deine professionelle `ROADMAP.md`. Sie fasst alle unsere besprochenen Konzepte, die technischen Verbesserungen zur Beseitigung unschöner Begriffe wie "Hub" sowie die zukünftigen Visionen für Karten und Automatisierungen zusammen.

***

# 🗺 OpenLigaDB Integration - Roadmap & Ideen

Dieses Dokument dient als zentrale Sammlung für geplante Features, UX-Verbesserungen und kreative Ideen, um die Integration zur ultimativen Fußball-Erfahrung in Home Assistant zu machen.

## 🎨 UI & Polish (User Experience)
*Verbesserungen der Optik und Integration in das HA-Ökosystem.*

- [ ] **Renaming "Hub":** Erstellung von `translations/de.json` und `strings.json`, um den technischen Begriff "Hub" durch "Mannschaft" oder "Verein" zu ersetzen.
- [ ] **Entity Pictures:** Umstellung der Sensoren von statischen Icons auf `entity_picture`. Das echte Vereinslogo soll direkt in der HA-Entitätenliste und in runden Avataren erscheinen.
- [ ] **Official Branding:** Einreichen eines Pull-Requests beim [Home Assistant Brands Repository](https://github.com/home-assistant/brands), damit das OpenLigaDB-Logo in der Integrationsübersicht erscheint.
- [ ] **Internationalisierung:** Bereitstellung von Übersetzungen in Deutsch und Englisch für alle Menüs.

## 🛠 Architektur & Daten-Optimierung
*Stabilität und Effizienz im Hintergrund.*

- [ ] **Shared Polling:** Umbau des Coordinators, damit bei mehreren Mannschaften derselben Liga nur ein API-Aufruf pro Intervall erfolgt (Schonung der OpenLigaDB-Server).
- [ ] **Binary Sensors:** Einführung spezieller Sensoren für Automatisierungen:
    - `binary_sensor.team_match_day`: `on` am Tag des Spiels.
    - `binary_sensor.team_is_playing`: `on` während der 90+ Minuten (perfekt für "Nicht stören"-Szenarien).
- [ ] **Erweiterte Attribute:** Aufnahme von Stadion-Infos, Schiedsrichter und Zuschauerzahlen in die Sensor-Attribute.

## 📊 Tabellen & Wettbewerbe
*Mehr als nur das nächste Spiel.*

- [ ] **League Standings Sensor:** Ein neuer Sensortyp pro Liga, der die komplette Tabelle als strukturiertes Array speichert.
- [ ] **Tabellen-Karte:** Eine Dashboard-Karte, die die aktuelle Tabelle anzeigt, mit Fokus (Highlighting) auf das eigene Team und die direkte Konkurrenz (Plätze darüber/darunter).
- [ ] **Spieltags-Übersicht:** Ein Sensor, der alle Ergebnisse des aktuellen Spieltags liefert.

## ⚡️ Advanced Dashboard Visuals
*Kreative Ideen für die Match-Karte.*

- [ ] **Goal Alerts:** Die Karte soll bei einem Tor für 30 Sekunden visuell aufblinken oder einen goldenen/grünen Rahmen erhalten.
- [ ] **Next 5 Matches:** Eine kompakte Listenansicht der nächsten 5 Termine für die langfristige Planung.
- [ ] **Form-Anzeige:** Kleine farbige Punkte (S-S-U-N-S), die die Formkurve der letzten 5 Spiele im Badge-Bereich anzeigen.

## 🔔 Automatisierung & Ökosystem
*Fußball trifft Smart Home.*

- [ ] **Tor-Events:** Auslösen eines HA-Events (`openligadb_goal`), damit Nutzer ihre Philips Hue Lampen bei einem Tor in Vereinsfarben blinken lassen können.
- [ ] **Kalender-Integration:** Automatisches Synchronisieren der Spieltermine in den Home Assistant Kalender.
- [ ] **Sieg-Benachrichtigung:** Versenden einer "Push-Notification" mit dem Endergebnis direkt nach Abpfiff.

## 🚀 Distribution
- [ ] **HACS Integration:** Aufnahme in den offiziellen HACS-Default-Store.
- [ ] **Versionierung:** Einführung eines sauberen Release-Zyklus (v1.1.0, v1.2.0 etc.) über Git-Tags.

---
*Diese Roadmap ist ein lebendes Dokument. Ideen und Vorschläge aus der Community sind jederzeit willkommen!*