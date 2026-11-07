# drop — отпускание кнопки на экране

```lua
drop(screenAddress, x, y, button, playerName)
```
Приходит после `touch`/`drag` при отпускании. Распаковка: `local _, _, x, y = event.pull("drop")`.
