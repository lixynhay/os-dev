# modem_message — сетевое сообщение

```lua
modem_message(localAddress, remoteAddress, port, distance, ...)
```
`...` — те же аргументы, что передали в `modem.send/broadcast` (строки/числа/boolean).
Таблицы передаются сериализованными.

```lua
local event = require("event")
local modem = require("component").modem
modem.open(123)
local _, _, from, port, dist, msg = event.pull("modem_message")
```

Перед приёмом порт обязан быть открыт (`modem.open`), иначе сообщения теряются молча.
