# Arduino - Контроллер температуры

Система позволяет контролировать температуру водяной системы отопления отправляя в телеграмм температуру радиатора отопления, температуру помещения и влажность.

## Для работы испольузются следующие модули

- Arduino AT Mega 2560 
- Датчик температуры DHT11 (https://роботехника18.рф/dht11/)
- Датчик температуры и влажности DS18B20 (https://3d-diy.ru/wiki/arduino-datchiki/tsifrovoy-datchik-temperatury-ds18b20/)

## Установка

Для работы системы требуется python3
Внимание, для работы скрипта требуется создать и заполнить файл .env по образцу,
требуется задать минимальную и максимальную температуру для индикации

```sh
pip install requests
pip install pyserial
pip install python-dotenv
```

## Настройка
Используя файл .env укажите следующие параметры:
```sh
TOKEN="" # Токен для телеграмм-бота
BOT_ID=""
CHAT_ID="" # id чата с ботом, куда отправлять статистику
MAX_TEMPERATURE=80 
MIN_TEMPERATURE=15
COM_PORT="COM5" # порт для приема данных от платы arduino
LOG_FILE="log.txt"
```

## Запуск

```sh
python index.py
```

## Зависимости для скетча

Чтобы использовать эти библиотеки, откройте диспетчер библиотек в Arduino IDE и установите ее оттуда.

| Библиотека | Ссылка |
| ------ | ------ |
| OneWire | [https://www.arduino.cc/reference/en/libraries/onewire/][PlDb] |
| DHT | [https://www.arduino.cc/reference/en/libraries/dht-sensor-library/][PlGh] |

## Лицензия

MIT
