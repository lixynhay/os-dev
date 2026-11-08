# touch
Генерируется при клике по экрану (монитору) 2-го или 3-го уровня.

**Сигнатура:** `touch(screenAddress: string, x: number, y: number, button: number, playerName: string)`

- `screenAddress` — адрес экрана (string, НЕ координата!)
- `x` — координата X (number)
- `y` — координата Y (number)
- `button` — кнопка мыши (number)
- `playerName` — ник игрока (string)

**Важно:** если используешь `local x, y = event.pull("touch")`, то x получит адрес, y — координату X. Правильно: `local _, _, x, y = event.pull("touch")`.
```
