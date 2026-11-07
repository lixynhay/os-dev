# eeprom — микросхема BIOS

- `get(): string` — текущий Lua-код BIOS
- `set(data: string)`
- `getLabel()`, `setLabel(label)`
- `getSize()` / `getDataSize()` — ёмкость в байтах (зависит от версии)

## Грабли
- Прошивка хранит только BIOS-код; данные для неё — через `computer.getBootAddress()`
- Записать можно только если EEPROM не заблокирован (flash из крафта с книгой)
