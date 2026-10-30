# Sensirion SHT31 Smart Humigadget for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/default)
[![GitHub release](https://img.shields.io/github/v/release/AeddinPL/sht31-humigadget-ha-integration?include_prereleases)](https://github.com/AeddinPL/sht31-humigadget-ha-integration/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Niestandardowa integracja (Custom Component) dla **Home Assistant** umożliwiająca odczyt danych z czujnika **Sensirion SHT31 Smart Humigadget** za pośrednictwem Bluetooth Low Energy (BLE GATT).

---

## 🧐 Dlaczego ta integracja? / Why this integration?

### [PL]
Oficjalna, wbudowana w Home Assistant integracja `Sensirion BLE` obsługuje wyłącznie urządzenia nadające dane w trybie pasywnym (*BLE Advertisements*, takie jak nowsze gadżety *SHT4x* czy *MyCO2*). 

Starszy **Sensirion SHT31 Smart Humigadget** **nie rozgłasza** wartości pomiarowych w pakietach radiowych — wysyła jedynie minimalną ramkę rozgłoszeniową (`0x02 0x01 0x06`) i nazwę `Smart Humigadget`. Aby pobrać z niego temperaturę i wilgotność, wymagane jest **aktywne połączenie BLE GATT** i odczyt dedykowanych serwisów.

Ta integracja wypełnia tę lukę:
- Łączy się bezpośrednio z sensorem SHT31 po Bluetooth.
- Odczytuje temperaturę, wilgotność oraz stan baterii.
- Natychmiast zwalnia połączenie po odczycie, gwarantując **długą żywotność baterii pastylkowej CR2032**.

### [EN]
The official Home Assistant `Sensirion BLE` integration only supports devices broadcasting telemetry in passive BLE advertisement frames (such as the *SHT4x Smart Gadget* or *MyCO2*).

The older **Sensirion SHT31 Smart Humigadget** does **not** broadcast measurements in advertisement packets — it only broadcasts basic discovery flags (`0x02 0x01 0x06`) and the local name `Smart Humigadget`. Reading live temperature and humidity requires an **active BLE GATT connection**.

This custom integration enables full GATT reading for the SHT31 Smart Humigadget while conserving the CR2032 coin-cell battery by disconnecting immediately after each poll.

---

## ✨ Funkcje / Features

* 🌡️ **Temperatura** (°C) – 32-bitowy format zmiennoprzecinkowy IEEE 754.
* 💧 **Wilgotność** (%RH) – 32-bitowy format zmiennoprzecinkowy IEEE 754.
* 🔋 **Poziom baterii** (%) – z kategorii diagnostycznej Home Assistant.
* 🔍 **Automatyczne wykrywanie (Bluetooth Discovery)** – Home Assistant automatycznie powiadomi Cię o znalezieniu czujnika w pobliżu.
* ⚡ **Optymalizacja baterii** – krótkie cykliczne połączenie co 60 sekund i natychmiastowe rozłączenie.
* 📡 **Wsparcie dla Bluetooth Proxy** – działa zarówno z lokalnym adapterem USB w HA (np. w Proxmox/Raspberry Pi), jak i zdalnymi bramkami **ESPHome Bluetooth Proxy**.

---

## 📦 Instalacja / Installation

### Metoda 1: HACS (Zalecana / Recommended)

1. Upewnij się, że masz zainstalowany [HACS](https://hacs.xyz/).
2. W Home Assistant przejdź do **HACS** → **Integracje** (*Integrations*).
3. Kliknij ikonę trzech kropek w prawym górnym rogu i wybierz **Niestandardowe repozytoria** (*Custom repositories*).
4. Wklej URL tego repozytorium GitHub:
   ```
   https://github.com/AeddinPL/sht31-humigadget-homeassistant
   ```
5. Wybierz kategorię: **Integracja** (*Integration*) i kliknij **Dodaj** (*Add*).
6. Znajdź **Sensirion SHT31 Smart Humigadget** i kliknij **Pobierz** (*Download*).
7. Zrestartuj Home Assistant.

---

### Metoda 2: Ręczna instalacja / Manual Installation

1. Pobierz archiwum ZIP tego repozytorium z zakładki [Releases](https://github.com/AeddinPL/sht31-humigadget-homeassistant/releases).
2. Skopiuj folder `custom_components/sht31_humigadget/` do katalogu konfiguracji Twojego Home Assistant:
   ```
   /config/custom_components/sht31_humigadget/
   ```
3. Zrestartuj Home Assistant:
   * **Ustawienia** → **System** → **Uruchom ponownie** (lub *Narzędzia deweloperskie* → *Zrestartuj*).

---

## ⚙️ Konfiguracja / Configuration

### Automatyczne wykrycie (Auto-Discovery)
Jeśli Bluetooth w Twoim Home Assistant działa i słyszy sensor, w sekcji **Ustawienia** → **Urządzenia oraz usługi** pojawi się kafelek z powiadomieniem o wykryciu czujnika **Smart Humigadget**. Wystarczy kliknąć **Konfiguruj** (*Configure*) i potwierdzić.

### Dodanie ręczne
1. Wejdź w **Ustawienia** (*Settings*) → **Urządzenia oraz usługi** (*Devices & Services*).
2. Kliknij **Dodaj integrację** (*Add Integration*) w prawym dolnym rogu.
3. Wyszukaj: **Sensirion SHT31 Smart Humigadget**.
4. Wprowadź adres MAC czujnika Bluetooth (np. `F3:15:B7:5E:61:C2`) oraz opcjonalną nazwę urządzenia.
5. Kliknij **Zatwierdź** (*Submit*).

---

## 🛠️ Dane techniczne GATT / Technical GATT Details

Dla celów referencyjnych, czujnik Sensirion SHT31 Smart Humigadget korzysta z następujących serwisów i cech GATT:

| Sensor | Service UUID | Characteristic UUID | Format |
| :--- | :--- | :--- | :--- |
| **Temperatura** | `00002234-b38d-4985-720e-0f993a68ee41` | `00002235-b38d-4985-720e-0f993a68ee41` | Float32 Little-Endian (°C) |
| **Wilgotność** | `00001234-b38d-4985-720e-0f993a68ee41` | `00001235-b38d-4985-720e-0f993a68ee41` | Float32 Little-Endian (%RH) |
| **Bateria** | `0000180f-0000-1000-8000-00805f9b34fb` | `00002a19-0000-1000-8000-00805f9b34fb` | uint8 (0–100%) |

---

## ❓ Rozwiązywanie problemów / Troubleshooting

* **Sensor nie jest wykrywany / Błąd połączenia:**
  * Upewnij się, że Bluetooth w gadżecie jest włączony (symbol Bluetooth widoczny na wyświetlaczu LCD). Jeśli go nie ma, przytrzymaj przycisk na płytce przez 2 sekundy.
  * Upewnij się, że aplikacja na telefonie (*Sensirion MyAmbience*) jest wyłączona – dopóki telefon utrzymuje aktywne połączenie, żadne inne urządzenie nie połączy się z gadżetem.
  * Sprawdź baterię CR2032 – słaba bateria może uniemożliwić nawiązanie stabilnego połączenia radiowego.
  * Zbliż czujnik na czas parowania do odbiornika Bluetooth w Home Assistant.

---

## 📄 Licencja / License

Projekt udostępniany na zasadach licencji [MIT](LICENSE).

