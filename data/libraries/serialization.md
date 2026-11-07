# serialization — таблицы ⇄ строки

```lua
local serialization = require("serialization")
```

- `serialization.serialize(value[, pretty]): string`
- `serialization.unserialize(str): value|nil, err`

Применение: конфиги на диске, передача таблиц через `modem.send`.
Строка на выходе — валидный Lua-табличный литерал.

## Грабли
- Функции и userdata не сериализуются
- В старых версиях есть лимит длины строки — большие таблицы режь на части
