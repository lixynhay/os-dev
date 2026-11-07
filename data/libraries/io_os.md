# io / os — базовый ввод-вывод OpenOS

- `print(...)`, `io.write(...)` — вывод в консоль
- `io.read("*l")` — строка из консоли
- `io.open(path, mode)` — файлы (`r/w/a`), `f:read(n)`, `f:write(s)`, `f:close()`
- `os.sleep(seconds)` — неблокирующий сон (через таймеры)
- `os.exit()` — завершить программу
- `os.time()`, `os.clock()` — в OpenOS ограниченные (нет полноценных часов; uptime через `computer.uptime()`)

## ⚠️ НЕ ComputerCraft
Нет `os.pullEvent`, `os.loadAPI`, `shell.run` как в CC (в OpenOS свой `shell`).
