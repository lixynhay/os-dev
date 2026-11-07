# key_down — нажатие клавиши (с клавиатуры OC)

```lua
key_down(keyboardAddress: string, char: number, code: number, playerName: string)
```
- `char` — код символа (для букв/цифр), 0 для служебных клавиш
- `code` — скан-код клавиши; сравнивай с константами:

```lua
local keyboard = require("keyboard")
local _, _, c = event.pull("key_down")
if c == keyboard.keys.enter then ... end
if c == keyboard.keys.space then ... end
if c == keyboard.keys.back then ... end  -- backspace
-- стрелки: keyboard.keys.left / right / up / down
```
