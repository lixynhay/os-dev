# interrupted — Ctrl+C в консоли

Приходит, когда игрок жмёт Ctrl+C в терминале. **Обязательно обрабатывай в вечных циклах**, иначе скрипт не остановить без перезагрузки компьютера.

```lua
local event = require("event")
while true do
  local ev = event.pull(0.5)          -- тик-цикл
  if ev == "interrupted" then break end
end
```

Без таймаута `pull("interrupted")` перекроет рабочие события — используй общий pull с проверкой имени.
