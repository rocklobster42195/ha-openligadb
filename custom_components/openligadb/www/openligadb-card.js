/*
  MAPPING FÜR MANUELLE LOGO-KORREKTUREN
  Syntax: "TeamID": "HTTPS-Link zum Logo"
*/
const LOGO_MAPPING = {
  "98": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Fc_st_pauli_logo.svg",
  "7":  "https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg"
};

console.info("%c OPENLIGADB-CARD %c v14.0.0 (Smart-Live-Edition) ", "color: white; background: #25a69a; font-weight: 700;", "color: #25a69a; background: white; font-weight: 700;");

class OpenLigaDBCard extends HTMLElement {
  static getConfigForm() {
    return { schema: [{ name: "entity", label: "Mannschaft", required: true, selector: { entity: { domain: "sensor", filter: [{ integration: "openligadb" }] } } }] };
  }

  setConfig(config) { this.config = config; }

  set hass(hass) {
    const stateObj = hass.states[this.config.entity];
    if (!stateObj) return;

    const attr = stateObj.attributes;
    const state = stateObj.state;

    // Zeitberechnung
    const matchDate = new Date(attr.datetime);
    const now = new Date();
    const isToday = matchDate.toDateString() === now.toDateString();
    const tomorrow = new Date(); tomorrow.setDate(now.getDate() + 1);
    const isTomorrow = matchDate.toDateString() === tomorrow.toDateString();
    const timeOnly = matchDate.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' }) + " Uhr";
    
    let badgeText = timeOnly;

    if (state === "live") {
      const diffMs = now - matchDate;
      const diffMins = Math.floor(diffMs / 60000);
      let currentMinute = 0;
      
      // Basis-Text bestimmen
      if (diffMins < 45) {
        currentMinute = diffMins;
        badgeText = `${currentMinute}. Min.`;
      } else if (diffMins >= 45 && diffMins < 60) {
        badgeText = "Halbzeit";
      } else if (diffMins >= 60 && diffMins < 105) {
        currentMinute = diffMins - 15;
        badgeText = `${currentMinute}. Min.`;
      } else {
        currentMinute = 90;
        badgeText = "90.+ Min.";
      }

      // INTELLIGENTE TOR-ANZEIGE:
      // Falls ein Tor gefallen ist und es weniger als 5 Min her ist, zeige das Tor im Badge
      if (attr.last_goal && attr.last_goal_minute) {
        const goalAge = currentMinute - attr.last_goal_minute;
        if (goalAge >= 0 && goalAge <= 5) {
          badgeText = `⚽️ ${attr.last_goal}`;
        }
      }
    } else if (state === "finished") {
      badgeText = "Spiel beendet";
    } else {
      if (isToday) badgeText = `Heute, ${timeOnly}`;
      else if (isTomorrow) badgeText = `Morgen, ${timeOnly}`;
      else badgeText = matchDate.toLocaleDateString('de-DE', { weekday: 'short', day: '2-digit', month: '2-digit' }) + "., " + timeOnly;
    }

    const homeIcon = LOGO_MAPPING[attr.team_home_id] || attr.team_home_icon.replace('http:', 'https:');
    const awayIcon = LOGO_MAPPING[attr.team_away_id] || attr.team_away_icon.replace('http:', 'https:');

    this.innerHTML = `
      <style>
        .ol-card { padding: 16px; text-align: center; cursor: pointer; transition: opacity 0.2s; }
        @keyframes ol-pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
        .ol-live-dot { height: 10px; width: 10px; background-color: #e74c3c; border-radius: 50%; display: inline-block; margin-right: 8px; animation: ol-pulse 1.5s infinite; }
        .ol-header { font-size: 0.85em; color: var(--secondary-text-color); text-transform: uppercase; letter-spacing: 1.5px; font-weight: bold; margin-bottom: 15px; }
        .ol-header.is-live { color: #e74c3c; }
        .ol-match { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .ol-team { flex: 1; text-align: center; width: 40%; }
        .ol-team img { width: 55px; height: 55px; object-fit: contain; }
        .ol-team-name { font-size: 0.85em; margin-top: 8px; font-weight: 500; line-height: 1.2; }
        .ol-score { flex: 0.6; font-size: 2.2em; font-weight: 900; }
        .ol-badge { display: inline-block; padding: 6px 18px; background: var(--secondary-background-color); border-radius: 20px; font-size: 0.9em; font-weight: 500; border: 1px solid var(--divider-color); }
      </style>
      <ha-card class="ol-card">
        <div class="ol-header ${state === 'live' ? 'is-live' : ''}">
          ${state === 'live' ? '<span class="ol-live-dot"></span>LIVE' : (state === 'finished' ? 'Endergebnis' : 'Nächstes Spiel')}
        </div>
        <div class="ol-match">
          <div class="ol-team"><img src="${homeIcon}"><div class="ol-team-name">${attr.team_home}</div></div>
          <div class="ol-score">${state !== 'scheduled' ? `${attr.score_home}:${attr.score_away}` : '<span style="opacity:0.3;font-size:0.7em">VS</span>'}</div>
          <div class="ol-team"><img src="${awayIcon}"><div class="ol-team-name">${attr.team_away}</div></div>
        </div>
        <div class="ol-badge">${badgeText}</div>
      </ha-card>
    `;

    this.onclick = () => {
      this.style.opacity = "0.5";
      setTimeout(() => { this.style.opacity = "1"; }, 200);
      hass.callService("homeassistant", "update_entity", { entity_id: this.config.entity });
    };
  }
}
customElements.define("openligadb-card", OpenLigaDBCard);
window.customCards = window.customCards || [];
window.customCards.push({ type: "openligadb-card", name: "OpenLigaDB Match Card", preview: true });