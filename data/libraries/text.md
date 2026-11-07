# text — утилиты строк

```lua
local text = require("text")
```

- `text.padRight(s, n)` / `text.padLeft(s, n)` — дополнить пробелами до длины (аккуратно с кириллицей — длина в байтах)
- `text.split(s, sep)` — разбить по разделителю
- `text.trim(s)` — убрать пробелы по краям (в новых версиях)
