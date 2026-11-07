# unicode — UTF-8 строки (КРИТИЧНО для кириллицы)

```lua
local unicode = require("unicode")
```

- `unicode.len(s)` — число СИМВОЛОВ (оператор `#` считает байты: русская буква = 2 байта!)
- `unicode.sub(s, i, j)` — обрезка по символам
- `unicode.char(...)` — собрать строку из кодов
- `unicode.wlen(s)` — печатная ширина (двойные символы = 2 колонки) — для центрирования
- `unicode.lower(s)`, `unicode.upper(s)`

```lua
local s = "Привет"
print(#s)            -- 12 байт — НЕПРАВИЛЬНО для UI
print(unicode.len(s)) -- 6 символов
```
