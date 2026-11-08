# key_down
Генерируется при нажатии клавиши на клавиатуре.

**Сигнатура:** `key_down(keyboardAddress: string, char: number, code: number, playerName: string)`

- `keyboardAddress` — адрес клавиатуры (string)
- `char` — КОД символа (number, НЕ строка!). Для получения символа: `unicode.char(char)`
- `code` — код клавиши (number). Enter=28, Esc=1, Backspace=14, F1..F6=59..64
- `playerName` — ник игрока (string)
