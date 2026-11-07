# filesystem (fs) — файлы в OpenOS

```lua
local fs = require("filesystem")
```

- `fs.get(path)` — прокси-компонент тома для пути
- `fs.exists(path)`, `fs.isDirectory(path)`, `fs.list(path)`
- `fs.makeDirectory(path)`, `fs.remove(path)`, `fs.rename(a, b)`, `fs.copy(a, b)`
- `fs.size(path)`
- Пути: `/mnt/<адрес-диска>/...`; дискеты и жёсткие диски монтируются автоматически

```lua
local f = io.open("/mnt/xxx/myprog.lua", "w")
f:write("print('hello')")
f:close()
```
