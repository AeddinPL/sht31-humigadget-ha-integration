"""Config flow for Sensirion SHT31 Smart Humigadget integration."""
from __future__ import annotations

import re
from typing import Any

import voluptuous as vol
from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CONF_MAC, CONF_NAME, DEFAULT_NAME, DOMAIN

MAC_REGEX = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")


class SHT31ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sensirion SHT31 Smart Humigadget."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow."""
        self._discovered_info: bluetooth.BluetoothServiceInfoBleak | None = None

    async def async_step_bluetooth(
        self, discovery_info: bluetooth.BluetoothServiceInfoBleak
    ) -> ConfigFlowResult:
        """Handle bluetooth discovery."""
        formatted_mac = discovery_info.address.upper()
        await self.async_set_unique_id(formatted_mac)
        self._abort_if_unique_id_configured()

        self._discovered_info = discovery_info
        self.context["title_placeholders"] = {
            "name": discovery_info.name or DEFAULT_NAME,
            "address": formatted_mac,
        }
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm bluetooth discovery."""
        assert self._discovered_info is not None

        if user_input is not None:
            name = user_input.get(CONF_NAME, self._discovered_info.name or DEFAULT_NAME)
            return self.async_create_entry(
                title=name,
                data={
                    CONF_MAC: self._discovered_info.address.upper(),
                    CONF_NAME: name,
                },
            )

        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders={
                "name": self._discovered_info.name or DEFAULT_NAME,
                "address": self._discovered_info.address.upper(),
            },
            data_schema=vol.Schema({
                vol.Optional(CONF_NAME, default=self._discovered_info.name or DEFAULT_NAME): str,
            }),
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle user-initiated configuration flow."""
        errors: dict[str, str] = {}

        if user_input is not None:
            raw_mac = user_input[CONF_MAC].strip()
            if not MAC_REGEX.match(raw_mac):
                errors[CONF_MAC] = "invalid_mac"
            else:
                formatted_mac = raw_mac.upper()
                await self.async_set_unique_id(formatted_mac)
                self._abort_if_unique_id_configured()

                name = user_input.get(CONF_NAME, DEFAULT_NAME)
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_MAC: formatted_mac,
                        CONF_NAME: name,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_MAC, default="F3:15:B7:5E:61:C2"): str,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
