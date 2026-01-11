"""The OpenLigaDB integration."""
from __future__ import annotations
import logging
import os
import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant, CoreState
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.components.http import StaticPathConfig
from .const import DOMAIN, CONF_LEAGUE, CONF_SEASON, CONF_TEAM_ID
from .coordinator import OpenLigaDBUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = async_get_clientsession(hass)
    coordinator = OpenLigaDBUpdateCoordinator(hass, session, entry.data[CONF_LEAGUE], entry.data[CONF_TEAM_ID], entry.data[CONF_SEASON])
    
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    current_dir = os.path.dirname(__file__)
    static_path = os.path.join(current_dir, "www")
    
    if os.path.exists(static_path):
        await hass.http.async_register_static_paths([StaticPathConfig("/openligadb/www", static_path, False)])

    async def _register_resources(_=None):
        await asyncio.sleep(2)
        if "lovelace" in hass.data:
            lovelace = hass.data["lovelace"]
            resources = getattr(lovelace, "resources", None)
            if resources and hasattr(resources, "async_create_item"):
                url = "/openligadb/www/openligadb-card.js"
                items = resources.async_items()
                if asyncio.iscoroutine(items): items = await items
                if not any(res.get("url") == url for res in items):
                    await resources.async_create_item({"res_type": "module", "url": url})

    if hass.state == CoreState.running:
        hass.async_create_task(_register_resources())
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _register_resources)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok: hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok