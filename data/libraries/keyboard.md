# keyboard — коды клавиш

```lua
local keyboard = require("keyboard")
-- keyboard.keys.enter, .space, .back, .tab, .escape
-- .left, .right, .up, .down, .home, .end_key, .delete
-- буквы/цифры: keyboard.keys.a, keyboard.keys["1"] (по имени)
```

Юзай со `key_down`: третий аргумент события — скан-код, сравнивай с константами.
