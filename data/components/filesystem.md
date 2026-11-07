# filesystem — диск/дискета/ROM (компонент)

В OpenOS диски автоматически монтируются в `/mnt/<короткий-адрес>`.
Для обычной работы с файлами используй `io.open` + библиотеку `filesystem`,
component-прокси нужен для низкоуровневых задач.

- `exists(path)`, `isDirectory(path)`, `list(path)`
- `makeDirectory(path)`, `remove(path)`, `rename(from, to)`
- `size(path)`, `spaceUsed()`, `spaceTotal()`, `isReadOnly()`
- `open(path, mode)` → файл с `read(n)/write(s)/close()`, mode `"r"/"w"/"a"`
- `getLabel()`, `setLabel(s)` — дискеты

## Грабли
- `open(path, "w")` молча затирает файл
- ROM (EEPROM/прошивка) — только чтение
