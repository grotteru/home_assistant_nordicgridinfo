"""Coordinator for Namedays integration."""
import datetime
import logging
import time  # Add this import
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util
from .statnett_api import fetch_productionconsumption, get_all_data, get_exchanges_by_zone
from .const import _COUNTRY

_LOGGER = logging.getLogger(__name__)

class NordicGridInfoCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from Statnett API."""

    def __init__(self, hass, country: str,corridors:bool):
        """Initialize the NordicGridInfo coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"NordicGridInfo data {country}",
            update_interval=datetime.timedelta(minutes=1),
        )
        self._session = async_get_clientsession(hass)
        self.country = country
        self.corridors = corridors
        self.countrycode = _COUNTRY[country]

    async def _async_update_data(self):
        """Fetch data from the API."""
        data = {} if self.data is None else self.data
        if self.corridors:
            try:
                data = await get_all_data(self._session, self.countrycode, self.corridors)
            except Exception:
                _LOGGER.error(f"Error fetching Statnett-data")
            return data
        try:
            data = await fetch_productionconsumption(self._session, self.countrycode)
        except Exception:
            _LOGGER.error(f"Error fetching Statnett-data ")
        return data