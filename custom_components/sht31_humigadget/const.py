"""Constants for Sensirion SHT31 Smart Humigadget integration."""

DOMAIN = "sht31_humigadget"
DEFAULT_NAME = "Smart Humigadget SHT31"
DEFAULT_SCAN_INTERVAL = 60

CONF_MAC = "mac"
CONF_NAME = "name"
CONF_SCAN_INTERVAL = "scan_interval"

# Sensirion Smart Humigadget GATT Service & Characteristic UUIDs
# Temperature Service & Characteristic (Float32 Little-Endian)
TEMP_SERVICE_UUID = "00002234-b38d-4985-720e-0f993a68ee41"
TEMP_CHAR_UUID    = "00002235-b38d-4985-720e-0f993a68ee41"

# Humidity Service & Characteristic (Float32 Little-Endian)
HUM_SERVICE_UUID  = "00001234-b38d-4985-720e-0f993a68ee41"
HUM_CHAR_UUID     = "00001235-b38d-4985-720e-0f993a68ee41"

# Battery Service & Characteristic (uint8 percentage)
BATT_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
BATT_CHAR_UUID    = "00002a19-0000-1000-8000-00805f9b34fb"
