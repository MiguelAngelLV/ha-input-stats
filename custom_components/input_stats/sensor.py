"""Create and add sensors to Home Assistant."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from typing_extensions import override
import voluptuous as vol

from homeassistant.components.sensor import (
    RestoreEntity,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.helpers import config_validation as cv, entity_platform

from .const import (
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_MEASUREMENT,
    CONF_NAME,
    CONF_STATE_CLASS,
    CONF_UNIT_OF_MEASUREMENT,
    DOMAIN,
    SERVICE_DECREMENT,
    SERVICE_INCREMENT,
    SERVICE_SET_VALUE,
)

if TYPE_CHECKING:
    from datetime import date, datetime
    from decimal import Decimal

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    _: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Initialise sensors and add to Home Assistant."""
    name = entry.data[CONF_NAME]
    icon = entry.data[CONF_ICON]
    unit_of_measurement = entry.data.get(CONF_UNIT_OF_MEASUREMENT, None)
    device_class = entry.data.get(CONF_DEVICE_CLASS, None)
    state_class = (
        SensorStateClass.MEASUREMENT
        if entry.data[CONF_STATE_CLASS] == CONF_MEASUREMENT
        else SensorStateClass.TOTAL
    )

    description = SensorEntityDescription(
        key=DOMAIN,
        name=name,
        icon=icon,
        has_entity_name=True,
        state_class=state_class,
        device_class=device_class,
        native_unit_of_measurement=unit_of_measurement,
    )
    input_stats = InputStats(description=description, unique_id=entry.entry_id)

    platform = entity_platform.async_get_current_platform()

    platform.async_register_entity_service(
        SERVICE_INCREMENT,
        {vol.Required("amount"): cv.positive_float},
        SERVICE_INCREMENT,
    )
    platform.async_register_entity_service(
        SERVICE_DECREMENT,
        {vol.Required("amount"): cv.positive_float},
        SERVICE_DECREMENT,
    )
    platform.async_register_entity_service(
        SERVICE_SET_VALUE, {vol.Required("value"): cv.positive_float}, SERVICE_SET_VALUE
    )

    async_add_entities([input_stats])


class InputStats(SensorEntity, RestoreEntity):
    """Input Stats Sensor."""

    def __init__(self, description: SensorEntityDescription, unique_id: str) -> None:
        """Initialize all values."""
        super().__init__()
        self._attr_unique_id = unique_id
        self._state = 0
        self.entity_description = description

    @property
    @override
    def native_value(self) -> StateType | date | datetime | Decimal:
        return self._state

    @override
    async def async_added_to_hass(self) -> None:
        last_sensor_data = await self.async_get_last_state()
        if last_sensor_data is not None:
            self._state = float(last_sensor_data.state)
        else:
            self._state = 0

        self.async_write_ha_state()

    async def increment(self, amount: float) -> None:
        """Increment the sensor value."""
        await self.set_value(self._state + amount)

    async def decrement(self, amount: float) -> None:
        """Decrement the sensor value."""
        await self.set_value(self._state - amount)

    async def set_value(self, value: float) -> None:
        """Set the sensor value."""
        self._state = value
        self.async_write_ha_state()
