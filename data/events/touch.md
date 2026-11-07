# touch — клик по экрану (T2/T3)

```lua
touch(screenAddress: string, x: number, y: number, button: number, playerName: string)
```

## ❌ Главная ошибка OC
```lua
local x, y = event.pull("touch")  -- x = адрес экрана (строка!), y = координата X
```

## ✅ Правильно
```lua
local _, _, x, y = event.pull("touch")
-- или: local _, addr, x, y, btn, player = event.pull("touch")
```

`button`: 0 = левый, 1 = правый. GUI vs touch регулируется `screen.setTouchModeInverted()`.
