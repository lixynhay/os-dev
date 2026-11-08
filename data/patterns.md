# Типовые паттерны OpenComputers

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

---

## ⚠️ КРИТИЧНЫЕ ГРАБЛИ (проверено на практике)

### 1. `touch`: screenAddress — это АДРЕС, а не X!
```lua
local ev, p1, p2, p3, p4, p5 = event.pull("touch")
if ev == "touch" then
    local screenAddr = p1 -- АДРЕС ЭКРАНА (string!)
    local x = p2           -- Координата X (number)
    local y = p3           -- Координата Y (number)
    local button = p4
    local player = p5      -- Ник игрока (string)
end
```
**Ошибка:** `local x, y = event.pull("touch")` — тогда `x` станет адресом, а `y` — координатой X. Координата Y потеряется.

### 2. `key_down`: p2 — это КОД символа (number), а не строка!
```lua
local ev, p1, p2, p3, p4 = event.pull("key_down")
if ev == "key_down" then
    local kbAddr = p1     -- Адрес клавиатуры
    local charCode = p2   -- Число! Для получения символа: unicode.char(charCode)
    local keyCode = p3    -- Код клавиши (Enter=28, Esc=1, Backspace=14, F1..F6=59..64)
    local player = p4
    if charCode and charCode > 32 then
        local typedChar = unicode.char(charCode)
    end
end
```

### 3. `scroll`: сигнатура как у touch + direction в p4
```lua
local ev, p1, p2, p3, p4, p5 = event.pull("scroll")
if ev == "scroll" then
    -- p4: 1 = вверх, -1 = вниз
end
```

### 4. PIM: поля `display_name` и `qty`, а не `label` и `size`
```lua
local stack = pim.getStackInSlot(slot)
if stack then
    local label = stack.display_name or stack.label or stack.name
    local amount = math.floor(tonumber(stack.qty) or tonumber(stack.size) or 0)
    local name = stack.id or stack.name
    local dmg = math.floor(tonumber(stack.damage) or tonumber(stack.dmg) or 0)
end
```
**Всегда** применяй `math.floor` к `qty`/`size` — PIM возвращает float (`1.0`).

### 5. AE2: методы энергии называются иначе
```lua
-- НЕТ методов getEnergyStored/getMaxEnergyStored!
local stored = me_interface.getStoredPower()
local max = me_interface.getMaxStoredPower()
local injection = me_interface.getAvgPowerInjection()
local usage = me_interface.getAvgPowerUsage()
```

### 6. AE2: для NBT-предметов используй fingerprint
```lua
local items = me_interface.getItemsInNetwork()
for _, item in ipairs(items) do
    -- item.fingerprint — готовый отпечаток для exportItem
    me_interface.exportItem(item.fingerprint, "UP", 1)
end
```

### 7. `getCraftables` возвращает userdata, проверяй через pcall
```lua
local ok, craftables = pcall(me_interface.getCraftables)
if ok and craftables then
    for _, c in ipairs(craftables) do
        local stack = c.getItemStack()
        -- ...
    end
end
```

### 8. Перезагрузка компьютера: `computer.shutdown(true)`, а не `reboot`
```lua
computer.shutdown(true)  -- true = перезагрузка
computer.shutdown()      -- без аргументов = выключение
```

### 9. UTF-8: `unicode.len`, а не `#`
```lua
local unicode = require("unicode")
local len = unicode.len("Привет")   -- 6 (символы)
local sub = unicode.sub("Привет", 1, 3)  -- "При"
local wlen = unicode.wlen("Привет") -- ширина для центрирования
```

### 10. Не фильтруй touch через `event.pull("touch")` при нескольких событиях
```lua
-- ПЛОХО (может пропускать события):
local ev, a, b = event.pull(0.05, "touch", "key_down")

-- ХОРОШО (лови всё, проверяй внутри):
local ev, a, b, c = event.pull(0.05)
if ev == "touch" then -- ...
elseif ev == "key_down" then -- ...
```

### 11. Атомарная запись файлов (защита БД)
```lua
local function safeSave(path, content)
    local tmpPath = path .. ".tmp"
    local f = io.open(tmpPath, "w")
    if not f then return false end
    f:write(content)
    f:close()
    if filesystem.exists(path) then filesystem.remove(path) end
    return filesystem.rename(tmpPath, path)
end
```

### 12. Dirty Flag + Throttling для плавного GUI
```lua
local state = { dirty = false, lastRender = 0 }
local RENDER_INTERVAL = 0.1 -- 10 FPS максимум

local function requestRedraw() state.dirty = true end

while true do
    local ev = event.pull(0.05)
    if state.dirty and (computer.uptime() - state.lastRender > RENDER_INTERVAL) then
        drawScreen()
        state.dirty = false
        state.lastRender = computer.uptime()
    end
end
```

### 13. TTL-кэш для тяжёлых запросов
```lua
local cache = { data = nil, time = 0 }
local CACHE_TTL = 2.0

local function getCachedItems(force)
    if force or not cache.data or (computer.uptime() - cache.time > CACHE_TTL) then
        cache.data = me_interface.getItemsInNetwork()
        cache.time = computer.uptime()
    end
    return cache.data
end

-- Точечный запрос (быстрее, чем обход всей сети):
-- local iron = me_interface.getItemsInNetwork({name = "minecraft:iron_ingot"})
```

### 14. `event.pull` без таймаута блокирует навсегда
```lua
-- ПЛОХО (можно зависнуть):
local ev = event.pull("touch")

-- ХОРОШО (есть таймаут):
local ev = event.pull(0.1, "touch")

-- ИЛИ (лови всё, проверяй внутри):
local ev = event.pull(0.1)
```

### 15. Модалки на маленьких экранах
```lua
-- Всегда проверяй, влезает ли окно:
local mw, mh = 56, 16
local mx = math.floor((W - mw) / 2) + 1
local my = math.floor((H - mh) / 2) + 1
if mx < 1 or my < 1 or mx + mw > W or my + mh > H then
    -- Не рисуй модалку, покажи сообщение "Экран слишком мал"
end
