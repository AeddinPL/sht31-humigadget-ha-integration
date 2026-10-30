"""DataUpdateCoordinator for Sensirion SHT31 Smart Humigadget."""
from __future__ import annotations

import logging
import struct
from datetime import timedelta
from typing import Any

from bleak import BleakClient
from homeassistant.components import bluetooth
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    BATT_CHAR_UUID,
    DEFAULT_SCAN_INTERVAL,
    HUM_CHAR_UUID,
    TEMP_CHAR_UUID,
)

_LOGGER = logging.getLogger(__name__)


class SHT31Coordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage polling data from Sensirion SHT31 Smart Humigadget."""

    def __init__(self, hass: HomeAssistant, address: str, name: str, scan_interval: int = DEFAULT_SCAN_INTERVAL) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"SHT31 {name} ({address})",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.address = address
        self.device_name = name

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the SHT31 gadget via BLE GATT connection."""
        ble_device = bluetooth.async_ble_device_from_address(
            self.hass, self.address, connectable=True
        )

        if not ble_device:
            raise UpdateFailed(
                f"Bluetooth device {self.address} ({self.device_name}) not found or not connectable in range"
            )

        _LOGGER.debug("Connecting to Sensirion SHT31 at %s", self.address)

        try:
            async with BleakClient(ble_device, timeout=15.0) as client:
                if not client.is_connected:
                    raise UpdateFailed(f"Could not connect to {self.address}")

                # Read temperature (IEEE-754 32-bit float, little-endian)
                raw_temp = await client.read_gatt_char(TEMP_CHAR_UUID)
                temperature = round(struct.unpack("<f", raw_temp)[0], 2)

                # Read humidity (IEEE-754 32-bit float, little-endian)
                raw_hum = await client.read_gatt_char(HUM_CHAR_UUID)
                humidity = round(struct.unpack("<f", raw_hum)[0], 2)

                # Read battery level (uint8, 0-100%)
                battery: int | None = None
                try:
                    raw_bat = await client.read_gatt_char(BATT_CHAR_UUID)
                    if raw_bat:
                        battery = int(raw_bat[0])
                except Exception as bat_err:
                    _LOGGER.debug("Could not read battery level from %s: %s", self.address, bat_err)

                _LOGGER.debug(
                    "SHT31 %s read success -> Temp: %s°C, Hum: %s%%, Bat: %s%%",
                    self.address,
                    temperature,
                    humidity,
                    battery,
                )

                return {
                    "temperature": temperature,
                    "humidity": humidity,
                    "battery": battery,
                }

        except Exception as err:
            raise UpdateFailed(
                f"Error communicating with Sensirion SHT31 ({self.address}): {err}"
            ) from err
