# internet — HTTP-карта

```lua
local internet = require("internet")
```

- `internet.request(url[, data[, headers]]): table` — POST если data задано
- Ответ — итератор строк (или `internet.socket` для потоковых сокетов)

## Грабли
- Нужна internet-карта (компонент) и `enableHttp`/`enableHttp` в конфиге OC
- Обычно запрещено в многопользовательских серверах
