<p align="center">
  <img src="assets/banner.svg" alt="Yandex Eat for Home Assistant" width="100%">
</p>

<p align="center">
  <img src="assets/icon.svg" alt="Yandex Eat" width="128" height="128">
</p>

<p align="center">
  <a href="https://github.com/BadKikoSecond/hass_yandex_eat/releases">
    <img src="https://img.shields.io/github/v/release/BadKikoSecond/hass_yandex_eat?label=версия&style=for-the-badge" alt="Версия">
  </a>
  <a href="https://www.home-assistant.io/">
    <img src="https://img.shields.io/badge/Home%20Assistant-2024.1%2B-03A9F4?style=for-the-badge&logo=home-assistant&logoColor=white" alt="Home Assistant 2024.1+">
  </a>
  <a href="https://hacs.xyz/">
    <img src="https://img.shields.io/badge/HACS-Custom-FE7403?style=for-the-badge&logo=home-assistant&logoColor=white" alt="HACS Custom">
  </a>
  <img src="https://img.shields.io/badge/Яндекс%20Еда-Деливери-Лавка-FC3F1D?style=for-the-badge" alt="Сервисы">
</p>

<p align="center">
  <a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=BadKikoSecond&repository=hass_yandex_eat&category=integration">
    <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Добавить в HACS">
  </a>
  &nbsp;
  <a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=yandex_eat">
    <img src="https://my.home-assistant.io/badges/config_flow_start.svg" alt="Добавить интеграцию">
  </a>
</p>

<p align="center">
  <strong>🇷🇺 <a href="#yandex-eat--home-assistant">Русский</a> · 🇬🇧 <a href="#english">English</a></strong>
</p>

---

# Yandex Eat · Home Assistant

> Неофициальная интеграция Home Assistant и CLI для отслеживания заказов **Яндекс Еда**, **Деливери** и **Лавка**.

