# drag — протаскивание по экрану

Сигнатура **точно такая же**, как у `touch`:
```lua
drag(screenAddress, x, y, button, playerName)
```
Шлётся многократно при движении с зажатой кнопкой. Та же ошибка с распаковкой: `local _, _, x, y = event.pull("drag")`.
