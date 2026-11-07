# modem — сетевая карта (проводная/беспроводная)

- `open(port): bool` — ОБЯЗАТЕЛЬНО перед приёмом, порт 1..65535
- `close([port])`
- `isOpen(port): bool`
- `send(remoteAddress, port, ...)` — конкретному компьютеру
- `broadcast(port, ...)` — всем в сети/радиусе
- `isWireless(): bool`
- `getStrength(): number`, `setStrength(dB)` — только беспроводные

Событие приёма: `modem_message(localAddress, remoteAddress, port, distance, ...)`.

## Грабли
- Порт не открыт → входящие молча теряются, без ошибок
- Таблицы через модем: сериализуй через `serialization.serialize` / `unserialize`
- В беспроводной сети ограничен радиус (`setStrength`), кабель — без лимита
