"""Constants for the Namedays integration."""
from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.const import UnitOfPower


DOMAIN = "nordicgridinfo"

_COUNTRY = {
    "Norway": "NO",
    "Sweden": "SE",
    "Finland":"FI",
    "Denmark":"DK",
    "Estonia":"EE",
    "Lithuania":"LT",
    "Latvia":"LV",
}

_ZONES= {"NO":["NO1","NO2","NO3","NO4","NO5"],
       "DK":["DK1","DK2"],
       "SE":["SE1","SE2","SE3","SE4"],
       "DE":["DE"],
       "FI":["FI"],
       "EE":["EE"],
       "LT":["LT"],
       "LV":["LV"],
       "PL":["PL"],
       "GB":["GB"],
       "RU":["RU"],
       "EN":["EN"]
}

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="consumption",
        name="Total consumption",
        icon="mdi:home-lightning-bolt",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
    SensorEntityDescription(
        key="production",
        name="Total production",
        icon="mdi:transmission-tower-import",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
    SensorEntityDescription(
        key="export",
        name="Total export",
        icon="mdi:transmission-tower-export",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
)

SENSORS_PRODTYPE: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="nuclear",
        name="Nuclear production",
        icon="mdi:atom",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
    SensorEntityDescription(
        key="hydro",
        name="Hydro production",
        icon="mdi:hydro-power",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
    SensorEntityDescription(
        key="wind",
        name="Wind production",
        icon="mdi:wind-power",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
    SensorEntityDescription(
        key="thermal",
        name="Thermal production",
        icon="mdi:gas-burner",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
    SensorEntityDescription(
        key="unknown",
        name="Unknown production",
        icon="mdi:lightbulb-question",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfPower.MEGA_WATT
    ),
)

