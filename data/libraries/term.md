# term — терминал OpenOS

```lua
local term = require("term")
```

- `term.clear()` — очистить экран, курсор в (1,1)
- `term.clearLine()` — очистить строку (прогресс-бары)
- `term.write(s)` — вывод без переноса строки
- `term.setCursor(x, y)`, `term.getCursor(): x, y`

## ⚠️ Это НЕ ComputerCraft
Нет `term.setTextColor()`, `term.getCursorPos()`, `term.setCursorPos()`.
Цвет: `gpu.setForeground()/setBackground()`. Позиция: `term.setCursor()`.
События: `event.pull()`, не `os.pullEvent()`.
