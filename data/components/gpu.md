# gpu — видеокарта

Привязка к экрану: `gpu.bind(address)`. По умолчанию — к ближайшему экрану.
К одному GPU — один экран.

## Разрешение и глубина цвета
| Тир экрана | maxResolution | Цвета | Глубина |
|---|---|---|---|
| T1 (базовый) | 50×16 | ч/б | 1 бит |
| T2 | 80×25 | 16 | 4 бита |
| T3 | 160×50 | 256 | 8 бит |

- `maxResolution(): w, h`
- `getResolution(): w, h`
- `setResolution(w, h): bool`
- `maxDepth(): number`, `getDepth()`, `setDepth(depth)`

## Цвет
- `setForeground(color[, palette]): oldColor` — color: `0xRRGGBB` (T3) или индекс палитры
- `getForeground(): color, palette`
- `setBackground(color[, palette])`, `getBackground()`
- `setPaletteColor(index, value)`, `getPaletteColor(index)` — T2/T3

## Вывод
- `set(x, y, value[, vertical])` — value: строка, unicode поддерживается
- `get(x, y): char, fg, bg`
- `fill(x, y, w, h, char)`
- `copy(x, y, w, h, tx, ty)` — сдвиг области экрана; основа быстрой прокрутки

## Грабли
- `setResolution()` НЕ заливает экран заново — сделай `gpu.fill(1, 1, w, h, " ")` после смены разрешения
- Координаты за пределами экрана → ошибка, проверяй границы
- Для центрирования текста считай ширину через `unicode.wlen()` (двойная ширина символов)
