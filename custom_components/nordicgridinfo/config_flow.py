"""Config flow for NordicGridInfo sensor."""

from homeassistant import config_entries
from .const import DOMAIN, _COUNTRY
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from typing import Any, Dict, Optional

countries = sorted(list(_COUNTRY.keys()))

DATA_SCHEMA = vol.Schema(
    {
        vol.Required("country", default="Norway"): vol.In(countries),
        vol.Optional("all_prodtypes", default=False): cv.boolean,
        vol.Optional("all_corridors", default=False): cv.boolean,
    }
)


class PowerSystemFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NordicGridInfo."""

    async def async_step_user(self, user_input=None):
        errors: Dict[str, str] = {}
        """Handle the initial step."""
        if user_input is not None:
            # Opprett konfigurasjonsoppføringen
            return self.async_create_entry(
                title=f"NordiGridInfo {user_input['country']}", data=user_input
            )

        placeholders = {
            "country": countries,
        }
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            description_placeholders=placeholders,
            errors=errors,
        )
