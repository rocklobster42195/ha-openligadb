from datetime import timedelta
import logging
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class OpenLigaDBUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, session, league, team_id, season):
        self.league = league
        self.team_id = int(team_id)
        self.season = season
        self.session = session
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(minutes=15))

    def _parse_datetime(self, date_str):
        if not date_str: return None
        dt = dt_util.parse_datetime(date_str)
        return dt_util.as_local(dt) if dt and dt.tzinfo is None else dt

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(10):
                url = f"https://api.openligadb.de/getmatchdata/{self.league}/{self.season}"
                async with self.session.get(url) as resp:
                    all_matches = await resp.json()
                    team_matches = [m for m in all_matches if m['team1']['teamId'] == self.team_id or m['team2']['teamId'] == self.team_id]
                    team_matches.sort(key=lambda x: x['matchDateTime'])
                    
                    now = dt_util.now()
                    selected_match = None

                    # 1. Live-Match suchen
                    live_match = next((m for m in team_matches if not m['matchIsFinished'] and self._parse_datetime(m['matchDateTime']) <= now), None)
                    
                    if live_match:
                        selected_match = live_match
                        self.update_interval = timedelta(minutes=1)
                    else:
                        self.update_interval = timedelta(minutes=15)
                        finished = [m for m in team_matches if m['matchIsFinished']]
                        last_finished = finished[-1] if finished else None
                        upcoming = next((m for m in team_matches if not m['matchIsFinished']), None)
                        
                        # Wenn das letzte Spiel < 24h her ist, zeige es als Ergebnis an
                        if last_finished and (now - self._parse_datetime(last_finished['matchDateTime'])).total_seconds() < 86400:
                            selected_match = last_finished
                            # Aber: Wenn das nächste Spiel in < 3h beginnt, wechsle zur Vorschau
                            if upcoming and (self._parse_datetime(upcoming['matchDateTime']) - now).total_seconds() < 10800:
                                selected_match = upcoming
                        else:
                            selected_match = upcoming if upcoming else last_finished

                    return selected_match
        except Exception as err:
            raise UpdateFailed(f"API Fehler: {err}")