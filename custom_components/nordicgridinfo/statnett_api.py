from datetime import datetime
import logging
from homeassistant.util import dt as dt_util
from .const import _ZONES

STATNETT_API_PROD = "http://driftsdata.statnett.no/restapi/ProductionConsumption/GetLatestDetailedOverview"
STATNETT_API_FLOW='http://driftsdata.statnett.no/restapi/PhysicalFlowMap/GetFlow'

_LOGGER = logging.getLogger(__name__)

async def get_all_data(session,zone_key:str,all:bool):
    data = await fetch_productionconsumption(session,zone_key)
    if not all:
        return data
    data["exchange"]=await get_exchanges_by_zone(session,zone_key)
    return data

async def fetch_productionconsumption(
        session,
        zone_key: str,
):
    resp = await session.get(STATNETT_API_PROD)
    obj = await resp.json()

    def get_value(data, key):
        item = next((x for x in data if x['titleTranslationId'] == key and x['value'] != "-"), None)
        return float(item['value'].replace(u'\xa0', '')) if item else 0.0

    data = {
        'zoneKey': zone_key,
        'production': get_value(obj['ProductionData'], f'ProductionConsumption.Production{zone_key}Desc'),
        'nuclear': get_value(obj['NuclearData'], f'ProductionConsumption.Nuclear{zone_key}Desc'),
        'hydro': get_value(obj['HydroData'], f'ProductionConsumption.Hydro{zone_key}Desc'),
        'wind': get_value(obj['WindData'], f'ProductionConsumption.Wind{zone_key}Desc'),
        'thermal': get_value(obj['ThermalData'], f'ProductionConsumption.Thermal{zone_key}Desc'),
        'unknown': get_value(obj['NotSpecifiedData'], f'ProductionConsumption.NotSpecifiedData{zone_key}Desc'),
        'consumption': get_value(obj['ConsumptionData'], f'ProductionConsumption.Consumption{zone_key}Desc'),
        #Want export to be postive
        'export': -get_value(obj['NetExchangeData'], f'ProductionConsumption.NetExchange{zone_key}Desc'),
    }

    return data

async def get_exchanges_by_zone(
        session,
        zone_key: str
):
    resp = await session.get(STATNETT_API_FLOW)
    obj = await resp.json()
    # Validate zone_key
    if zone_key not in _ZONES:
        raise ValueError(f"Zone key '{zone_key}' is not valid.")
    
    # Get the subzones for the specified zone_key
    subzones = set(_ZONES[zone_key])
    
    # Collect valid exchanges
    data = {}
    for entry in obj:
        out_zone = entry.get('OutAreaElspotId')
        in_zone = entry.get('InAreaElspotId')
        value = entry.get('Value')
        # Exception 1: Replace 'EN' with 'GB'
        if out_zone == 'EN':
            out_zone = 'GB'
        if in_zone == 'EN':
            in_zone = 'GB'

        # Exception 2: Multiply the value by -1 for the specific SE4->DK2 case
        if out_zone == 'SE4' and in_zone == 'DK2':
            value *= -1

        # Check if OutAreaElspotId is in the subzones of the selected zone
        # and InAreaElspotId belongs to another zone
        if out_zone in subzones and in_zone not in subzones:
            data[f"{out_zone}->{in_zone}"] = value
        elif in_zone in subzones and out_zone not in subzones:
            data[f"{in_zone}->{out_zone}"] = -value

    return data

