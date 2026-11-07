# Типовые паттерны

## Тик-цикл с событиями (основа любой программы)
```lua
local event = require("event")
while true do
  local ev, a, b, c = event.pull(0.5)
  if ev == "interrupted" then break
  elseif ev == "touch" then        -- a=адрес, b=x, c=y
    onTouch(b, c)
  elseif ev == "key_down" then
    onKey(c)
  end
end
```

## Центрирование текста (unicode-safe)
```lua
local unicode = require("unicode")
local function center(y, s, gpu)
  local w = gpu.getResolution()
  gpu.set(math.floor((w - unicode.wlen(s)) / 2) + 1, y, s)
end
```

## Прокрутка лога через gpu.copy
```lua
local function scrollLog(gpu, x, y, w, h)
  gpu.copy(x, y + 1, w, h - 1, 0, -1)  -- поднять содержимое на строку
  gpu.fill(x, y + h - 1, w, 1, " ")    -- очистить последнюю строку
end
```

## Кнопки на экране
```lua
local buttons = {{x1=5, y1=3, x2=15, y2=5, label="Купить", action=buy}}
local function click(x, y)
  for _, b in ipairs(buttons) do
    if x >= b.x1 and x <= b.x2 and y >= b.y1 and y <= b.y2 then b.action() end
  end
end
```

## Пинг-понг по модему
```lua
local component = require("component")
local event = require("event")
local serialization = require("serialization")
local modem = component.modem
modem.open(123)
-- клиент:
modem.send(serverAddr, 123, serialization.serialize({cmd = "buy", item = "stone"}))
local _, _, from, port, _, msg = event.pull("modem_message")
local data = serialization.unserialize(msg)
```
