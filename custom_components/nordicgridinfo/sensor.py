"""Platform for Namedays sensor."""
from datetime import date,timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.const import UnitOfPower
from .const import DOMAIN,SENSORS,SENSORS_PRODTYPE
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.util import dt as dt_util
from .coordinator import NordicGridInfoCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up NordicGridInfo sensor."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    country = config["country"]
    corridors = config["all_corridors"]
    coordinator = NordicGridInfoCoordinator(hass, country,corridors)

    await coordinator.async_config_entry_first_refresh()

    sensors = [NordicGridInfo(coordinator, description) for description in SENSORS]

    if config["all_prodtypes"]:
        sensors += [NordicGridInfo(coordinator, description) for description in SENSORS_PRODTYPE]

    if config["all_corridors"]:
        CORR_SENSORS = tuple(
        SensorEntityDescription(
            key=key,
            name="Flow",
            icon="mdi:transmission-tower-export",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfPower.MEGA_WATT,
            suggested_display_precision=1,
            )
        for key in coordinator.data["exchange"]
        )
        sensors += [NordicGridInfo(coordinator, description) for description in CORR_SENSORS]

    async_add_entities(sensors)

    await coordinator.async_config_entry_first_refresh()



class NordicGridInfo(SensorEntity,CoordinatorEntity["NordicGridInfoCoordinator"]):
    """Representation of the NordicGridInfo Sensor."""

    def __init__(self, coordinator, entity_description):
        """Initialize the sensor."""
        super().__init__(coordinator=coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{DOMAIN}_{self.entity_description.key}_{coordinator.country}_MW"
        if "->" in self.entity_description.key:
            self._attr_name= f"{self.entity_description.name} {self.entity_description.key}"
        else:
            self._attr_name= f"{self.entity_description.name} {coordinator.country}"


    @callback
    def _handle_coordinator_update(self) -> None:
        if "->" in self.entity_description.key:
            value = self.coordinator.data["exchange"].get(self.entity_description.key)
        else:
            value = self.coordinator.data.get(self.entity_description.key)
        self._attr_native_value = value if value is not None else self._attr_native_value
        self.async_write_ha_state()