"""Config flow for Input Stats integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.sensor import (
    DEVICE_CLASS_UNITS,
)
from homeassistant.helpers.selector import (
    IconSelector,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
)

from .const import (
    CONF_ICON,
    CONF_NAME,
    CONF_STATE_CLASS,
    CONF_UNIT_OF_MEASUREMENT,
    DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.data_entry_flow import FlowResult

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Input Stats."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Config flow for Net Balance."""
        schema = vol.Schema(
            {
                vol.Required(CONF_NAME): TextSelector(
                    TextSelectorConfig(multiline=False)
                ),
                vol.Required(CONF_ICON): IconSelector(),
                vol.Required(CONF_STATE_CLASS): SelectSelector(
                    SelectSelectorConfig(
                        translation_key="state_class",
                        multiple=False,
                        options=[
                            SelectOptionDict(label="TOTAL", value="TOTAL"),
                            SelectOptionDict(label="MEASUREMENT", value="MEASUREMENT"),
                        ],
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional(CONF_UNIT_OF_MEASUREMENT): SelectSelector(
                    SelectSelectorConfig(
                        options=list(
                            {
                                str(unit)
                                for units in DEVICE_CLASS_UNITS.values()
                                for unit in units
                                if unit is not None
                            }
                        ),
                        mode=SelectSelectorMode.DROPDOWN,
                        translation_key="sensor_unit_of_measurement",
                        custom_value=True,
                        sort=True,
                    ),
                ),
            }
        )

        # Handle the initial step.
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=schema)

        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
