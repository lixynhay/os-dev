# pim — Personal Inventory Manager (OpenPeripheral)

События (генерируются, когда игрок встаёт/сходит с плиты):
- `player_on(name, uuid)`
- `player_off(name, uuid)`

Типовой сценарий: магазин/выдача предметов по игроку на платформе.

## Грабли
- Компонент существует только при установленном OpenPeripheral
- Имена методов/событий между версиями OpenPeripheral плавают — проверяй
  `component.methods(address)` и мониторинг событий (`=event.pull()` в консоли)
