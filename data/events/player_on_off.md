# player_on / player_off — PIM (OpenPeripheral)

```lua
player_on(name: string, uuid: string)
player_off(name: string, uuid: string)
```

```lua
local eventName, playerName = event.pull("player_on", "player_off")
if eventName == "player_on" then
  print("Игрок " .. playerName .. " встал на PIM.")
else
  print("Игрок " .. playerName .. " сошёл с PIM.")
end
```

`event.pull("player_on", "player_off")` ловит оба — смотри первое возвращённое значение.
События генерирует блок PIM — нужен установленный OpenPeripheral.
