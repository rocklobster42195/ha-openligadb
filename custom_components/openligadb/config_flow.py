import voluptuous as vol
import re
import logging
from urllib.parse import quote
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_LEAGUE, CONF_SEASON, CONF_TEAM_ID, CONF_TEAM_NAME, DEFAULT_SEASON

_LOGGER = logging.getLogger(__name__)

class OpenLigaDBConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenLigaDB."""

    VERSION = 1

    def __init__(self):
        self.selected_league = None
        self.selected_season = DEFAULT_SEASON
        self.leagues_dict = {} 

    async def async_step_user(self, user_input=None):
        """Erster Schritt: Liga auswählen."""
        errors = {}
        session = async_get_clientsession(self.hass)
        
        try:
            async with session.get("https://api.openligadb.de/getavailableleagues") as resp:
                leagues = await resp.json()
                temp_dict = {}
                for l in leagues:
                    shortcut = l['leagueShortcut']
                    raw_name = l['leagueName']
                    
                    # Name säubern
                    clean_name = re.sub(r'\s\d{4}(/\d{4})?.*', '', raw_name).strip()
                    clean_name = clean_name.strip("'").strip('"')
                    
                    if shortcut not in temp_dict:
                        temp_dict[shortcut] = clean_name

                # Sortierung: Wichtige Ligen nach oben
                def sort_key(item):
                    shortcut, name = item
                    priority = {"bl1": 0, "bl2": 1, "bl3": 2, "dfb": 3}
                    return (priority.get(shortcut.lower(), 99), name)

                self.leagues_dict = dict(sorted(temp_dict.items(), key=sort_key))
        except Exception as err:
            _LOGGER.error("Fehler beim Laden der Ligen: %s", err)
            errors["base"] = "cannot_connect"

        if user_input is not None:
            self.selected_league = user_input[CONF_LEAGUE]
            self.selected_season = user_input[CONF_SEASON]
            return await self.async_step_team()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_LEAGUE): vol.In(self.leagues_dict),
                vol.Required(CONF_SEASON, default=DEFAULT_SEASON): str,
            }),
            errors=errors
        )

    async def async_step_team(self, user_input=None):
        """Zweiter Schritt: Team mit dem KORREKTEN Endpunkt auswählen."""
        errors = {}
        teams_map = {}

        session = async_get_clientsession(self.hass)
        safe_league = quote(self.selected_league)
        # KORREKTUR: /getavailableteams statt /getteamsbyleagueandsport
        url = f"https://api.openligadb.de/getavailableteams/{safe_league}/{self.selected_season}"
        
        _LOGGER.warning("OpenLigaDB: Versuche Teams zu laden von: %s", url)

        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    _LOGGER.error("OpenLigaDB API Fehler %s bei %s", resp.status, url)
                    errors["base"] = "cannot_get_teams"
                else:
                    teams = await resp.json()
                    if not teams:
                        errors["base"] = "no_teams_found"
                    else:
                        for t in teams:
                            # Wir nehmen teamId als String für das Schema
                            teams_map[str(t['teamId'])] = t['teamName']
                        
                        # Alphabetisch sortieren
                        teams_map = dict(sorted(teams_map.items(), key=lambda item: item[1]))
        except Exception as err:
            _LOGGER.error("Exception beim Laden der Teams: %s", err)
            errors["base"] = "cannot_connect"

        if user_input is not None and not errors:
            team_id = user_input[CONF_TEAM_ID]
            return self.async_create_entry(
                title=f"{teams_map[team_id]} ({self.selected_league})",
                data={
                    CONF_LEAGUE: self.selected_league,
                    CONF_SEASON: self.selected_season,
                    CONF_TEAM_ID: int(team_id), # Als Integer speichern
                    CONF_TEAM_NAME: teams_map[team_id],
                },
            )

        # Falls ein Fehler auftrat, zurück zum ersten Schritt oder Fehler anzeigen
        if errors:
             return self.async_show_form(
                step_id="user", 
                data_schema=vol.Schema({
                    vol.Required(CONF_LEAGUE, default=self.selected_league): vol.In(self.leagues_dict),
                    vol.Required(CONF_SEASON, default=self.selected_season): str,
                }),
                errors=errors
            )

        return self.async_show_form(
            step_id="team",
            data_schema=vol.Schema({
                vol.Required(CONF_TEAM_ID): vol.In(teams_map),
            }),
            errors=errors
        )