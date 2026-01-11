# ⚽ OpenLigaDB für Home Assistant

Diese Integration bringt Live-Fußball-Daten von [OpenLigaDB.de](https://www.openligadb.de) direkt in dein Home Assistant Dashboard. Verfolge dein Lieblingsteam mit Live-Spielständen, berechneten Spielminuten und einer hochoptimierten Dashboard-Karte.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![HACS](https://img.shields.io/badge/HACS-Compatible-orange.svg)
![Home Assistant](https://img.shields.io/badge/Home--Assistant-2025.1+-green.svg)

## ✨ Features

- **Einfache Einrichtung:** Liga, Saison und Mannschaft bequem per Dropdown auswählen (Config Flow).
- **Intelligentes Polling:** 
    - **Normalbetrieb:** Alle 15 Minuten.
    - **Live-Modus:** Sobald ein Spiel läuft, schaltet die Integration automatisch auf **1-Minuten-Intervalle** um.
- **Smarte Zustands-Logik:** 
    - Automatische Erkennung von `Geplant`, `Live` und `Beendet`.
    - **24h-Ergebnis-Anzeige:** Nach Abpfiff bleibt das Ergebnis 24 Stunden lang sichtbar, bevor auf das nächste Spiel umgeschaltet wird.
    - **Auto-Abpfiff:** Sicherheitstimer beendet Spiele nach 4 Stunden automatisch (ideal für Pokalspiele mit Verlängerung oder hängende API-Daten).
- **Custom Dashboard Card:**
    - **Live-Ticker:** Pulsierender roter Punkt bei Live-Spielen.
    - **Spielminuten:** Automatisch berechnete Spielminute (inkl. Halbzeit-Erkennung).
    - **Tor-Fokus:** Ein neues Tor wird für 5 Minuten prominent im Badge angezeigt.
    - **Logo-Fixes:** Integriertes Mapping für problematische Vereinslogos (z.B. St. Pauli Fix via Wikimedia).
    - **Tap-to-Refresh:** Ein Tippen auf die Karte erzwingt sofort ein Daten-Update inklusive haptischem Feedback in der App.

## 📸 Vorschau
*(Hier Screenshot einfügen)*

## 🚀 Installation

### Über HACS (Empfohlen)
1. Öffne **HACS** in Home Assistant.
2. Klicke auf die drei Punkte oben rechts und wähle **Benutzerdefinierte Repositories**.
3. Füge die URL deines GitHub-Repositorys hinzu und wähle als Kategorie `Integration`.
4. Suche nach **OpenLigaDB** und klicke auf **Installieren**.
5. Starte Home Assistant neu.

### Manuelle Installation
1. Kopiere den Ordner `custom_components/openligadb` in das Verzeichnis `/config/custom_components/` deines Home Assistant.
2. Starte Home Assistant neu.

## ⚙️ Konfiguration

1. Gehe zu **Einstellungen > Geräte & Dienste**.
2. Klicke auf **Integration hinzufügen** und suche nach **OpenLigaDB**.
3. Wähle die gewünschte Liga (z.B. 1. Bundesliga), die Saison und dein Team aus.
4. Die Dashboard-Karte wird automatisch als Ressource registriert.

## 📊 Dashboard Nutzung

Die Integration bringt eine eigene Karte mit (`OpenLigaDB Match Card`). Du kannst sie einfach über den visuellen Editor hinzufügen:

1. Klicke auf **Karte hinzufügen**.
2. Suche nach **OpenLigaDB Match-Karte**.
3. Wähle deinen Sensor aus der Liste aus.

### YAML-Beispiel
```yaml
type: custom:openligadb-card
entity: sensor.openligadb_borussia_monchengladbach
```

## 🛠 Entwicklung

Das Projekt nutzt einen **VS Code Dev-Container** für eine konsistente Entwicklungsumgebung.

1. Repository klonen.
2. In VS Code öffnen und **Reopen in Container** wählen.
3. Home Assistant zum Testen starten:
   ```bash
   hass -c config
   ```

### Logo-Mapping erweitern
Sollte ein Vereinslogo in der API fehlen oder fehlerhaft sein, kann es in der `openligadb-card.js` im Objekt `LOGO_MAPPING` korrigiert werden:
```javascript
const LOGO_MAPPING = {
  "98": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Fc_st_pauli_logo.svg"
};
```

## 🛡 Disclaimer
Dieses Projekt ist eine private Entwicklung und steht in keiner offiziellen Verbindung zu OpenLigaDB.de. Ein großes Dankeschön geht an das Team von OpenLigaDB für die Bereitstellung der kostenlosen API.

---
*Erstellt für alle Fußballfans in der Home Assistant Community. Feedback und Pull-Requests sind willkommen!*