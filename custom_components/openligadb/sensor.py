"""Sensor platform for OpenLigaDB."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up OpenLigaDB sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([OpenLigaDBMatchSensor(coordinator, entry)], True)

class OpenLigaDBMatchSensor(SensorEntity):
    """Sensor for the next or current match of a team."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = f"OpenLigaDB {entry.data['team_name']}"
        self._attr_unique_id = f"{entry.entry_id}_match"

    @property
    def state(self) -> str:
        """Return the state of the sensor (scheduled, live, finished)."""
        m = self.coordinator.data
        if not m:
            return "unknown"
        
        match_time_str = m.get('matchDateTime')
        if not match_time_str:
            return "scheduled"
        
        match_time = dt_util.parse_datetime(match_time_str)
        if match_time:
            match_time = dt_util.as_local(match_time)
            now = dt_util.now()

            # 1. AUTO-ABPFIFF LOGIK:
            # Wenn das Spiel offiziell beendet ist ODER seit Anpfiff 4 Stunden vergangen sind
            if m.get('matchIsFinished') or (now - match_time).total_seconds() > 14400:
                return "finished"
            
            # 2. LIVE LOGIK:
            # Wenn die Anpfiff-Zeit erreicht oder überschritten ist
            if now >= match_time:
                return "live"
            
        return "scheduled"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes for the dashboard card."""
        m = self.coordinator.data
        if not m:
            return {}

        # Ergebnis-Logik: Suche nach dem Endergebnis (ResultTypeID 2)
        results = m.get('matchResults', [])
        res = next((r for r in results if r.get('resultTypeID') == 2), None)
        # Fallback auf das letzte verfügbare Teilergebnis (während des Spiels)
        if not res and results:
            res = results[-1]

        # Tor-Logik: Finde das letzte Tor für den Ticker
        goals = m.get('goals', [])
        last_goal_text = ""
        last_goal_minute = 0
        
        if goals:
            g = goals[-1]
            last_goal_minute = g.get('matchMinute', 0)
            name = g.get('goalGetterName')
            # Format: "72' Tor" oder "72' Tor: Name"
            last_goal_text = f"{last_goal_minute}' Tor" + (f": {name}" if name else "")

        return {
            "datetime": m.get('matchDateTime'),
            "team_home": m.get('team1', {}).get('teamName', 'Heim'),
            "team_home_id": str(m.get('team1', {}).get('teamId', '')),
            "team_home_icon": m.get('team1', {}).get('teamIconUrl', ''),
            "team_away": m.get('team2', {}).get('teamName', 'Gast'),
            "team_away_id": str(m.get('team2', {}).get('teamId', '')),
            "team_away_icon": m.get('team2', {}).get('teamIconUrl', ''),
            "score_home": res.get('pointsTeam1', 0) if res else 0,
            "score_away": res.get('pointsTeam2', 0) if res else 0,
            "last_goal": last_goal_text,
            "last_goal_minute": last_goal_minute,
            "match_id": m.get('matchID'),
            "league_name": self._entry.data.get("team_name"), # Nutzt Teamnamen als Label
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success