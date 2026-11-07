# event — событийная модель

```lua
local event = require("event")
```

- `event.pull([timeout], [name], [filter...])` — блокирующее ожидание; возвращает `name, args...`
- `event.pullMultiple(name1, name2, ...)` — ждать несколько типов событий
- `event.listen(name, callback)`, `event.ignore(name, callback)` — callback-стиль
- `event.timer(interval, callback[, times])` — таймер; возвращает id, отмена `event.cancel(id)`
- `event.cancel(id)`
- `event.push(name, ...)` — сгенерировать событие вручную

## Грабли
- `pull()` без таймаута ждёт вечно — для циклов ставь `pull(0.05)` и проверяй имя события
- В вечном цикле лови `"interrupted"` (Ctrl+C)
