# component — доступ к компонентам

```lua
local component = require("component")
```

- `component.gpu`, `component.screen` — прямой доступ (первый найденный компонент типа)
- `component.isAvailable(type): bool`
- `component.list([filter])` — итератор `(address, type)` по всем компонентам; фильтр по имени/шаблону
- `component.proxy(address)` — прокси с методами по адресу
- `component.methods(address)` — таблица методов компонента (`{name = docstring}`)
- `component.type(address)`, `component.slot(address)`

## Паттерн: несколько одинаковых компонентов
```lua
for address, ctype in component.list("screen") do
  print(ctype, address)
end
```