Интеграция опрашивает API заказов в реальном времени, создаёт сенсоры для автоматизаций и уведомлений, поддерживает **несколько аккаунтов** и авторизацию через **QR-код** или **x-token** (как в [Yandex Station](https://github.com/AlexxIT/YandexStation)).

| Возможность | Описание |
|-------------|----------|
| 🍔 **Три сервиса** | Еда, Деливери (Market Delivery) и Лавка в одной интеграции |
| 📦 **Активные заказы** | Статус, ETA курьера, «курьер рядом» |
| 📊 **История** | Прошлые заказы и суммы трат по каждому сервису |
| 👥 **Мультиаккаунт** | Добавьте интеграцию повторно для каждого логина |
| ⚡ **Умный опрос** | Интервал ускоряется при приближении курьера |
| 🛠 **CLI** | Опциональный клиент для терминала |

## Быстрый старт

### 1. Добавить в HACS

Нажмите кнопку **«Open in HACS»** вверху страницы или добавьте репозиторий вручную:

1. **HACS** → **Настройки** → **Пользовательские репозитории**
2. URL: `https://github.com/BadKikoSecond/hass_yandex_eat`
3. Категория: **Integration**
4. **HACS** → **Интеграции** → **Yandex Eat** → **Скачать**
5. Перезагрузите Home Assistant

### 2. Настроить интеграцию

**Настройки** → **Устройства и службы** → **Добавить интеграцию** → **Yandex Eat**

| Способ | Инструкция |
|--------|------------|
| **QR-код** | Отсканируйте QR в приложении Яндекс: профиль → добавить аккаунт |
| **Токен** | Вставьте `x_token` из [Yandex Station](https://github.com/AlexxIT/YandexStation) или `core.config_entries` |

Чтобы подключить **второй аккаунт**, снова добавьте интеграцию Yandex Eat — каждый логин создаёт отдельное устройство.

## Сущности

На каждый аккаунт создаётся устройство (например, **Kiko**) со следующими сущностями:

| Сущность | Назначение |
|----------|------------|
| `sensor.*_active_orders` | Количество активных заказов |
| `sensor.*_order_status` | Статус главного заказа (`none` — заказов нет) |
| `sensor.*_courier_eta` | Минут до курьера |
| `binary_sensor.*_courier_nearby` | Курьер рядом (`off`, если заказов нет) |
| `sensor.*_past_orders_eda` | История заказов Еда |
| `sensor.*_past_orders_delivery` | История заказов Деливери |
| `sensor.*_past_orders_lavka` | История заказов Лавка |
| `sensor.*_total_spent` | Потрачено всего (₽) |
| `sensor.*_total_spent_year` | Потрачено за текущий год (₽) |

При нескольких активных заказах «главным» считается заказ с курьером рядом, иначе — с наименьшим ETA.

### Статусы заказа

`none` · `confirmed` · `assembling` · `performer_found` · `delivery_arrived` · `closed` · `unknown`

## Автоматизации

### Курьер рядом

```yaml
alias: Курьер рядом
trigger:
  - platform: state
    entity_id: binary_sensor.kiko_courier_nearby
    from: "off"
    to: "on"
action:
  - service: notify.mobile_app_phone
    data:
      message: "Курьер Яндекс Еды почти у двери"
```

### Курьер через ≤ 5 минут

```yaml
alias: Курьер через 5 минут
trigger:
  - platform: numeric_state
    entity_id: sensor.kiko_courier_eta
    below: 6
condition:
  - condition: template
    value_template: >
      {{ states('sensor.kiko_order_status') not in ['none', 'closed', 'unknown', 'unavailable'] }}
action:
  - service: notify.mobile_app_phone
    data:
      message: "Курьер через {{ states('sensor.kiko_courier_eta') }} мин"
```

## Настройки

**Настроить** у записи интеграции → интервал опроса (15–300 сек, по умолчанию **90**).

Интервал автоматически ускоряется:
- до **15 с**, когда ETA курьера ≤ 5 минут;
- до **10 с**, когда курьер рядом.

## CLI (опционально)

```bash
git clone https://github.com/BadKikoSecond/hass_yandex_eat.git
cd hass_yandex_eat
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -e .
cp .env.example .env          # вставьте YANDEX_X_TOKEN
```

```bash
yandex-eat login
yandex-eat track
yandex-eat track --service eda
yandex-eat track --nearby
yandex-eat track --json
```

## API

```
GET https://eda.yandex.ru/api/v1/providers/orders/v1/tracked-orders      # Еда + Деливери
GET https://lavka.yandex.ru/api/v1/providers/orders/v1/tracked-orders  # Лавка
```

Авторизация: session cookies после обмена `x-token` через `mobileproxy.passport.yandex.net`.

## Структура репозитория

```
hacs.json
assets/                         # баннер и иконка для README
custom_components/yandex_eat/   # интеграция Home Assistant
  manifest.json
  config_flow.py
  sensor.py
  binary_sensor.py
  ...
yandex_eat/                     # CLI-клиент
```

## Разработка

Интеграция пока не входит в default HACS — добавляется как custom repository. Для публикации в default store см. [документацию HACS](https://www.hacs.xyz/docs/publish/integration/).

```bash
# Проверки CI локально
docker run --rm -v $(pwd):/github/workspace ghcr.io/hacs/action:main
```

## Теги репозитория

`home-assistant` · `homeassistant` · `hacs` · `homeassistant-integration` · `yandex` · `yandex-eat` · `yandex-lavka` · `yandex-delivery` · `delivery-tracking` · `smart-home`

---

# English

> Unofficial Home Assistant integration and CLI for tracking **Yandex Eda**, **Delivery**, and **Lavka** orders.

The integration polls order APIs, exposes sensors for automations and notifications, supports **multiple accounts**, and authenticates via **QR code** or **x-token** (same approach as [Yandex Station](https://github.com/AlexxIT/YandexStation)).

| Feature | Description |
|---------|-------------|
| 🍔 **Three services** | Eda, Delivery (Market Delivery), and Lavka in one integration |
| 📦 **Active orders** | Status, courier ETA, courier nearby |
| 📊 **History** | Past orders and spending per service |
| 👥 **Multi-account** | Add the integration again for each login |
| ⚡ **Smart polling** | Poll interval speeds up as the courier approaches |
| 🛠 **CLI** | Optional terminal client |

## Quick start

### 1. Add to HACS

Click **Open in HACS** at the top of this page, or add the repository manually:

1. **HACS** → **Settings** → **Custom repositories**
2. URL: `https://github.com/BadKikoSecond/hass_yandex_eat`
3. Category: **Integration**
4. **HACS** → **Integrations** → **Yandex Eat** → **Download**
5. Restart Home Assistant

### 2. Configure the integration

**Settings** → **Devices & services** → **Add integration** → **Yandex Eat**

| Method | Instructions |
|--------|--------------|
| **QR code** | Scan the QR in the Yandex app: profile → add account |
| **Token** | Paste `x_token` from [Yandex Station](https://github.com/AlexxIT/YandexStation) or `core.config_entries` |

To add a **second account**, add the Yandex Eat integration again — each login creates a separate device.

## Entities

Each account gets a device (e.g. **Kiko**) with these entities:

| Entity | Purpose |
|--------|---------|
| `sensor.*_active_orders` | Number of active orders |
| `sensor.*_order_status` | Primary order status (`none` when no orders) |
| `sensor.*_courier_eta` | Minutes until courier arrival |
| `binary_sensor.*_courier_nearby` | Courier nearby (`off` when no orders) |
| `sensor.*_past_orders_eda` | Eda order history count |
| `sensor.*_past_orders_delivery` | Delivery order history count |
| `sensor.*_past_orders_lavka` | Lavka order history count |
| `sensor.*_total_spent` | Total spent (RUB) |
| `sensor.*_total_spent_year` | Spent in the current year (RUB) |

With multiple active orders, the primary order is the one with courier nearby, otherwise the lowest ETA.

## Automations

### Courier nearby

```yaml
alias: Courier nearby
trigger:
  - platform: state
    entity_id: binary_sensor.kiko_courier_nearby
    from: "off"
    to: "on"
action:
  - service: notify.mobile_app_phone
    data:
      message: "Yandex Eda courier is almost at the door"
```

### Courier in ≤ 5 minutes

```yaml
alias: Courier in 5 minutes
trigger:
  - platform: numeric_state
    entity_id: sensor.kiko_courier_eta
    below: 6
condition:
  - condition: template
    value_template: >
      {{ states('sensor.kiko_order_status') not in ['none', 'closed', 'unknown', 'unavailable'] }}
action:
  - service: notify.mobile_app_phone
    data:
      message: "Courier in {{ states('sensor.kiko_courier_eta') }} min"
```

## Options

**Configure** on the integration entry → poll interval (15–300 s, default **90**).

Polling automatically speeds up to **15 s** when courier ETA ≤ 5 min, and **10 s** when courier is nearby.

## CLI (optional)

```bash
git clone https://github.com/BadKikoSecond/hass_yandex_eat.git
cd hass_yandex_eat
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

```bash
yandex-eat login
yandex-eat track
yandex-eat track --service eda
yandex-eat track --nearby
yandex-eat track --json
```

## API

```
GET https://eda.yandex.ru/api/v1/providers/orders/v1/tracked-orders
GET https://lavka.yandex.ru/api/v1/providers/orders/v1/tracked-orders
```

Auth: session cookies after exchanging `x-token` via `mobileproxy.passport.yandex.net`.

## Development

This integration is not in the default HACS store yet — add it as a custom repository. See [HACS publish docs](https://www.hacs.xyz/docs/publish/integration/) to submit to the default store.

## License

This is an unofficial community project and is not affiliated with Yandex.
