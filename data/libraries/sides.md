# sides — стороны света/блока

```lua
local sides = require("sides")
-- sides.bottom=0, sides.top=1, sides.north=2, sides.south=3, sides.west=4, sides.east=5
```

Используется в `redstone`, `inventory_controller` и др. — сторона считается от блока-компонента.
Есть и человеческие алиасы: `sides.down/sides.up`.
